from typing import List, Dict, Literal
from datetime import datetime
from pydantic import BaseModel, Field


class Project(BaseModel):
    name :str
    technologies: List[str]
    description: str

class Education(BaseModel):
    school_name: str
    degree: str


class Bullet(BaseModel):
    id: str
    content: str

class JobExperience(BaseModel):
    id :str
    company: str
    role: str
    start_date: datetime
    end_date: datetime
    bullets: List[Bullet]
    technologies: List[str]


class ResumeProfile(BaseModel):
    contact : str
    summary: str = None
    skills: List[str]
    experiences: List[JobExperience]
    projects: List[Project]
    education :Education









