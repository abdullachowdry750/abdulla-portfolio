
from pydantic import BaseModel
from typing import List


class Profile(BaseModel):
    name: str
    role: str
    experience: str
    specialization: List[str]


class Project(BaseModel):
    id: int
    name: str
    category: str
    status: str
    description: str
    stack: List[str]


class ProjectsResponse(BaseModel):
    projects: List[Project]


class HealthResponse(BaseModel):
    status: str