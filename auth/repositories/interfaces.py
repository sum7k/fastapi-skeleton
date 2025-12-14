from abc import ABC, abstractmethod
from typing import Any, Generic, Protocol, TypeVar

T = TypeVar("T")
TDto = TypeVar("TDto")
TModel = TypeVar("TModel")


class IMapper(Protocol[TDto, TModel]):
    """Protocol for mappers between DTOs and ORM models."""

    def from_db(self, model: TModel) -> TDto: ...

    def to_db(self, dto: TDto) -> TModel: ...


class IRepository(ABC, Generic[T]):
    @abstractmethod
    async def list(self, skip: int, take: int) -> list[T]:
        pass

    @abstractmethod
    async def get(self, uid: int) -> T:
        pass

    @abstractmethod
    async def create(self, record: Any) -> T:
        pass

    @abstractmethod
    async def update(self, uid: Any, attrs: dict[str, Any]) -> T:
        pass

    @abstractmethod
    async def delete(self, uid: int) -> None:
        pass
