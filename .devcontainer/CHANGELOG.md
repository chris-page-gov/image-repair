# Changelog: .devcontainer


## 2025-08-29

- Initial devcontainer setup for image-repair project.
- Added:
  - `devcontainer.json` (VS Code configuration)
  - `Dockerfile` (CPU-only, default)
  - `Dockerfile.gpu` (optional, NVIDIA GPU)
  - `postCreate.sh` (post-create setup script)
  - `download_models.py` (model weights downloader)
  - `README.md` (this file)
  - `CHANGELOG.md` (this file)
- Features:
  - Robust CA certs and VS Code integration via Microsoft base image
  - System libraries for OpenCV/ffmpeg
  - CPU and GPU PyTorch install options
  - Model weights prefetch on container creation
  - Input/output/weights folders and .gitignore
