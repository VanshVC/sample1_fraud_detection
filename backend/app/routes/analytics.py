from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.db import models
import os
import json

router = APIRouter()

# Paths
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
METRICS_PATH = os.path.join(BACKEND_DIR, "evaluation", "metrics.json")

@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    """
    Returns fraud statistics from the PostgreSQL database.
    """
    try:
        # Total transactions recorded
        total_transactions = db.query(models.Transaction).count()
        
        # Fraud cases (based on system predictions)
        fraud_count = db.query(models.Prediction).filter(models.Prediction.predicted_label == True).count()
        
        fraud_percentage = (fraud_count / total_transactions * 100) if total_transactions > 0 else 0
        
        # Average amount of transactions flagged as fraud
        avg_fraud_amount = db.query(func.avg(models.Transaction.amount))\
            .join(models.Prediction, models.Transaction.id == models.Prediction.transaction_id)\
            .filter(models.Prediction.predicted_label == True)\
            .scalar() or 0
            
        return {
            "total_transactions": total_transactions,
            "fraud_count": fraud_count,
            "fraud_percentage": round(fraud_percentage, 2),
            "avg_fraud_amount": round(float(avg_fraud_amount), 2)
        }
    except Exception as e:
        return {"error": str(e)}

@router.get("/model-metrics")
def get_model_metrics():
    """
    Returns the evaluation metrics (Precision, Recall, F1) from the latest training run.
    """
    try:
        if not os.path.exists(METRICS_PATH):
            return {"error": "Metrics not found. Run training first."}
            
        with open(METRICS_PATH, "r") as f:
            metrics = json.load(f)
        return metrics
    except Exception as e:
        return {"error": str(e)}
