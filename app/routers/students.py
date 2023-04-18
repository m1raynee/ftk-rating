from fastapi import APIRouter

from .base import CRUDRouter
from ..database import Student
from ..schemas import StudentCreate, StudentOut, StudentUpdate
from ..dependencies import get_db

router = APIRouter(prefix="/students")
crud = CRUDRouter(
    StudentOut,
    Student,
    get_db,
    StudentCreate,
    StudentUpdate,
    tags=["students"],
    delete_all_route=False,
)
router.include_router(crud)
