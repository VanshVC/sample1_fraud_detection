from fastapi import FastAPI
from app.core.config import settings
from app.routes import predict, analytics, visualizations

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

from fastapi.middleware.cors import CORSMiddleware


origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "https://sample1-fraud-detection.vercel.app",
    "https://sample1-fraud-detection-1.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(predict.router, prefix="/api", tags=["Prediction"])
app.include_router(analytics.router, prefix="/api", tags=["Analytics"])
app.include_router(visualizations.router, prefix="/api", tags=["Visualizations"])

# Create Database Tables
from app.db.database import engine, Base
from app.db import models
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Fraud Detection API is running", "health": "ok"}

@app.get("/ping")
def health_check():
    return {"status": "pong"}
