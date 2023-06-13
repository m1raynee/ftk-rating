from fastapi import APIRouter, status, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
import sqlalchemy as sql

from ..database import ScoreEntry
from ..schemas import (
    ScoreEntryCreate,
    ScoreEntryOut,
    ScoreEntryUpdate,
)
from .. import dependencies as dep

# students/{student}/scores
student_router = APIRouter()


@student_router.get("/", response_model=Page[ScoreEntryOut])
async def get_all_student_scores(student: dep.exists.Student, db: dep.DB):
    return await paginate(
        db, sql.select(ScoreEntry).where(ScoreEntry.student_id == student)
    )


@student_router.get("/judged", response_model=Page[ScoreEntryOut])
async def get_all_student_judged_scores(student: dep.exists.Student, db: dep.DB):
    return await paginate(
        db, sql.select(ScoreEntry).where(ScoreEntry.judge_id == student)
    )


# groups/{group_id}/students/{student_id}/scores
