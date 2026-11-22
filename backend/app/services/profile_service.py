
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories import profile_repository as repo


def save_profile(db: Session, data):
    existing = repo.get_profile(db)

    if existing:
        return repo.update_profile(db, existing, data)

    return repo.create_profile(db, data)


def require_profile(db: Session):
    profile = repo.get_profile(db)

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Create your profile first",
        )

    return profile


def add_skill(db: Session, data):
    profile = require_profile(db)

    try:
        return repo.create_skill(db, profile.id, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Skill already exists",
        )


def remove_skill(db: Session, skill_id: int):
    profile = require_profile(db)
    skill = repo.get_skill(db, skill_id)

    if not skill or skill.profile_id != profile.id:
        raise HTTPException(
            status_code=404,
            detail="Skill not found",
        )

    repo.delete_skill(db, skill)
