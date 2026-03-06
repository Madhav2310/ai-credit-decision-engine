from langgraph.graph import StateGraph
from ..llm.provider import llm
import json


class BorrowerState(dict):
    pass


# ---------------- RISK AGENT ----------------

def risk_agent(state: BorrowerState):

    belief = state.get("repayment_belief", 0.5)

    if belief < 0.3:
        risk = "high"
    elif belief < 0.6:
        risk = "medium"
    else:
        risk = "low"

    state["risk_level"] = risk

    return state


# ---------------- STRATEGY AGENT ----------------

def strategy_agent(state: BorrowerState):

    risk = state.get("risk_level", "medium")

    if risk == "high":
        strategy = "aggressive"

    elif risk == "medium":
        strategy = "moderate"

    else:
        strategy = "light"

    state["strategy"] = strategy

    return state


# ---------------- DECISION AGENT ----------------

def decision_agent_llm(state: BorrowerState):

    balance = state.get("outstanding_balance", 0)
    belief = state.get("repayment_belief", 0.5)
    engagement = state.get("engagement_score", 0)
    volatility = state.get("income_volatility_score", 0)
    risk = state.get("risk_level", "medium")
    strategy = state.get("strategy", "moderate")

    prompt = f"""
You are a credit collections strategist.

Borrower profile:
balance: {balance}
repayment belief: {belief}
engagement score: {engagement}
income volatility: {volatility}
risk level: {risk}
strategy: {strategy}

Choose the best intervention from:

send_sms
auto_call
human_call
payment_plan

Respond ONLY with JSON:

{{
 "action": "...",
 "reasoning": "..."
}}
"""

    response = llm.invoke(prompt)

    try:

        data = json.loads(response.content)

        action = data.get("action", "send_sms")
        reasoning = data.get("reasoning", "")

    except Exception:

        action = "send_sms"
        reasoning = "fallback"

    allowed = ["send_sms", "auto_call", "human_call", "payment_plan"]

    if action not in allowed:
        action = "send_sms"

    state["action"] = action
    state["reasoning"] = reasoning

    return state


# ---------------- GRAPH ----------------

builder = StateGraph(BorrowerState)

builder.add_node("risk_agent", risk_agent)
builder.add_node("strategy_agent", strategy_agent)
builder.add_node("decision_agent", decision_agent_llm)

builder.set_entry_point("risk_agent")

builder.add_edge("risk_agent", "strategy_agent")
builder.add_edge("strategy_agent", "decision_agent")

builder.set_finish_point("decision_agent")

decision_agent = builder.compile()