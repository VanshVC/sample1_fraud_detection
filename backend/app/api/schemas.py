from pydantic import BaseModel
from typing import Literal

class TransactionBase(BaseModel):
    amount: float
    time: int
    category: str
    age: int
    location: str
    previous_trans: int

class PredictionResponse(BaseModel):
    is_fraud: bool
    probability: float
    model_used: str
