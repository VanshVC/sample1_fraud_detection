from fastapi import APIRouter, HTTPException
from app.api.schemas import TransactionBase, PredictionResponse
import joblib
import pandas as pd
import numpy as np
import os

router = APIRouter()

# Load Artifacts
BASE_ML_PATH = r"app/ml/models"

try:
    lr_model = joblib.load(os.path.join(BASE_ML_PATH, "logistic_regression.pkl"))
    rf_model = joblib.load(os.path.join(BASE_ML_PATH, "random_forest.pkl"))
    le_category = joblib.load(os.path.join(BASE_ML_PATH, "encoder_category.pkl"))
    le_location = joblib.load(os.path.join(BASE_ML_PATH, "encoder_location.pkl"))
    scaler = joblib.load(os.path.join(BASE_ML_PATH, "scaler.pkl"))
except Exception as e:
    print(f"⚠️ Warning: Model artifacts not found. Predictions will fail. {e}")
    lr_model = None
    rf_model = None


@router.post("/predict/lr", response_model=PredictionResponse)
def predict_logistic_regression(transaction: TransactionBase):
    if not lr_model:
        raise HTTPException(status_code=500, detail="LR Model not loaded")
    
    return _predict(transaction, lr_model, "Logistic Regression")

@router.post("/predict/rf", response_model=PredictionResponse)
def predict_random_forest(transaction: TransactionBase):
    if not rf_model:
        raise HTTPException(status_code=500, detail="RF Model not loaded")

    return _predict(transaction, rf_model, "Random Forest")

def _predict(transaction: TransactionBase, model, model_name: str):
    # 1. Prepare Data
    data = {
        'amount': [transaction.amount],
        'time': [transaction.time],
        'category': [transaction.category],
        'age': [transaction.age],
        'location': [transaction.location],
        'previous_trans': [transaction.previous_trans]
    }
    df = pd.DataFrame(data)

    # 2. Preprocess
    try:
        # Handle unseen labels by assigning a default or mode (simplest: try/except or rigorous mapping)
        # Here we just assume valid input for simplicity of the prototype
        if transaction.category in le_category.classes_:
             df['category'] = le_category.transform(df['category'])
        else:
             # Fallback for unknown category -> transform to most common or 0
             df['category'] = 0 
             
        if transaction.location in le_location.classes_:
            df['location'] = le_location.transform(df['location'])
        else:
            df['location'] = 0

        numerical_features = ['amount', 'time', 'age', 'previous_trans']
        df[numerical_features] = scaler.transform(df[numerical_features])
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Preprocessing error: {str(e)}")

    # 3. Predict
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1] # Probability of Class 1 (Fraud)

    return PredictionResponse(
        is_fraud=bool(prediction),
        probability=round(float(probability), 4),
        model_used=model_name
    )
