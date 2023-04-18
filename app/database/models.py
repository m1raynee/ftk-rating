from __future__ import annotations

from datetime import datetime

import sqlalchemy as sql
from sqlalchemy import orm

from utils import parse_tablename
from schemas import ScoreTypeEnum


class Base(orm.DeclarativeBase):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    @orm.declared_attr.directive
    def __tablename__(cls) -> str:
        return parse_tablename(cls.__name__)


class CreatedAtMixin:
    created_at: orm.Mapped[datetime] = orm.mapped_column(server_default=sql.func.now())


class TimestampMixin(CreatedAtMixin):
    updated_at: orm.Mapped[datetime] = orm.mapped_column(server_default=sql.func.now())


class Group(Base, TimestampMixin):
    name: orm.Mapped[str]
    teacher_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("students.id"))

    teacher: orm.Mapped[Student] = orm.relationship(back_populates="teaching_groups")


# class Lesson(Base, TimestampMixin):
#     ...


class ScoreEntry(Base, CreatedAtMixin):
    student_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("students.id"))
    judge_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("students.id"))
    amount: orm.Mapped[int]
    score_type: orm.Mapped[ScoreTypeEnum]
    comment_id: orm.Mapped[int | None]

    judge: orm.Mapped[Student] = orm.relationship(
        back_populates="judged_scores", foreign_keys=[judge_id]
    )
    student: orm.Mapped[Student] = orm.relationship(
        back_populates="scores", foreign_keys=[student_id]
    )
    comment: orm.Mapped[Comment | None] = orm.relationship(back_populates="scores")


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


class Comment(Base):
    comment: orm.Mapped[str]
    base_amount: orm.Mapped[int | None]
