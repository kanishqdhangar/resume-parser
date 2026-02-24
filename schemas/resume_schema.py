from pydantic import BaseModel
from typing import List, Optional

class Education(BaseModel):
    degree: Optional[str]
    institution: Optional[str]
    year: Optional[str]

class WorkExperience(BaseModel):
    title: str
    organization: str
    start_date: str
    end_date: str
    description: List[str]

class ResumeResponse(BaseModel):
    full_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    skills: List[str]
    education: List[Education]
    work_experience: List[WorkExperience]
    total_experience_years: Optional[float]