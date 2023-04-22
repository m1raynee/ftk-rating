from fastapi import APIRouter, status, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
import sqlalchemy as sql

from ..database import Lesson
from ..schemas import (
    LessonCreate,
    LessonOut,
    LessonUpdate,
)
from .. import dependencies as dep

router = APIRouter()


@router.get("/", response_model=Page[LessonOut])
async def get_all_group_lessons(group: dep.exists.Group, db: dep.DB):
    return paginate(db, sql.select(Lesson).where(Lesson.group_id == group))


@router.post("/", response_model=LessonOut)
async def create_group_lesson(
    group: dep.exists.Group, schema: LessonCreate, db: dep.DB
):
    resp = await db.execute(
        sql.insert(Lesson).values(**schema.dict(), group_id=group).returning(Lesson)
    )
    return resp.scalar()


@router.patch("/{lesson_id}", response_model=LessonOut)
async def update_group_lesson(
    group: dep.exists.Group, lesson: dep.exists.Lesson, schema: LessonUpdate, db: dep.DB
):
    new_lesson = (
        await db.execute(
            sql.update(Lesson)
            .where(Lesson.group_id == group & Lesson.id == lesson)
            .values(**schema.dict())
            .returning(Lesson)
        )
    ).scalar()
    if new_lesson is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "lesson with such id does not exists in this group",
        )
    return new_lesson
