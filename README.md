# AI Photo Restoration Toolkit (GFPGAN + Real-ESRGAN)

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
   python restore_photos.py --in ./input --out ./output --scale 2 --denoise 8 --colour yes
   ```

> Tip for your two examples:
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
