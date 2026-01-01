from typing import List

from pydantic import BaseModel, Field

class CategoryScore(BaseModel):
    category_name: str
    score: int = Field(description="score between 1 to 100")

class MatchResults(BaseModel):
    fit_score_overall :int = Field(description="fit score from 1 to 100")
    fit_score_by_category : List[CategoryScore]
    missing_keywords: List[str]
    evidence: str = Field(description="which bullets support which requirements")
#
#
# class BulletChange(BaseModel):
#     bullet_id: str
#     original_text: str
#     new_text: str
#     reason : str
#
#
# class OutPutReport(BaseModel):
#     tailored_resume: str = Field(description="the final resume content")
#     bullet_changes: List[BulletChange]
#     summary_of_changes: str
#     match_results : MatchResults


class OutPutReport(BaseModel):
    base_match_result: MatchResults
    final_match_result: MatchResults