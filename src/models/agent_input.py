from pydantic import BaseModel

from src.models.job_profile import JobProfile
from src.models.resume_profile import ResumeProfile


class JobAndResume(BaseModel):
    job_profile: JobProfile
    resume_profile: ResumeProfile
