from typing import Dict, List

from pydantic import BaseModel

from src.models.job_profile import Skill


class ExperienceBulletPair(BaseModel):
    experience_id:str
    bullet_id: str

EvidenceMap = Dict[Skill,List[ExperienceBulletPair]]