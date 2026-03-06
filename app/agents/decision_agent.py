from langgraph.graph import StateGraph
from ..llm.provider import llm
import json
from langgraph.graph import END


from typing import TypedDict

class BorrowerState(TypedDict, total=False):
    repayment_belief: float
    outstanding_balance: float
    engagement_score: float
    income_volatility_score: float
    risk_level: str
    action: str
    reasoning: str


def risk_assessment(state: BorrowerState):
    belief = state.get("repayment_belief", 0.5)

    if belief < 0.3:
        state["risk_level"] = "high"
    elif belief < 0.6:
        state["risk_level"] = "medium"
    else:
        state["risk_level"] = "low"

    return state


def llm_strategy_node(state: BorrowerState):

    balance = state.get("outstanding_balance", 0)
    belief = state.get("repayment_belief", 0.5)
    engagement = state.get("engagement_score", 0)
    volatility = state.get("income_volatility_score", 0)
    risk = state.get("risk_level", "medium")

    prompt = f"""
You are a credit collections strategist.

Borrower profile:
balance: {balance}
repayment belief: {belief}
engagement score: {engagement}
income volatility: {volatility}
risk level: {risk}

Choose the best intervention from:

send_sms
auto_call
human_call
payment_plan

Respond ONLY with JSON in this format:

{{
  "action": "send_sms | auto_call | human_call | payment_plan",
  "reasoning": "short explanation"
}}
"""

    response = llm.invoke(prompt)

    try:
        import json
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

# ---- Build LangGraph ----

builder = StateGraph(BorrowerState)

builder.add_node("risk_assessment", risk_assessment)
builder.add_node("policy_reasoning", llm_strategy_node)

builder.set_entry_point("risk_assessment")

builder.add_edge("risk_assessment", "policy_reasoning")

# tell LangGraph the workflow ends here
builder.set_finish_point("policy_reasoning")

decision_agent = builder.compile()