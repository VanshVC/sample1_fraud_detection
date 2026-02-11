from fastapi import FastAPI
from app.core.config import settings
from app.routes import predict, analytics, visualizations

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# Allow CORS
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

@app.get("/ping")
def health_check():
    return {"status": "pong"}
