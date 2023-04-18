from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .database import session_factory


async def get_db():
    try:
        session = session_factory()
        yield session
    finally:
        await session.commit()
        await session.close()

DB = Annotated[AsyncSession, Depends(get_db)]
