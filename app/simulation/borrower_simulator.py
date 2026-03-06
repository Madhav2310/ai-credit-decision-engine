import random
from ..agents.decision_agent import decision_agent


def generate_borrower(borrower_id):

    return {
        "borrower_id": borrower_id,
        "outstanding_balance": random.randint(500, 5000),
        "repayment_belief": random.uniform(0.1, 0.9),
        "workflow_stage": "fresh_overdue",
        "engagement_score": random.uniform(0, 1),
        "income_volatility_score": random.uniform(0, 1)
    }


def simulate_repayment(borrower, action):

    base_prob = borrower["repayment_belief"]

    if action == "send_sms":
        boost = 0.05
        cost = 0.05

    elif action == "auto_call":
        boost = 0.1
        cost = 0.2

    elif action == "human_call":
        boost = 0.2
        cost = 1.5

    elif action == "payment_plan":
        boost = 0.3
        cost = 0.8

    else:
        boost = 0
        cost = 0

    repay_probability = min(base_prob + boost, 1)

    repaid = random.random() < repay_probability

    return repaid, cost


def run_simulation(n=1000):

    recovered = 0
    total_cost = 0

    actions = {
        "send_sms": 0,
        "auto_call": 0,
        "human_call": 0,
        "payment_plan": 0
    }

    for i in range(n):

        borrower = generate_borrower(i)

        result = decision_agent.invoke(borrower) or {}

        action = result.get("action", "send_sms")

        actions[action] += 1

        repaid, cost = simulate_repayment(borrower, action)

        total_cost += cost

        if repaid:
            recovered += borrower["outstanding_balance"]

    recovery_rate = recovered / max(1, n)

    avg_cost = total_cost / max(1, n)

    return {
        "borrowers_simulated": n,
        "total_recovered": recovered,
        "recovery_rate": recovery_rate,
        "avg_collection_cost": avg_cost,
        "action_distribution": actions
    }