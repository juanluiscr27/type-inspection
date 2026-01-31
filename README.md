# Type Inspection

Get the module name, class name and fully qualified name of python classes
## Installation

### Using uv (Recommended)

```bash
uv pip install .
```

Or for development with testing dependencies:

```bash
uv sync --all-extras
```

### Using pip

```bash
pip install .
```

## Development

### Setup Development Environment

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