from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from sqlalchemy.sql import func
from .database import Base


class BorrowerRecord(Base):
    __tablename__ = "borrowers"

    id = Column(Integer, primary_key=True)
    borrower_id = Column(Integer)
    outstanding_balance = Column(Float)
    repayment_belief = Column(Float)
    workflow_stage = Column(String)


class DecisionLog(Base):
    __tablename__ = "decision_logs"
    id = Column(Integer, primary_key=True, index=True)
    borrower_id = Column(Integer, index=True)
    action = Column(String)
    risk_level = Column(String)
    repayment_belief = Column(Float)
    llm_reasoning = Column(String)
    decision_latency_ms = Column(Float)
    policy_version = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())