from typing import Type, Any
import typing as t

from fastapi import Depends, Query, HTTPException
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from fastapi_crudrouter.core._types import (
    DEPENDENCIES,
    PYDANTIC_SCHEMA as SCHEMA,
)
import sqlalchemy as sql

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta as Model
from sqlalchemy.exc import IntegrityError

SessionDependency = t.Callable[..., t.Generator[AsyncSession, t.Any, None]]

CALLABLE = t.Callable[..., t.Coroutine[Any, Any, Model]]
CALLABLE_LIST = t.Callable[..., t.Coroutine[Any, Any, list[Model]]]


class CRUDRouter(SQLAlchemyCRUDRouter):
    def __init__(
        self,
        schema: Type[SCHEMA],
        db_model: Model,
        db: SessionDependency,
        create_schema: Type[SCHEMA] | None = None,
        update_schema: Type[SCHEMA] | None = None,
        prefix: str | None = None,
        tags: list[str] | None = None,
        paginate: int | None = None,
        get_all_route: bool | DEPENDENCIES = True,
        get_one_route: bool | DEPENDENCIES = True,
        create_route: bool | DEPENDENCIES = True,
        update_route: bool | DEPENDENCIES = True,
        delete_one_route: bool | DEPENDENCIES = True,
        delete_all_route: bool | DEPENDENCIES = True,
        **kwargs: Any
    ) -> None:
        super().__init__(
            schema,
            db_model,
            db,
            create_schema,
            update_schema,
            prefix,
            tags,
            paginate,
            get_all_route,
            get_one_route,
            create_route,
            update_route,
            delete_one_route,
            delete_all_route,
            **kwargs
        )

    @property
    def pk_field(self):
        return getattr(self.db_model, self._pk)

    def _get_all(self, *args: Any, **kwargs: Any) -> CALLABLE_LIST:
        async def route(
            db: t.Annotated[AsyncSession, Depends(self.db_func)],
            skip: t.Annotated[int, Query(ge=0)] = 0,
            limit: t.Annotated[int, Query(gt=0, le=50)] = 20,
        ) -> list[Model]:
            db_models: list[Model] = await db.execute(
                sql.select(self.db_model)
                .order_by(self.pk_field)
                .limit(limit)
                .offset(skip)
            )
            return db_models

        return route

    def _get_one(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(
            item_id: self._pk_type, db: t.Annotated[AsyncSession, Depends(self.db_func)]  # type: ignore
        ) -> Model:
            model: Model = await db.execute(
                sql.select(self.db_model).where(self.pk_field == item_id)
            )

            if model:
                return model
            else:
                raise HTTPException(404, "Item not found") from None

        return route

    def _create(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(
            model: self.create_schema,  # type: ignore
            db: t.Annotated[AsyncSession, Depends(self.db_func)],
        ) -> Model:
            try:
                db_model = await db.execute(
                    sql.insert(self.db_model)
                    .values(**model.dict())
                    .returning(self.db_model)
                )
                return db_model
            except IntegrityError:
                db.rollback()
                raise HTTPException(422, "Key already exists") from None

        return route

    def _update(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(
            item_id: self._pk_type,  # type: ignore
            model: self.update_schema,  # type: ignore
            db: t.Annotated[AsyncSession, Depends(self.db_func)],
        ) -> Model:
            try:
                db_model: Model = await db.execute(
                    sql.update(self.db_model)
                    .where(self.pk_field == item_id)
                    .values(**model.dict(exclude_unset=True))
                    .returning(self.db_model)
                )

                return db_model
            except IntegrityError as e:
                db.rollback()
                self._raise(e)

        return route

    def _delete_all(self, *args: Any, **kwargs: Any) -> CALLABLE_LIST:
        async def route(
            db: t.Annotated[AsyncSession, Depends(self.db_func)]
        ) -> list[Model]:
            await db.execute(sql.delete(self.db_model))

            return self._get_all()(db=db, **{"skip": 0, "limit": None})

        return route

    def _delete_one(self, *args: Any, **kwargs: Any) -> CALLABLE:
        async def route(
            item_id: self._pk_type, db: t.Annotated[AsyncSession, Depends(self.db_func)]  # type: ignore
        ) -> Model:
            db_model: Model = await db.execute(
                sql.delete(self.db_model)
                .where(self.pk_field == item_id)
                .returning(self.db_model)
            )

            return db_model

        return route
