from typing import List, Literal

from pydantic import BaseModel, Field

class BulletInstruction(BaseModel):
    bullet_id: str
    action : Literal['keep','rewrite','emphasize','de-emphasize','remove']
    reason: str
    focus_tags : List[str]
    priority: Literal['high','medium','low']

class PerExperience(BaseModel):
    experience_id: str
    bullets_instructions: List[BulletInstruction]

class TailoringPlan(BaseModel):
    target_role : str
    company: str
    per_experience: List[BulletInstruction]
    tailoring_aggressiveness: Literal["light","medium","heavy"]
    constrains: List[str]