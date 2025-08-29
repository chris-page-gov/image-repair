#!/usr/bin/env bash
set -euo pipefail

# Ensure we’re in the workspace
cd /workspaces/*

# Optional: create folders to avoid path confusion
mkdir -p input output weights

# Pre-download model weights (so first run is fast/robust)
python /usr/local/bin/download_models.py

echo "✅ postCreate complete. Try:"
echo "python ai_restoration_toolkit/restore_photos.py --in ./input --out ./output --scale 2 --denoise 8 --colour yes"
