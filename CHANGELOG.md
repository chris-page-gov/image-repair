# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-08-29
### Added
- Enforced exclusion of `.venv/` in `.gitignore` to prevent accidental commits of the virtual environment.
- Audited and updated all documentation and scripts to consistently reference `.venv` and its activation.
- Added safeguard and policy in `copilot-instructions.md` to require `.venv` exclusion and venv usage consistency in all future changes.

### Changed
- Switched devcontainer Python dependency management to use a uv-managed virtual environment (`uv venv .venv`) for all installs, avoiding permission issues and aligning with best practices.
- Updated README and copilot-instructions.md to reflect new venv-based workflow for both container and local development.

## [1.0.0] - 2025-08-29
### Added
- Initial devcontainer setup for image-repair project.
- Added: `devcontainer.json`, `Dockerfile`, `Dockerfile.gpu`, `postCreate.sh`, `download_models.py`, `README.md`, `CHANGELOG.md` (this file)
- Features: Robust CA certs and VS Code integration, system libraries for OpenCV/ffmpeg, CPU and GPU PyTorch install options, model weights prefetch, input/output/weights folders and .gitignore

### Changed
- Fixed usage instructions in `restore_photos.py` and `README.md` to use correct script path (`ai_restoration_toolkit/restore_photos.py`).
- Updated model download and usage to use RealESRGAN_x4plus.pth instead of x2plus.
