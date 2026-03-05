import random


def generate_borrower(borrower_id):

    return {
        "borrower_id": borrower_id,
        "outstanding_balance": random.randint(500, 5000),
        "repayment_belief": random.uniform(0.1, 0.9),
        "workflow_stage": "collection",
        "engagement_score": random.uniform(0, 1),
        "income_volatility": random.uniform(0, 1)
    }

def simulate_repayment(borrower, action):

    base_prob = borrower["repayment_belief"]

    if action == "send_sms":
        boost = 0.05
    elif action == "auto_call":
        boost = 0.1
    elif action == "human_call":
        boost = 0.2
    else:
        boost = 0

    repay_probability = min(base_prob + boost, 1)

    return random.random() < repay_probability


from ..agents.decision_agent import decision_agent


def run_simulation(n=1000):

    recovered = 0
    actions = {"send_sms": 0, "auto_call": 0, "human_call": 0}

    for i in range(n):

        borrower = generate_borrower(i)

        result = decision_agent.invoke(borrower)

        action = result["action"]

        actions[action] += 1

        repaid = simulate_repayment(borrower, action)

        if repaid:
            recovered += borrower["outstanding_balance"]

    return {
        "borrowers_simulated": n,
        "total_recovered": recovered,
        "action_distribution": actions
    }