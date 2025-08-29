#!/usr/bin/env python3
"""
Photo Restoration Pipeline (Faces + Upscale + Colour)

- Face restoration with GFPGAN (rebuilds facial detail & natural skin tones)
- Background/overall upscaling with Real-ESRGAN (x2 or x4)
- Mild denoising to reduce film grain without plastic look
- Optional colour cast correction

USAGE
-----
python ai_restoration_toolkit/restore_photos.py --in ./input --out ./output --scale 2 --denoise 8 --colour yes

Recommended for your case:
python ai_restoration_toolkit/restore_photos.py --in ./input --out ./output --scale 2 --denoise 8 --colour yes

Place your JPG/PNG photos in ./input. Outputs appear in ./output.
"""

import os
import cv2
import argparse
import numpy as np
from glob import glob
from pathlib import Path

# --- Model imports ---
from gfpgan import GFPGANer
from realesrgan import RealESRGANer

GFPGAN_URL = "https://github.com/TencentARC/GFPGAN/releases/download/v1.4/GFPGANv1.4.pth"
ESRGAN_URL = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x2plus.pth"

def ensure_weights(weights_dir="weights"):
    os.makedirs(weights_dir, exist_ok=True)
    gfp_path = os.path.join(weights_dir, "GFPGANv1.4.pth")
    esr_path = os.path.join(weights_dir, "RealESRGAN_x2plus.pth")

    import urllib.request
    if not os.path.exists(gfp_path):
        print("Downloading GFPGAN v1.4 weights...")
        urllib.request.urlretrieve(GFPGAN_URL, gfp_path)
    if not os.path.exists(esr_path):
        print("Downloading Real-ESRGAN x2plus weights...")
        urllib.request.urlretrieve(ESRGAN_URL, esr_path)

    return gfp_path, esr_path

def correct_colour_lab(img_bgr, strength=0.12):
    # neutralise colour cast gently
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    a_mean, b_mean = a.mean(), b.mean()
    a = cv2.add(a, int(-(a_mean - 128) * strength))
    b = cv2.add(b, int(-(b_mean - 128) * strength))
    lab_bal = cv2.merge([l, a, b])
    return cv2.cvtColor(lab_bal, cv2.COLOR_LAB2BGR)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="in_dir", required=True)
    parser.add_argument("--out", dest="out_dir", required=True)
    parser.add_argument("--scale", type=int, default=2, choices=[2,4], help="Upscale factor for Real-ESRGAN")
    parser.add_argument("--denoise", type=int, default=8, help="Denoise strength (0-20 recommended)")
    parser.add_argument("--colour", type=str, default="yes", choices=["yes","no"], help="Auto colour balance")
    args = parser.parse_args()

    in_dir = args.in_dir
    out_dir = args.out_dir
    os.makedirs(out_dir, exist_ok=True)

    gfp_path, esr_path = ensure_weights()

    # Init restorers
    face_restorer = GFPGANer(model_path=gfp_path, upscale=1, arch='clean', channel_multiplier=2)
    bg_restorer = RealESRGANer(model_path=esr_path, scale=2)

    # Gather files
    exts = ("*.jpg","*.jpeg","*.png","*.JPG","*.JPEG","*.PNG")
    files = []
    for e in exts:
        files.extend(glob(os.path.join(in_dir, e)))

    if not files:
        print("No input images found.")
        return

    for fp in files:
        print(f"Processing: {fp}")
        img = cv2.imread(fp, cv2.IMREAD_COLOR)

        # Step 0: mild denoise first (non-aggressive to avoid plastic look)
        if args.denoise > 0:
            img = cv2.fastNlMeansDenoisingColored(img, None, args.denoise, args.denoise, 7, 21)

        # Step 1: face restoration with GFPGAN (paste back into original)
        _, _, restored = face_restorer.enhance(img, has_aligned=False, only_center_face=False, paste_back=True)

        # Optional colour balance
        if args.colour == "yes":
            restored = correct_colour_lab(restored, strength=0.12)

        # Step 2: upscale the whole image with Real-ESRGAN
        restored, _ = bg_restorer.enhance(restored, outscale=args.scale)

        # Step 3: subtle unsharp mask to bring back micro-contrast
        blur = cv2.GaussianBlur(restored, (0,0), 1.0)
        final = cv2.addWeighted(restored, 1.15, blur, -0.15, 0)

        name = Path(fp).stem + f"_restored_x{args.scale}.jpg"
        out_fp = os.path.join(out_dir, name)
        cv2.imwrite(out_fp, final, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
        print(f"Saved -> {out_fp}")

if __name__ == "__main__":
    main()
