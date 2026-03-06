from fastapi import FastAPI
from .models import Borrower

from .database import engine, SessionLocal, Base
from .db_models import BorrowerRecord, DecisionLog
from .cache import redis_client
from .agents.decision_agent import decision_agent
from .simulation.borrower_simulator import run_simulation
from fastapi.responses import Response
import time
from .policy.policy_engine import apply_policy_overrides

from .observability.metrics import (
    record_request,
    record_llm_call,
    record_cache_hit,
    record_decision,
    get_metrics
)

# create tables automatically if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Credit Decision Engine")

@app.get("/metrics")
def metrics():

    return get_metrics()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/agent_graph")
def agent_graph():

    graph = decision_agent.get_graph()

    png = graph.draw_mermaid_png()

    return Response(content=png, media_type="image/png")


@app.post("/recommend_action")
def recommend_action(borrower: Borrower):

    record_request()

    # Redis cache key
    cache_key = f"borrower:{borrower.borrower_id}"

    # check Redis for cached belief
    cached_belief = redis_client.get(cache_key)

    if cached_belief:
        borrower.repayment_belief = float(cached_belief)
        record_cache_hit()

    if borrower.workflow_stage == "closed_repaid":
        return {"message": "Borrower already closed"}

    # -------- CALL POLICY + AGENT --------

    state = borrower.model_dump()

    start = time.time()

    override_action = apply_policy_overrides(state)

    if override_action:

        action = override_action
        reasoning = "policy_override"
        risk_level = "policy_override"
        latency_ms = 0

    else:

        record_llm_call()

        result = decision_agent.invoke(state) or {}

        latency_ms = (time.time() - start) * 1000

        action = result.get("action", "send_sms")
        reasoning = result.get("reasoning", "")
        risk_level = result.get("risk_level", "unknown")

    # -------- METRICS --------

    record_decision(action, latency_ms)

    # -------- CACHE --------

    redis_client.set(cache_key, borrower.repayment_belief, ex=3600)

    # -------- DATABASE --------

    db = SessionLocal()

    borrower_record = BorrowerRecord(
        borrower_id=borrower.borrower_id,
        outstanding_balance=borrower.outstanding_balance,
        repayment_belief=borrower.repayment_belief,
        workflow_stage=borrower.workflow_stage
    )

    db.add(borrower_record)

    decision_log = DecisionLog(
        borrower_id=borrower.borrower_id,
        action=action,
        risk_level=risk_level,
        repayment_belief=borrower.repayment_belief,
        llm_reasoning=reasoning,
        decision_latency_ms=latency_ms,
        policy_version="v1"
    )

    db.add(decision_log)

    db.commit()
    db.close()

    # -------- RESPONSE --------

    return {
        "borrower_id": borrower.borrower_id,
        "recommended_action": action,
        "repayment_belief": borrower.repayment_belief,
    }

@app.post("/simulate")
def simulate(n: int = 1000):

    results = run_simulation(n)

    return results
