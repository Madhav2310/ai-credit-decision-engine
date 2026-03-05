from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
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

    id = Column(Integer, primary_key=True)
    borrower_id = Column(Integer)
    action = Column(String)
    belief = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)