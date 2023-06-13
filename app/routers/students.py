from fastapi import APIRouter
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
import sqlalchemy as sql

from ..database import Student
from ..schemas import StudentCreate, StudentOut, StudentUpdate
from .. import dependencies as dep
from . import scores

router = APIRouter(prefix="/students", tags=["students"])


@router.get("/", response_model=Page[StudentOut])
async def get_all_students(db: dep.DB):
    return await paginate(db, sql.select(Student))


@router.post("/", response_model=StudentOut)
async def create_student(schema: StudentCreate, db: dep.DB):
    resp = await db.execute(
        sql.insert(Student).values(**schema.dict()).returning(Student)
    )
    return resp.scalar()


@router.patch("/{student_id}", response_model=StudentOut)
async def update_student(
    student: dep.exists.Student, schema: StudentUpdate, db: dep.DB
):
    resp = await db.execute(
        sql.update(Student)
        .where(Student.id == student)
        .values(**schema.dict(exclude_unset=True), updated_at=sql.func.now())
        .returning(Student)
    )
    return resp.scalar()


router.include_router(scores.student_router, prefix="/{student_id}/scores")
