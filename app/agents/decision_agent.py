from langgraph.graph import StateGraph


class BorrowerState(dict):
    pass


def risk_assessment(state: BorrowerState):

    belief = state["repayment_belief"]

    if belief < 0.3:
        state["risk_level"] = "high"
    elif belief < 0.6:
        state["risk_level"] = "medium"
    else:
        state["risk_level"] = "low"

    return state


def select_strategy(state: BorrowerState):

    risk = state["risk_level"]

    if risk == "high":
        state["strategy"] = "aggressive"
    elif risk == "medium":
        state["strategy"] = "moderate"
    else:
        state["strategy"] = "light"

    return state


def choose_action(state: BorrowerState):

    strategy = state["strategy"]

    if strategy == "aggressive":
        state["action"] = "human_call"
    elif strategy == "moderate":
        state["action"] = "auto_call"
    else:
        state["action"] = "send_sms"

    return state


builder = StateGraph(BorrowerState)

builder.add_node("risk_assessment", risk_assessment)
builder.add_node("strategy_selection", select_strategy)
builder.add_node("action_selection", choose_action)

builder.set_entry_point("risk_assessment")

builder.add_edge("risk_assessment", "strategy_selection")
builder.add_edge("strategy_selection", "action_selection")

decision_agent = builder.compile()