from fastapi import FastAPI
from app.core.config import settings
from app.routes import predict, analytics, visualizations

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

from fastapi.middleware.cors import CORSMiddleware



# Allow all Vercel and Render subdomains, plus localhost
origin_regex = r"https?://(localhost|.*\.vercel\.app|.*\.onrender\.com)(:\d+)?"

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=origin_regex,
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
