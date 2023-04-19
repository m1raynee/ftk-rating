from fastapi import APIRouter
from fastapi_pagination import Page, LimitOffsetPage
from fastapi_pagination.ext.async_sqlalchemy import paginate
import sqlalchemy as sql

from ..database import Student
from ..schemas import StudentCreate, StudentOut, StudentUpdate
from .. import dependencies as dep

router = APIRouter(prefix="/students")


@router.get("/", response_model=Page[StudentOut])
@router.get("/limit-offset", response_model=LimitOffsetPage[StudentOut])
async def get_all_students(db: dep.DB):
    return await paginate(db, sql.select(Student), params=params)


@router.post("/", response_model=StudentOut)
async def create_student(schema: StudentCreate, db: dep.DB):
    resp = await db.execute(
        sql.insert(Student).values(**schema.dict()).returning(Student)
    )
    return resp.scalar()


@router.patch("/{student_id}", response_model=StudentOut)
async def update_student(student_id: int, schema: StudentUpdate, db: dep.DB):
    resp = await db.execute(
        sql.update(Student)
        .where(Student.id == student_id)
        .values(**schema.dict(exclude_unset=True))
        .returning(Student)
    )
    return resp.scalar()
