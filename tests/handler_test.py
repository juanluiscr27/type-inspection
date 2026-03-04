from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import singledispatchmethod
from typing import TypeVar
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


class Projection(ABC):  # noqa: B024
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


class Projector[TProjection]:
    def __init__(self, projection: TProjection) -> None:
        self.projection = projection

    @property
    def handles(self) -> list[str]:
        return get_handled_types(type(self.projection))


TEntity = TypeVar("TEntity")


class Repository[TEntity](ABC):  # noqa: B024
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
    def __init__(self, user_id: UserID, name: str) -> None:
        super().__init__()
        self.name: str = name


class Users(Repository[User]):
    """User Repository Interface"""

    @abstractmethod
    def save(self, user: User) -> int: ...

    @abstractmethod
    def find_by_id(self, user_id: UserID) -> UserID | None: ...

    @abstractmethod
    def find_by_slug(self, slug: str) -> UserID | None: ...

    @abstractmethod
    def find_all(self) -> list[User]: ...


class TestUsers(Users):
    """Test User Repository Implementation"""

    def save(self, user: User) -> int:
        pass

    def find_by_id(self, user_id: UserID) -> UserID | None:
        pass

    def find_by_slug(self, slug: str) -> UserID | None:
        pass

    def find_all(self) -> list[User]:
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
