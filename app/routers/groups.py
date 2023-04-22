from fastapi import APIRouter, status, HTTPException, Response
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
import sqlalchemy as sql

from ..database import Group, Student, students_groups_association, Lesson
from ..schemas import (
    GroupCreate,
    GroupOut,
    GroupUpdate,
    StudentOut,
    LessonCreate,
    LessonOut,
    LessonUpdate,
)
from .. import dependencies as dep

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("/", response_model=Page[GroupOut])
async def get_all_groups(db: dep.DB):
    return await paginate(db, sql.select(Group))


@router.post("/", response_model=GroupOut)
async def create_group(schema: GroupCreate, db: dep.DB):
    resp = await db.execute(sql.insert(Group).values(**schema.dict()).returning(Group))
    return resp.scalar()


@router.patch("/{group_id}", response_model=GroupOut)
async def update_group(group: dep.exists.Group, schema: GroupUpdate, db: dep.DB):
    resp = await db.execute(
        sql.update(Group)
        .where(Group.id == group)
        .values(**schema.dict(exclude_unset=True))
        .returning(Group)
    )
    return resp.scalar()


@router.get("/{group_id}/students", response_model=list[StudentOut])
async def get_group_students(group: dep.exists.Group, db: dep.DB):
    resp = await db.execute(
        sql.select(Student).where(Student.groups.any(Group.id == group))
    )
    return resp.scalars().all()


@router.put("/{group_id}/students/{student_id}")
async def add_student_to_group(
    group: dep.exists.Group, student: dep.exists.Student, db: dep.DB
):
    if await db.execute(
        sql.select(Student)
        .where(Student.groups.any(Group.id == group))
        .where(Student.id == student)
    ):
        return Response(
            {"detail": "Student already in the group"},
            status.HTTP_204_NO_CONTENT,
        )

    await db.execute(
        sql.insert(students_groups_association).values(
            group_id=group, student_id=student
        )
    )
    return Response(
        {"detail": "Student added to the group"},
        status.HTTP_201_CREATED,
    )


@router.get("/{group_id}/lessons", response_model=Page[LessonOut])
async def get_all_group_lessons(group: dep.exists.Group, db: dep.DB):
    return paginate(db, sql.select(Lesson).where(Lesson.group_id == group))


@router.post("/{group_id}/lessons", response_model=LessonOut)
async def create_group_lesson(
    group: dep.exists.Group, schema: LessonCreate, db: dep.DB
):
    resp = await db.execute(
        sql.insert(Lesson).values(**schema.dict(), group_id=group).returning(Lesson)
    )
    return resp.scalar()


@router.patch("/{group_id}/lessons/{lesson_id}", response_model=LessonOut)
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
