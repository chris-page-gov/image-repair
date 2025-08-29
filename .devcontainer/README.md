# Devcontainer Setup for AI Photo Restoration Toolkit

This folder contains the development container configuration for the image-repair project, designed for robust, reproducible AI photo restoration using GFPGAN and Real-ESRGAN.






## Features

- **Base image:** Uses Microsoft’s official devcontainers for Python, ensuring proper CA certs and VS Code integration.
- **System libraries:** Installs all required system libraries for OpenCV, ffmpeg, and GUI backends.
- **PyTorch:** Installs CPU-only PyTorch by default (works everywhere), with an optional GPU variant.
- **Model weights:** Includes scripts to pre-download model weights for fast, reliable first runs.
- **Non-root user:** Runs as `vscode` for sane file permissions.
- **Input/output folders:** Binds `input/` and `output/` for easy file access between host and container.

## Files

- `devcontainer.json`: Main configuration for VS Code devcontainer.
- `Dockerfile`: CPU-only build (default, works everywhere).
- `Dockerfile.gpu`: Optional GPU build (requires NVIDIA GPU and nvidia-container-toolkit).
- `postCreate.sh`: Script to set up folders and prefetch model weights after container creation.
- `download_models.py`: Downloads required model weights for GFPGAN and Real-ESRGAN.

## Usage

1. Open the repo in VS Code.
2. Select “Reopen in Container” when prompted.
3. Place test images in the `input/` folder.
4. Run the restoration script:

   ```bash
   python ai_restoration_toolkit/restore_photos.py --in ./input --out ./output --scale 2 --denoise 8 --colour yes
   ```

## Switching to GPU

- Edit `devcontainer.json`:
  - Change `"dockerfile": "Dockerfile.gpu"` in the `build` section.
  - Uncomment `"--gpus=all"` in `runArgs`.
- Requires NVIDIA GPU and nvidia-container-toolkit on the host.

## Why this setup?

- **Reliability:** Avoids common issues with CA certs, system libraries, and PyTorch wheels.
- **Performance:** Pre-downloads models for fast startup.
- **Portability:** CPU default works everywhere; GPU is a one-line swap.

---

For more details, see the comments in each file and the main project README.
