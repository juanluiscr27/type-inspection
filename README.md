# Type Inspection

Extract type information from classes implementations derived from generic abstract base classes using AST introspection. Designed for **Domain-Driven Design** applications, ideal for getting the types handled by a projections or event handlers in event sourcing patterns.



## Overview

`typeinspection` is a utility library for discovering and extracting type information from Python classes in Domain-Driven Design applications. It helps you:

- **Discover handled events** in projection/event handler classes via `@apply.register` decorators
- **Extract aggregate types** from generic repository patterns
- **Introspect inheritance hierarchies** in generic type parameters

Built on Python's AST (Abstract Syntax Tree) module for reliable, static code analysis without runtime side effects.

**Requires Python 3.12+**

## Quick Start

### Installation

Using `uv` (recommended):
```bash
uv pip install .
```

Using `pip`:
```bash
pip install .
```

### Basic Usage

**Example 1: Event Handler Discovery in Projections**

```python
from functools import singledispatchmethod
from typeinspection import get_handled_types

class UserDetailsProjection:
    @singledispatchmethod
    def apply(self, event):
        pass

    @apply.register
    def _when(self, event: UserRegistered) -> None:
        pass

    @apply.register
    def _when(self, event: UserNameUpdated) -> None:
        pass

# Extract handled event types
handled_events = get_handled_types(UserDetailsProjection)
# Result: ["UserRegistered", "UserNameUpdated"]
```

**Example 2: Generic Repository Type Extraction**

```python
from typing import Generic, TypeVar
from typeinspection import get_super_name

TEntity = TypeVar("TEntity")

class Repository(Generic[TEntity]):
    @property
    def aggregate_type(self) -> str:
        return get_super_name(self)

class Users(Repository[User]):
    pass

users_repo = Users()
aggregate_type = users_repo.aggregate_type
# Result: "User"
```

## Common Use Cases in DDD

### Event Sourcing with Projections

Projections use the singledispatch pattern to handle different event types. This library helps you discover which events a projection handles without requiring explicit configuration:

```python
projector = Projector(UserDetailsProjection())
events_to_handle = projector.handles  # Auto-discovered from decorators
```

### Aggregate Repositories

Generic repository patterns define the aggregate type they manage. Extract this information for validation, serialization, or reflection:

```python
user_repository = Users()
entity_class = user_repository.aggregate_type  # Extracted: "User"
```

## API Reference

### Handler/Event Discovery

| Function | Purpose | Returns |
|----------|---------|---------|
| `get_handled_types(handler_class)` | Get event types handled by a projection | `List[str]` - unqualified names |
| `get_handled_qualname(handler_class)` | Get fully qualified event types | `List[str]` - module.ClassName format |

### Generic Type Introspection

| Function | Purpose | Returns |
|----------|---------|---------|
| `get_base_name(instance)` | Get base type parameter name | `str` - unqualified |
| `get_base_qualname(instance)` | Get fully qualified base type | `str` - module.ClassName |
| `get_super_name(instance)` | Get super type parameter name | `str` - unqualified |
| `get_super_qualname(instance)` | Get fully qualified super type | `str` - module.ClassName |

## Development

### Setup Environment

```bash
uv sync --all-extras
```

### Run Tests

```bash
uv run pytest
```

### Build Distribution

```bash
uv build
```

## License

MIT - See [LICENSE](LICENSE) for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.
