# Base: Microsoft devcontainers with Python & proper CA certs
FROM mcr.microsoft.com/devcontainers/python:3.9

# Avoid prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_NO_CACHE_DIR=1

# System libs needed by OpenCV/ffmpeg/GUI backends used by cv2
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    git wget curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /workspaces/${LOCAL_WORKSPACE_FOLDER_BASENAME:-app}

# --- Python deps ---
# 1) Install CPU-only PyTorch (stable wheels)
RUN pip install --upgrade pip && \
    pip install --extra-index-url https://download.pytorch.org/whl/cpu \
      torch torchvision torchaudio

# 2) Core libs for the toolkit
#    We keep versions flexible to avoid broken wheels in the future.
COPY ai_restoration_toolkit/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Helper scripts for first-run model downloads & setup
COPY .devcontainer/download_models.py /usr/local/bin/download_models.py
COPY .devcontainer/postCreate.sh /usr/local/bin/postCreate.sh
RUN chmod +x /usr/local/bin/postCreate.sh

# Default shell
SHELL ["/bin/bash", "-lc"]
