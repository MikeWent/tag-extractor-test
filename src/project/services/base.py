from typing import Any, Dict, Generic, List, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from project.exceptions.common import NotFoundException
from project.models.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    model: Type[ModelType]

    def __init__(self, db: AsyncSession):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.db: AsyncSession = db

    async def get(self, id: Any) -> ModelType:
        results = await self.db.scalars(select(self.model).where(self.model.id == id))
        result = results.one_or_none()
        if not result:
            raise NotFoundException(model=self.model, id=id)
        return result

    async def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        results = await self.db.scalars(select(self.model).offset(skip).limit(limit))
        return results.all()

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(
        self, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def remove(self, *, db_obj: ModelType) -> int:
        await self.db.delete(db_obj)
        await self.db.commit()
        return db_obj.id
