from __future__ import annotations

from datetime import datetime

import sqlalchemy as sql
from sqlalchemy import orm

from ..utils import parse_tablename
from ..schemas import ScoreTypeEnum


class Base(orm.DeclarativeBase):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    @orm.declared_attr.directive
    def __tablename__(cls) -> str:
        return parse_tablename(cls.__name__)


class CreatedAtMixin:
    created_at: orm.Mapped[datetime] = orm.mapped_column(server_default=sql.func.now())


class TimestampMixin(CreatedAtMixin):
    updated_at: orm.Mapped[datetime] = orm.mapped_column(server_default=sql.func.now())


students_groups_association = sql.Table(
    "students_to_groups",
    Base.metadata,
    sql.Column("group_id", sql.ForeignKey("groups.id"), primary_key=True),
    sql.Column("student_id", sql.ForeignKey("students.id"), primary_key=True),
)


class Group(Base, TimestampMixin):
    name: orm.Mapped[str]
    teacher_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("students.id"))
    default_score_type: orm.Mapped[ScoreTypeEnum | None]

    teacher: orm.Mapped[Student] = orm.relationship(back_populates="teaching_groups")
    students: orm.Mapped[list[Student]] = orm.relationship(
        secondary=students_groups_association, back_populates="groups"
    )
    lessons: orm.Mapped[list[Lesson]] = orm.relationship(back_populates="group")


class Lesson(Base, CreatedAtMixin):
    group_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("groups.id"))
    starts_at: orm.Mapped[datetime]
    ends_at: orm.Mapped[datetime]
    theme: orm.Mapped[str | None]

    group: orm.Mapped[Group] = orm.relationship(back_populates="lessons")
    scores: orm.Mapped[list[ScoreEntry]] = orm.relationship(back_populates="lesson")


class ScoreEntry(Base, CreatedAtMixin):
    student_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("students.id"))
    judge_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("students.id"))
    lesson_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("lessons.id"))
    amount: orm.Mapped[int]
    score_type: orm.Mapped[ScoreTypeEnum]
    event_id: orm.Mapped[int | None] = orm.mapped_column(sql.ForeignKey("events.id"))

    judge: orm.Mapped[Student] = orm.relationship(
        back_populates="judged_scores", foreign_keys=[judge_id]
    )
    student: orm.Mapped[Student] = orm.relationship(
        back_populates="scores", foreign_keys=[student_id]
    )
    lesson: orm.Mapped[Lesson] = orm.relationship(back_populates="scores")
    event: orm.Mapped[Event | None] = orm.relationship(back_populates="scores")


class Event(Base):
    comment: orm.Mapped[str]
    base_amount: orm.Mapped[int | None]

    scores: orm.Mapped[list[ScoreEntry]] = orm.relationship(back_populates="event")


class Student(Base, TimestampMixin):
    firstname: orm.Mapped[str]
    lastname: orm.Mapped[str]

    scores: orm.Mapped[list[ScoreEntry]] = orm.relationship(
        back_populates="student", foreign_keys=[ScoreEntry.student_id]
    )
    judged_scores: orm.Mapped[list[ScoreEntry]] = orm.relationship(
        back_populates="judge", foreign_keys=[ScoreEntry.judge_id]
    )
    teaching_groups: orm.Mapped[list[Group]] = orm.relationship(
        back_populates="teacher"
    )
    groups: orm.Mapped[list[Group]] = orm.relationship(
        secondary=students_groups_association, back_populates="students"
    )
