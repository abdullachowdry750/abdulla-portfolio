import sys
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.schemas import (
    Profile,
    Project,
    ProjectsResponse,
    HealthResponse,
)

# Connect the portfolio backend to the Enterprise Data Platform.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PLATFORM_ROOT = (
    PROJECT_ROOT / "projects" / "enterprise-data-platform"
)

sys.path.insert(0, str(DATA_PLATFORM_ROOT))

from src.analytics.customer_analytics import get_customer_analytics


app = FastAPI(
    title="Abdulla Engineering API",
    description="AI and Data Engineering Portfolio",
    version="1.0.0"
)

CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000"
    ).split(",")
    if origin.strip()
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["Content-Type", "Authorization"],
)

@app.get("/")
def home():
    return {
        "message": "Welcome to Abdulla's Engineering API",
        "status": "running"
    }


@app.get("/api/health")
def health():
    return {"status": "healthy"}


@app.get("/api/profile")
def get_profile():
    return {
        "name": "Abdulla Chowdry",
        "role": "AI & Data Engineer",
        "experience": "5+ years",
        "specialization": [
            "AI Engineering",
            "Data Engineering",
            "LLM Systems",
            "Cloud Architecture"
        ]
    }


@app.get("/api/projects")
def get_projects():
    return {
        "projects": [
            {
                "id": 1,
                "name": "Enterprise Data Platform",
                "category": "Data Engineering",
                "status": "In Development",
                "description": "Scalable data ingestion and orchestration platform.",
                "stack": [
                    "Python", "Airflow", "PostgreSQL", "ClickHouse"
                ]
            },
            {
                "id": 2,
                "name": "Enterprise RAG Platform",
                "category": "Applied AI",
                "status": "Planned",
                "description": "Enterprise knowledge retrieval using hybrid search.",
                "stack": [
                    "FastAPI", "Qdrant", "LLMs", "Python"
                ]
            },
            {
                "id": 3,
                "name": "ModelOps Platform",
                "category": "MLOps",
                "status": "Planned",
                "description": "End-to-end machine learning lifecycle management.",
                "stack": [
                    "MLflow", "Docker", "Python", "GCP"
                ]
            }
        ]
    }


@app.get("/api/analytics/customers")
def customer_analytics():
    try:
        return get_customer_analytics()

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Customer analytics are temporarily unavailable"
        ) from exc