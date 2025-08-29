# Safeguards and Consistency

- Always add `.venv/` to `.gitignore` to prevent committing the virtual environment.
- All documentation, scripts, and code must refer to `.venv` and its activation consistently (e.g., `source .venv/bin/activate`).
- When updating dependencies or workflow, check that `.venv` usage is correct in:
  - `.gitignore`
  - `README.md`
  - `copilot-instructions.md`
  - `postCreate.sh` and any setup scripts
- Copilot and contributors should refuse to generate or accept code that omits `.venv` from `.gitignore` or uses inconsistent venv activation.
# Copilot Instructions: Test-Driven Development for Python

This project uses Python and is designed for test-driven development (TDD). Follow these guidelines to ensure Copilot and contributors can generate, run, and maintain tests effectively.

For local development (outside containers), prefer using [uv](https://github.com/astral-sh/uv) for dependency management and virtual environments. Use pip/venv only if uv is unavailable.

For container/devcontainer workflows, create and activate a virtual environment with uv:
```bash
uv venv .venv
source .venv/bin/activate
uv pip install -r ai_restoration_toolkit/requirements.txt -r requirements-dev.txt
```

To check if you are in a container, look for the `/.dockerenv` file:
```bash
if [ -f "/.dockerenv" ]; then echo "In container"; else echo "Local dev"; fi
```
- Place all test files in a `tests/` directory at the project root.
- Name test files as `test_*.py` (e.g., `test_restore_photos.py`).
- Use the `pytest` framework for writing and running tests.

## 2. Writing Tests
- Each function or class should have at least one corresponding test.
- Use descriptive test function names (e.g., `def test_face_restoration():`).
- Include tests for both expected behavior and edge cases.
- Use fixtures for setup/teardown if needed.

## 3. Running Tests
- Run all tests with:
  ```bash
  source .venv/bin/activate
  PYTHONPATH=. pytest
  ```
- To run a specific test file:
  ```bash
  source .venv/bin/activate
  PYTHONPATH=. pytest tests/test_restore_photos.py
  ```

## 4. Test Coverage
- Aim for high test coverage, especially for core logic in `ai_restoration_toolkit/`.
- Use `pytest-cov` for coverage reports:
  ```bash
  pytest --cov=ai_restoration_toolkit
  ```

## 5. Continuous Integration
- Ensure all tests pass before merging code.
- Add new tests for any new features or bug fixes.


## 6. Documentation and Changelog Requirements
- All new features, bug fixes, and significant changes must be documented in the `README.md` or other relevant documentation files.
- Every code or feature change must include a corresponding entry in the `CHANGELOG.md` (with date and summary).

## 7. Copilot Usage
- When prompted, Copilot should:
  - Generate tests in the `tests/` directory.
  - Use `pytest` conventions.
  - Suggest test cases for new or changed code.
  - Refactor or update tests as code evolves.
  - Prompt for or add documentation and changelog entries for all substantive changes.

## 7. Example Test (pytest)
```python
import pytest
from ai_restoration_toolkit.restore_photos import correct_colour_lab
import numpy as np

def test_correct_colour_lab_identity():
    img = np.ones((10, 10, 3), dtype=np.uint8) * 128
    result = correct_colour_lab(img, strength=0)
    assert np.allclose(result, img)
```

---

By following these instructions, Copilot and all contributors can maintain a robust, test-driven Python codebase.
