from . import students, groups

from fastapi import APIRouter

router = APIRouter()
router.include_router(students.router)
router.include_router(groups.router)
