from typing import Any, Generic, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.interfaces import IMapper, IRepository

TDto = TypeVar("TDto")
TModel = TypeVar("TModel")


class Repository(IRepository[TDto], Generic[TDto, TModel]):
    """Generic repository implementation for CRUD operations."""

    def __init__(
        self,
        session: AsyncSession,
        model_class: Type[TModel],
        mapper: IMapper,
    ):
        self.session = session
        self._model_class = model_class
        self.mapper = mapper

    async def list(self, skip: int, take: int) -> list[TDto]:
        result = await self.session.execute(
            select(self._model_class).offset(skip).limit(take)
        )
        return [self.mapper.from_db(r) for r in result.scalars().all()]

    async def get(self, uid: Any) -> TDto:
        try:
            entity = await self._get(uid)
        except NoResultFound:
            raise ValueError(f"No {self._model_class.__name__} found with id:{uid}")
        return self.mapper.from_db(entity)  # type: ignore[no-any-return]

    async def create(self, record: Any) -> TDto:
        """Create a new entity from a Create DTO.

        Args:
            record: Create DTO (e.g., CreateUserDTO, CreateTokenDTO)

        Returns:
            Full DTO of the created entity
        """
        entity = self.mapper.to_db_new(record)
        self.session.add(entity)
        await self.session.flush()  # Flush to get the ID
        await self.session.refresh(entity)
        created_dto = self.mapper.from_db(entity)
        return created_dto  # type: ignore[no-any-return]

    async def update(self, uid: Any, attrs: dict[str, Any]) -> TDto:
        try:
            entity = await self._get(uid)
        except NoResultFound:
            raise ValueError(f"{self._model_class.__name__} not found.")

        for key, value in attrs.items():
            if hasattr(entity, key):  # Only update fields that exist on ORM
                setattr(entity, key, value)

        await self.session.flush()
        await self.session.refresh(entity)
        return self.mapper.from_db(entity)  # type: ignore[no-any-return]

    async def delete(self, uid: int) -> None:
        try:
            entity = await self._get(uid)
        except NoResultFound:
            return  # No-op if record doesn't exist

        await self.session.delete(entity)
        await self.session.flush()

    async def _get(self, entity_id: Any) -> TModel:
        result = await self.session.execute(
            select(self._model_class).where(self._model_class.id == entity_id)  # type: ignore
        )
        one: TModel = result.scalar_one()
        return one
