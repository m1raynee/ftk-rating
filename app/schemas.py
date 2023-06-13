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
    default_score_type: ScoreTypeEnum


class GroupCreate(_BaseGroup):
    ...


class GroupOut(_BaseGroup, TimestampMixin):
    id: int


class GroupUpdate(Base):
    name: str
    teacher_id: int


class _BaseLesson(Base):
    group_id: int
    starts_at: datetime
    ends_at: datetime
    theme: str | None


class LessonCreate(_BaseLesson):
    ...


class LessonOut(_BaseLesson, CreatedAtMixin):
    id: int


class LessonUpdate(Base):
    group_id: int | None
    starts_at: datetime | None
    ends_at: datetime | None
    theme: str | None


class _BaseScoreEntry(Base):
    student_id: int
    judge_id: int
    lesson_id: int
    amount: int
    score_type: ScoreTypeEnum
    event_id: int


class ScoreEntryCreate(_BaseScoreEntry):
    ...


class ScoreEntryOut(_BaseScoreEntry, CreatedAtMixin):
    id: int


class ScoreEntryUpdate(Base):
    student_id: int | None
    judge_id: int | None
    lesson_id: int | None
    amount: int | None
    score_type: ScoreTypeEnum | None
    event_id: int | None
