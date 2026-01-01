from typing import List

from pydantic import BaseModel, Field


class Responsibility(BaseModel):
    name : str = Field(description="the name of the responsibility")
    rank: int = Field(description="rank of the importance of the responsibility from 1-10 , 10 - most important")

class Skill(BaseModel):
    name: str = Field(description="the name of the skill")
    rank: int = Field(description="rank of the importance of the skill from 1-10 , 10 - most important")

class JobProfile(BaseModel):
    title: str
    company: str
    location: str
    responsibilities : List[Responsibility]
    must_haves: List[Skill]
    nice_to_haves: List[Skill]
    keywords: List[str]
    seniority_signals: List[str]
    domain_signals: List[str]