from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import singledispatchmethod
from typing import Generic, List, TypeVar, Optional
from uuid import UUID

from typeinspection import get_handled_types
from typeinspection.handlers import get_super_name


@dataclass(frozen=True)
class DomainEvent:
    pass


@dataclass(frozen=True)
class UserRegistered(DomainEvent):
    user_id: int
    name: str
    slug: str


@dataclass(frozen=True)
class UserNameUpdated(DomainEvent):
    user_id: int
    new_name: str
    previous_name: str


class Projection(ABC):
    pass


class UserDetailsProjection(Projection):

    # noinspection PyMethodMayBeStatic
    def get_position(self, _: UUID, __: str) -> int:
        return 1

    def update_position(self, entity_id: UUID, event_type: str, position: int) -> None:
        pass

    @singledispatchmethod
    def apply(self, event: DomainEvent) -> None:
        pass

    @apply.register
    def _when(self, event: UserRegistered) -> None:
        pass

    @apply.register
    def _when(self, event: UserNameUpdated) -> None:
        pass


TProjection = TypeVar("TProjection", bound=Projection)


class Projector(Generic[TProjection]):

    def __init__(self, projection: TProjection):
        self.projection = projection

    @property
    def handles(self) -> List[str]:
        return get_handled_types(type(self.projection))


TEntity = TypeVar("TEntity")


class Repository(ABC, Generic[TEntity]):
    """Repository Generic Abstract Base class

    The Repository Interface defines the operations on an entity of type `TEntity`.
    """

    @property
    def aggregate_type(self) -> str:
        """Returns the qualified name of the entity this repository is based on"""
        return get_super_name(self)


@dataclass(frozen=True)
class UserID:
    value: int


class User:

    def __init__(self, user_id: UserID, name):
        super().__init__(user_id, 0)
        self.name: str = name


class Users(Repository[User]):
    """User Repository Interface"""

    @abstractmethod
    def save(self, user: User) -> int:
        ...

    @abstractmethod
    def find_by_id(self, user_id: UserID) -> Optional[UserID]:
        ...

    @abstractmethod
    def find_by_slug(self, slug: str) -> Optional[UserID]:
        ...

    @abstractmethod
    def find_all(self) -> List[User]:
        ...


class TestUsers(Users):
    """Test User Repository Implementation"""

    def save(self, user: User) -> int:
        pass

    def find_by_id(self, user_id: UserID) -> Optional[UserID]:
        pass

    def find_by_slug(self, slug: str) -> Optional[UserID]:
        pass

    def find_all(self) -> List[User]:
        pass


def test_projector_handles_projection_events():
    # Arrange
    expected = ["UserRegistered", "UserNameUpdated"]

    projection = UserDetailsProjection()

    projector = Projector(projection)

    # Act
    result = projector.handles

    # Assert
    assert result == expected


def test_repository_with_aggregates():
    # Arrange
    expected = "User"

    # Act
    users = TestUsers()

    # Assert
    assert users.aggregate_type == expected
