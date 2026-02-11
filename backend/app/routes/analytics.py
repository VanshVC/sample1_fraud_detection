from fastapi import APIRouter
import pandas as pd
import os
import json

router = APIRouter()

# Paths (Ideally from config)
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BACKEND_DIR, "data", "credit_card_fraud.csv")
METRICS_PATH = os.path.join(BACKEND_DIR, "evaluation", "metrics.json")

@router.get("/analytics")
def get_analytics():
    """
    Returns basic fraud statistics from the dataset.
    """
    try:
        if not os.path.exists(DATA_PATH):
             return {"error": "Data file not found."}
             
        df = pd.read_csv(DATA_PATH)
        total_transactions = len(df)
        fraud_cases = df[df['is_fraud'] == 1]
        fraud_count = len(fraud_cases)
        fraud_percentage = (fraud_count / total_transactions) * 100
        
        avg_fraud_amount = fraud_cases['amount'].mean() if fraud_count > 0 else 0
        
        return {
            "total_transactions": total_transactions,
            "fraud_count": fraud_count,
            "fraud_percentage": round(fraud_percentage, 2),
            "avg_fraud_amount": round(avg_fraud_amount, 2)
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
