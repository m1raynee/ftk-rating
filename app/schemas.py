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


class CreatedAtMixin(BaseModel):
    created_at: datetime


class TimestampMixin(CreatedAtMixin):
    updated_at: datetime

class _BaseStudent(BaseModel):
    firstname: str
    lastname: str

class StudentCreate(_BaseStudent): ...

class StudentOut(_BaseStudent, TimestampMixin):
    id: int

class StudentUpdate(BaseModel):
    firstname: str | None
    lastname: str | None