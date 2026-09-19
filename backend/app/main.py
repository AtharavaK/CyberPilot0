from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.db.database import init_db

app = FastAPI(
    title="CyberPilot API",
    description="Agentic AI Platform for Autonomous Security Assessment",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    init_db()

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the CyberPilot API Gateway"}
