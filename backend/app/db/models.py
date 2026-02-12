from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    time = Column(Integer, nullable=False) # Step of the simulation
    category = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
    previous_trans = Column(Integer, nullable=False)
    is_fraud = Column(Boolean, default=False) # Ground truth
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    predictions = relationship("Prediction", back_populates="transaction")

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"))
    predicted_label = Column(Boolean, nullable=False) # 0 or 1
    probability = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    transaction = relationship("Transaction", back_populates="predictions")

class ModelMetrics(Base):
    __tablename__ = "model_metrics"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, nullable=False)
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
