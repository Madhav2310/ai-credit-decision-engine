def apply_policy_overrides(state):

    # hardship override
    if state.get("hardship_flag"):
        return "payment_plan"

    # very overdue borrowers
    if state.get("days_overdue", 0) > 90:
        return "human_call"

    # unresponsive borrowers
    if state.get("engagement_score", 1) < 0.2:
        return "human_call"

    return None