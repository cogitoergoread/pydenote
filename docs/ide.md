# IDE configuration

VSCode is used.

## Editorconfig

Sample `.editorconfig` file added. VSCode extension should be installed.

## Lint

`Ruff` linter is used.

CLI Ruff install:

```shell
pdm add -dG lint ruff
```

Stuff to add`pyproject.toml`:

```text
[tool.ruff]
select = [
    "B", # flake8-bugbear
    "C4", # flake8-comprehensions
    "E", # pycodestyle - Error
    "F", # Pyflakes
    "I", # isort
    "W", # pycodestyle - Warning
    "UP", # pyupgrade
]
ignore = [
    "E501", # line-too-long
    "W191", # tab-indentation
]
include = ["**/*.py", "**/*.pyi", "**/pyproject.toml"]
[tool.ruff.pydocstyle]
convention = "google"
```

`MyPy` also added:

```shell
pdm add -dG lint mypy
```

It has to be configured to exclude `tests/` in VSCode `settings.json`:

```json
"mypy-type-checker.ignorePatterns": [
      "tests/*py"
    ],
    "mypy-type-checker.preferDaemon": true,
    "mypy-type-checker.reportingScope": "workspace"
```

## Pre-commit

Pre-commit hook to keep code clean. Install:

```shell
pdm add -dG lint pre-commit
```

A file should be added, `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-yaml
        args:
          - --unsafe
      - id: end-of-file-fixer
      - id: trailing-whitespace
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.2
    hooks:
      - id: ruff
      - id: ruff-format
```

```shell
pdm run pre-commit install
```

## Pytest

Some testing tool should be installed in order to write tested code. Install:

```shell
pdm add -dG pytest pytest-cov
```

Should be configured as well `pyproject.toml`:

```toml
[tool.pytest.ini_options]
log_level = "DEBUG"
addopts = '''
--cov=tnt
 --color=yes
 --cov-report=term
 --log-cli-level=DEBUG
'''
pythonpath = [
  "src/pydenote"
]
```
