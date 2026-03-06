from pydantic import BaseModel
from typing import Literal


class Borrower(BaseModel):
    borrower_id: int
    original_loan_amount: float
    outstanding_balance: float
    interest_rate_daily: float

    days_overdue: int
    missed_payment_count: int
    total_paid_so_far: float

    last_contact_sentiment: float
    engagement_score: float
    income_volatility_score: float

    hardship_flag: bool
    promise_to_pay_flag: bool

    repayment_belief: float
    workflow_stage: Literal[
    "fresh_overdue",
    "soft_collection",
    "hard_collection",
    "legal",
    "closed_repaid"
]
    interventions_used: int