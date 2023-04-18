from . import students

from fastapi import APIRouter

router = APIRouter()
router.include_router(students.router)
