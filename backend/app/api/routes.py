
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories import profile_repository as repo
from app.schemas.profile import (
    ProfileCreate,
    ProfileResponse,
    SkillCreate,
    SkillResponse,
)
from app.services import profile_service as service

router = APIRouter(prefix="/api")


@router.get("/profile", response_model=ProfileResponse)
def get_profile(db: Session = Depends(get_db)):
    return service.require_profile(db)


@router.put("/profile", response_model=ProfileResponse)
def save_profile(
    data: ProfileCreate,
    db: Session = Depends(get_db),
):
    return service.save_profile(db, data)


@router.get("/skills", response_model=list[SkillResponse])
def get_skills(db: Session = Depends(get_db)):
    profile = service.require_profile(db)
    return repo.list_skills(db, profile.id)


@router.post(
    "/skills",
    response_model=SkillResponse,
    status_code=201,
)
def add_skill(
    data: SkillCreate,
    db: Session = Depends(get_db),
):
    return service.add_skill(db, data)


@router.delete("/skills/{skill_id}", status_code=204)
def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
):
    service.remove_skill(db, skill_id)
