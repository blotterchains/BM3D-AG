# BM3D-AG

**Blender/Model 3D - Assets Generator**

BM3D-AG is a Python-based **game assets generator** powered by [Shape-E](https://github.com/openai/shap-e).
It allows you to generate **3D game-ready assets** from text input.
To simplify installation and GPU acceleration (CUDA), BM3D-AG is packaged with **Docker**.

With this setup, you don’t need to worry about dependencies or CUDA drivers inside Python — everything runs inside the container.

---

## 🚀 Features

* Generate **3D assets** for games using Shape-E.
* Input as a **file (line by line array)** → each line = one generation prompt.
* Supports **CUDA acceleration** when Docker is run with `--gpus all`.
* Portable: build your own Docker image or pull from Docker Hub.

---

## 📦 Installation

### 1. Install Docker

Follow the official Docker installation guide for your OS:

* [Docker Desktop (Windows/Mac)](https://docs.docker.com/get-docker/)
* [Docker Engine (Linux)](https://docs.docker.com/engine/install/)

After installation, verify with:

```bash
docker --version
```

If you have an NVIDIA GPU, install:

* [NVIDIA Drivers](https://www.nvidia.com/Download/index.aspx)
* [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

Verify GPU access in Docker:

```bash
docker run --rm --gpus all nvidia/cuda:12.2.0-base nvidia-smi
```

---

### 2. Clone the Repository

```bash
git clone https://github.com/BMMission/BM3D-AG.git
cd BM3D-AG
```

---

## 🛠️ Build Docker Image

You can build the image locally:

```bash
docker build -t bm3d-ag .
```

Or pull from Docker Hub (if published):

```bash
docker pull BMMission/bm3d-ag:latest
```

---

## ▶️ Usage

### 1. Prepare Input File

Create a file `input.txt` with prompts (each line = one asset):

```
futuristic sword
wooden treasure chest
icy mountain castle
flying robot drone
```

---

### 2. Run the Generator

Run with CUDA support:

```bash
docker run --rm -it \
  --gpus all \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/input.txt:/app/input.txt \
  bm3d-ag
```

Explanation:

* `--gpus all` → enables GPU acceleration.
* `-v $(pwd)/output:/app/output` → saves generated assets to local `output/`.
* `-v $(pwd)/input.txt:/app/input.txt` → reads prompts from local `input.txt`.
* `bm3d-ag if you named it and build it from dockerfile if you pull from dockerhub BMMission/bm3d-ag fro prebuild image`
---

### 3. Output

All generated `.glb` or `.obj` files will appear inside the `output/` folder.

---

## 🧩 Example

```bash
echo "ancient ice temple" > input.txt
docker run --rm --gpus all \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/input.txt:/app/input.txt \
  bm3d-ag
```

Output:

```
output/ancient_ice_temple.glb
```

---

## 📌 Notes

* Requires **NVIDIA GPU** for CUDA acceleration.
* CPU-only mode is possible but much slower (remove `--gpus all`).
* Customize Dockerfile if you need additional dependencies.

---

## 🐳 Docker Hub (Optional)

If you publish to Docker Hub:

```bash
docker pull  BMMission/bm3d-ag
```

Run it:

```bash
docker run --rm --gpus all -v $(pwd)/output:/app/output -v $(pwd)/input.txt:/app/input.txt BMMission/bm3d-ag
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or PRs.

---

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.

