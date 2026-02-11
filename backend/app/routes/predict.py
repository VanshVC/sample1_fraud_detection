from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.ml.inference import ModelInference
from app.api.schemas import TransactionBase, PredictionResponse
from app.db.database import get_db
from app.db.models import Transaction, Prediction

router = APIRouter()
inference = ModelInference()

@router.post("/predict", response_model=PredictionResponse)
def predict(transaction: TransactionBase, model: str = "rf", db: Session = Depends(get_db)):
    """
    Predicts fraud probability and saves the transaction to the database.
    - **model**: 'rf' (Random Forest - Default) or 'lr' (Logistic Regression)
    """
    try:
        # 1. Run Inference
        data = transaction.dict() 
        result = inference.predict(data, model_type=model)
        
        # 2. Save to Database
        # Save Transaction
        db_transaction = Transaction(
            amount=transaction.amount,
            time=transaction.time,
            category=transaction.category,
            age=transaction.age,
            location=transaction.location,
            previous_trans=transaction.previous_trans
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        
        # Save Prediction
        db_prediction = Prediction(
            transaction_id=db_transaction.id,
            is_fraud=result["is_fraud"],
            probability=result["probability"],
            model_used=result["model_used"]
        )
        db.add(db_prediction)
        db.commit()
        
        return PredictionResponse(
            is_fraud=result["is_fraud"],
            probability=result["probability"],
            model_used=result["model_used"]
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
