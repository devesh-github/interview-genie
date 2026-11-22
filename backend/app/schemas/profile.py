
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ProfileCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    role: str = Field(min_length=1, max_length=150)
    experience_years: int = Field(ge=0, le=60)
    target_company: str = Field(min_length=1, max_length=150)


class ProfileResponse(ProfileCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SkillCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    level: Literal["Beginner", "Intermediate", "Advanced"]
    priority: Literal["Low", "Medium", "High"]


class SkillResponse(SkillCreate):
    id: int
    profile_id: int

    model_config = ConfigDict(from_attributes=True)
