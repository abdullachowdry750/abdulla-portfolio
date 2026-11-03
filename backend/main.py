
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import Profile, Project, ProjectsResponse, HealthResponse

app = FastAPI(
    title="Abdulla Engineering API",
    description="AI and Data Engineering Portfolio",
    version="1.0.0"
)

# Frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
