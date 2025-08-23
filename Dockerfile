# Use official PyTorch base image with CUDA
FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    ffmpeg \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch (CUDA compatible)
RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu121

# Install Shape-E and dependencies
RUN pip3 install git+https://github.com/openai/shap-e.git
RUN pip3 install pillow trimesh

# Copy project files into container
COPY . /app

# Default input/output
VOLUME ["/app/input.txt", "/app/output"]

# Run script
CMD ["python3", "bm3d_ag.py"]
