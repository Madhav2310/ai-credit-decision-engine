from fastapi import FastAPI
from .models import Borrower

from .database import engine, SessionLocal, Base
from .db_models import BorrowerRecord, DecisionLog
from .cache import redis_client
from .agents.decision_agent import decision_agent

# create tables automatically if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Credit Decision Engine")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/recommend_action")
def recommend_action(borrower: Borrower):

    # Redis cache key
    cache_key = f"borrower:{borrower.borrower_id}"

    # check Redis for cached belief
    cached_belief = redis_client.get(cache_key)

    if cached_belief:
        borrower.repayment_belief = float(cached_belief)

    if borrower.workflow_stage == "closed_repaid":
        return {"message": "Borrower already closed"}

    # -------- CALL THE AGENT --------

    state = borrower.dict()

    result = decision_agent.invoke(state)

    action = result["action"]

    # --------------------------------

    # store belief in Redis (TTL = 1 hour)
    redis_client.set(cache_key, borrower.repayment_belief, ex=3600)

    # open database session
    db = SessionLocal()

    # save borrower state
    borrower_record = BorrowerRecord(
        borrower_id=borrower.borrower_id,
        outstanding_balance=borrower.outstanding_balance,
        repayment_belief=borrower.repayment_belief,
        workflow_stage=borrower.workflow_stage
    )

    db.add(borrower_record)

    # log the decision
    decision_log = DecisionLog(
        borrower_id=borrower.borrower_id,
        action=action,
        belief=borrower.repayment_belief
    )

    db.add(decision_log)

    # commit transaction
    db.commit()

    # close session
    db.close()

    return {
        "borrower_id": borrower.borrower_id,
        "recommended_action": action,
        "repayment_belief": borrower.repayment_belief,
    }