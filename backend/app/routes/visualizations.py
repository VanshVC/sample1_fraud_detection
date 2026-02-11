from fastapi import APIRouter
import pandas as pd
import numpy as np
import joblib
import os
import json

router = APIRouter()

# Paths
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BACKEND_DIR, "data", "credit_card_fraud.csv")
MODELS_DIR = os.path.join(BACKEND_DIR, "models")
METRICS_PATH = os.path.join(BACKEND_DIR, "evaluation", "metrics.json")
RF_MODEL_PATH = os.path.join(MODELS_DIR, "random_forest.pkl")

@router.get("/visualizations/feature-importance")
def get_feature_importance():
    """
    Returns feature importance from the Random Forest model.
    """
    try:
        model = joblib.load(RF_MODEL_PATH)
        # Feature names corresponding to the training columns
        features = ['amount', 'time', 'category', 'age', 'location', 'previous_trans']
        
        if not hasattr(model, 'feature_importances_'):
            return {"error": "Model does not support feature importance."}
            
        importances = model.feature_importances_
        # Sort by importance
        indices = np.argsort(importances)[::-1]
        
        feature_importance = []
        for i in range(len(features)):
            feature_importance.append({
                "feature": features[indices[i]],
                "importance": round(float(importances[indices[i]]), 4)
            })
            
        return feature_importance
    except Exception as e:
        return {"error": str(e)}

@router.get("/visualizations/fraud-distribution")
def get_fraud_distribution():
    """
    Returns data for Fraud vs Legitimate distribution pie/bar chart.
    """
    try:
        df = pd.read_csv(DATA_PATH)
        counts = df['is_fraud'].value_counts().to_dict()
        return [
            {"name": "Legitimate", "value": counts.get(0, 0)},
            {"name": "Fraud", "value": counts.get(1, 0)}
        ]
    except Exception as e:
        return {"error": str(e)}

@router.get("/visualizations/amount-vs-fraud")
def get_amount_vs_fraud():
    """
    Returns binning data for transaction amounts split by fraud status.
    """
    try:
        df = pd.read_csv(DATA_PATH)
        
        # Bin amounts into ranges
        bins = [0, 50, 100, 200, 500, 1000, 5000, 10000]
        labels = ['0-50', '50-100', '100-200', '200-500', '500-1k', '1k-5k', '5k+']
        
        df['amount_bin'] = pd.cut(df['amount'], bins=bins, labels=labels)
        
        # Group by bin and fraud status
        grouped = df.groupby(['amount_bin', 'is_fraud'], observed=False).size().unstack(fill_value=0)
        
        data = []
        for bin_label in labels:
            if bin_label in grouped.index:
                data.append({
                    "range": bin_label,
                    "legitimate": int(grouped.loc[bin_label, 0]),
                    "fraud": int(grouped.loc[bin_label, 1])
                })
            else:
                data.append({"range": bin_label, "legitimate": 0, "fraud": 0})
                
        return data
    except Exception as e:
        return {"error": str(e)}
