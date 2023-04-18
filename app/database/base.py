from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


engine = create_async_engine(
    "postgresql+asyncpg://ftk:secret@localhost:5432/ftk-data", echo=True
)  # TODO: env variable
session_factory = async_sessionmaker(engine, expire_on_commit=False)
