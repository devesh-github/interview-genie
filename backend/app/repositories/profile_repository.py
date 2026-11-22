
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.profile import Profile, Skill


def get_profile(db: Session):
    return db.scalar(
        select(Profile).order_by(Profile.id).limit(1)
    )


def create_profile(db: Session, data):
    profile = Profile(**data.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def update_profile(db: Session, profile: Profile, data):
    for key, value in data.model_dump().items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile


def list_skills(db: Session, profile_id: int):
    return db.scalars(
        select(Skill)
        .where(Skill.profile_id == profile_id)
        .order_by(Skill.id)
    ).all()


def create_skill(db: Session, profile_id: int, data):
    skill = Skill(
        profile_id=profile_id,
        **data.model_dump(),
    )
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


def get_skill(db: Session, skill_id: int):
    return db.get(Skill, skill_id)


def delete_skill(db: Session, skill: Skill):
    db.delete(skill)
    db.commit()
