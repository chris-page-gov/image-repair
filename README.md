# AI Photo Restoration Toolkit (GFPGAN + Real-ESRGAN)

## ⚡️ Recommended: Fast Local Development with uv

For the fastest Python workflow, use [uv](https://github.com/astral-sh/uv) (a drop-in replacement for pip/pip-tools/venv):

**If you are working locally (not in a container):**
1. Install uv (if not already):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   uv venv .venv
   source .venv/bin/activate
   uv pip install -r requirements.txt -r requirements-dev.txt
   ```

3. Run tests or scripts as usual (e.g., `python ai_restoration_toolkit/restore_photos.py ...`).


> **VS Code users:**
> - The test explorer will discover and run tests automatically if you:
>   - Use the `.vscode/settings.json` provided (pytest enabled, test root set to `tests`)
>   - Have a `.env` file with `PYTHONPATH=.`
>   - Select the `.venv` Python interpreter in the bottom-left or via Command Palette
> - This ensures all tests run in the correct environment and all imports work.

> To run tests manually:
> ```bash
> PYTHONPATH=. pytest
> ```
> This ensures Python can find the ai_restoration_toolkit module.


**If you are in a container (e.g., devcontainer):**
1. Create and activate a virtual environment:
   ```bash
   uv venv .venv
   source .venv/bin/activate
   uv pip install -r ai_restoration_toolkit/requirements.txt -r requirements-dev.txt
   ```
2. Run tests or scripts as usual (e.g., `pytest`, `python ai_restoration_toolkit/restore_photos.py ...`).

> The devcontainer will do this automatically on first start.

> To run tests, use:
> ```bash
> source .venv/bin/activate
> PYTHONPATH=. pytest
> ```
> This ensures Python can find the ai_restoration_toolkit module and uses the venv.

## What this does

- Restores **faces** (eyes, mouth, hair) with **GFPGAN** for natural skin tones.
- Upscales the **whole image** with **Real-ESRGAN** for more detail.
- Applies **mild denoising** and **gentle colour balance** (tuned for scanned prints).

## Quick Start

1. Install Python 3.9+.

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Put your images (JPG/PNG) in an `input` folder.

4. Run:


   ```bash
   python ai_restoration_toolkit/restore_photos.py --in ./input --out ./output --scale 2 --denoise 8 --colour yes
   ```

> Tip for your two examples:
>
> - Photo 1 (blurry): `--scale 2 --denoise 8` is a good start.
> - Photo 5 (colour cast): try `--denoise 4 --colour yes`

## Notes

- First run will **download model weights** automatically into `./weights`.
- If colour looks too warm/cool, rerun with `--colour no` and adjust later in your editor.
- If faces look too smooth, lower `--denoise` (e.g., 4–6).

## Batch processing

Drop many photos in `./input` – each one is processed and saved to `./output` with `_restored_x{scale}` suffix.

## Why this works better

Classical filters blur faces when removing noise. This pipeline **reconstructs** facial detail using learned priors, then upscales the whole image, avoiding the “painted” or “plastic” look.

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) in the project root for a detailed list of all changes, updates, and policies.
