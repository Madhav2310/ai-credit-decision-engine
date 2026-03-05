import random
from .models import Borrower


ACTIONS = {
    "send_sms": {"cost": 2, "effect": 0.05},
    "auto_call": {"cost": 10, "effect": 0.10},
    "human_call": {"cost": 50, "effect": 0.20},
    "offer_payment_plan": {"cost": 30, "effect": 0.25},
    "do_nothing": {"cost": 0, "effect": 0.0},
}


def update_belief(borrower: Borrower):
    belief = borrower.repayment_belief

    if borrower.promise_to_pay_flag:
        belief += 0.15

    if borrower.last_contact_sentiment > 0.5:
        belief += 0.10

    if borrower.hardship_flag:
        belief -= 0.25

    if borrower.days_overdue > 30:
        belief -= 0.05

    borrower.repayment_belief = max(0.0, min(1.0, belief))


def compute_action_value(borrower: Borrower, action_name: str):
    action = ACTIONS[action_name]

    projected_belief = borrower.repayment_belief + action["effect"]
    projected_belief = max(0.0, min(1.0, projected_belief))

    expected_recovery = projected_belief * borrower.outstanding_balance
    net_value = expected_recovery - action["cost"]

    return net_value


def choose_best_action(borrower: Borrower):
    best_action = "do_nothing"
    best_value = float("-inf")

    for action_name in ACTIONS.keys():
        value = compute_action_value(borrower, action_name)
        if value > best_value:
            best_value = value
            best_action = action_name

    return best_action