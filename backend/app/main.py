from fastapi import FastAPI
from app.core.config import settings
from app.routes import predict, analytics, visualizations

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# Allow CORS
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request, Response

@app.middleware("http")
async def add_cors_private_network_header(request: Request, call_next):
    if request.method == "OPTIONS":
        if "access-control-request-private-network" in request.headers:
            response = Response()
            response.headers["Access-Control-Allow-Origin"] = request.headers.get("origin", "*")
            response.headers["Access-Control-Allow-Private-Network"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "*"
            response.headers["Access-Control-Allow-Headers"] = "*"
            return response
    
    response = await call_next(request)
    # Add Private Network Access support for the actual response
    response.headers["Access-Control-Allow-Private-Network"] = "true"
    return response

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

@app.get("/")
def read_root():
    return {"message": "Fraud Detection API is running", "health": "ok"}

@app.get("/ping")
def health_check():
    return {"status": "pong"}
