from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar, List

Model = TypeVar("Model")
CreateSchema = TypeVar("CreateSchema")
UpdateSchema = TypeVar("UpdateSchema")


class BaseCRUD(ABC, Generic[Model, CreateSchema, UpdateSchema]):
    """
    Generic CRUD Factory

    Implementation Example
    -------
    OrderCRUD(BaseCRUD[Order, OrderCreate, OrderUpdate])
    * All BaseCrud parameters are schemas created for the object/table
    """

    @abstractmethod
    async def create(self, data: CreateSchema) -> Model:
        ...

    # Just a general getter using an id
    @abstractmethod
    async def read(self, unique_id: int) -> Optional[Model]:
        ...

    # group_id limits results to a subsection of the data
    # This could be split into separate methods for a cleaner class
    @abstractmethod
    async def read_many(self, offset: int, limit: int, group_id: Optional[int]) -> List[Model]:
        ...

    @abstractmethod
    async def update(self, unique_id: int, data: UpdateSchema) -> Model:
        ...

    @abstractmethod
    async def delete(self, unique_id: int) -> None:
        ...
