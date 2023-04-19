from typing import Annotated

from fastapi import Depends, HTTPException, status
import sqlalchemy as sql
from sqlalchemy.ext.asyncio import AsyncSession

from .database import session_factory, Student, Group


async def get_db():
    try:
        session = session_factory()
        yield session
        await session.commit()
    finally:
        await session.close()


DB = Annotated[AsyncSession, Depends(get_db)]


class _ModelDependency:
    async def get_student(student_id: int, db: DB):
        student = (
            await db.execute(sql.select(Student).where(Student.id == student_id))
        ).scalar()
        if student is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, "student with such id does not exists"
            )
        return student

    async def get_group(group_id: int, db: DB):
        group = (
            await db.execute(sql.select(Group).where(Group.id == group_id))
        ).scalar()
        if group is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, "group with such id does not exists"
            )
        return group

    Student = Annotated[Student, Depends(get_student)]
    Group = Annotated[Group, Depends(get_group)]


model = _ModelDependency()
