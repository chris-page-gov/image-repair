#!/usr/bin/env bash
set -euo pipefail

# Ensure we’re in the workspace
cd /workspaces/image-repair

# Optional: create folders to avoid path confusion
mkdir -p input output weights



# Install uv (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh


# Create and activate a virtual environment (always clear to avoid prompt)
uv venv --clear .venv
source .venv/bin/activate

# Install all Python dependencies (runtime + dev) into the venv
uv pip install --upgrade pip
uv pip install -r ai_restoration_toolkit/requirements.txt -r requirements-dev.txt

# Pre-download model weights (so first run is fast/robust)
python /usr/local/bin/download_models.py

echo "✅ postCreate complete. Try:"
echo "python ai_restoration_toolkit/restore_photos.py --in ./input --out ./output --scale 2 --denoise 8 --colour yes"
