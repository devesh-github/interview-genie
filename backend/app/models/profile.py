
from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(String(150))
    experience_years: Mapped[int] = mapped_column(Integer)
    target_company: Mapped[str] = mapped_column(String(150))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    skills: Mapped[list["Skill"]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
    )


class Skill(Base):
    __tablename__ = "skills"

    __table_args__ = (
        UniqueConstraint("profile_id", "name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    profile_id: Mapped[int] = mapped_column(
        ForeignKey("profiles.id"),
    )

    name: Mapped[str] = mapped_column(String(100))
    level: Mapped[str] = mapped_column(String(30))
    priority: Mapped[str] = mapped_column(String(30))

    profile: Mapped["Profile"] = relationship(
        back_populates="skills",
    )
