from abc import ABC
from dataclasses import dataclass
from functools import singledispatchmethod
from types import get_original_bases
from typing import Generic, List, TypeVar, get_args
from uuid import UUID

from typeinspection import gethandledtypes


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

    def get_position(self, entity_id: UUID, event_type: str) -> int:
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
        return gethandledtypes(type(self.projection))


def test_projector_handles_projection_events():
    # Arrange
    expected = ["UserRegistered", "UserNameUpdated"]

    projection = UserDetailsProjection()

    projector = Projector(projection)

    # Act
    result = projector.handles

    # Assert
    assert result == expected
