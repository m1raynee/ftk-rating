from enum import Enum
from datetime import datetime

from pydantic import BaseModel


class ScoreTypeEnum(Enum):
    robotics = "robotics"
    electrics = "electrics"
    needlework = "needlework"
    intellect = "intellect"
    architecture = "architecture"
    games = "games"
    newspaper = "newspaper"
    hikes = "hikes"
    competition_town = "competition_town"
    competitions = "competitions"


class Base(BaseModel):
    class Config:
        orm_mode = True


class CreatedAtMixin(Base):
    created_at: datetime


class TimestampMixin(CreatedAtMixin):
    updated_at: datetime


class _BaseStudent(Base):
    firstname: str
    lastname: str


class StudentCreate(_BaseStudent):
    ...


class StudentOut(_BaseStudent, TimestampMixin):
    id: int


class StudentUpdate(Base):
    firstname: str | None
    lastname: str | None


class _BaseGroup(Base):
    name: str
    teacher_id: int


class GroupCreate(_BaseGroup):
    ...


class GroupOut(_BaseGroup, TimestampMixin):
    id: int


class GroupUpdate(Base):
    name: str
    teacher_id: int
