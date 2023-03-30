from typing import Any, Optional, Dict, Generic, Type, TypeVar
from fastapi import HTTPException, status

from project.models.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)


class NotFoundException(HTTPException, Generic[ModelType]):
    def __init__(
        self,
        model: Type[ModelType],
        id: int,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__name__} with id {id} not found.",
        )
