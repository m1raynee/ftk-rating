from fastapi import APIRouter, status, Response
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
import sqlalchemy as sql

from ..database import Group, Student, students_groups_association
from ..schemas import (
    GroupCreate,
    GroupOut,
    GroupUpdate,
    StudentOut,
)
from .. import dependencies as dep
from . import lessons

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("/", response_model=Page[GroupOut])
async def get_all_groups(db: dep.DB):
    return await paginate(db, sql.select(Group))


@router.post("/", response_model=GroupOut)
async def create_group(schema: GroupCreate, db: dep.DB):
    resp = await db.execute(sql.insert(Group).values(**schema.dict()).returning(Group))
    return resp.scalar()


group_router = APIRouter()


@group_router.patch("/", response_model=GroupOut)
async def update_group(group: dep.exists.Group, schema: GroupUpdate, db: dep.DB):
    resp = await db.execute(
        sql.update(Group)
        .where(Group.id == group)
        .values(**schema.dict(exclude_unset=True))
        .returning(Group)
    )
    return resp.scalar()


@group_router.get("/students", response_model=list[StudentOut])
async def get_group_students(group: dep.exists.Group, db: dep.DB):
    resp = await db.execute(
        sql.select(Student).where(Student.groups.any(Group.id == group))
    )
    return resp.scalars().all()


@group_router.put("/students/{student_id}")
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


group_router.include_router(lessons.router, prefix="/lessons", tags=["lessons"])
router.include_router(group_router, prefix="/{group_id}")
