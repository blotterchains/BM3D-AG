#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BM3D-AG (Blender/Model 3D - Assets Generator)

Description:
    BM3D-AG is a game assets generator built on top of OpenAI's Shape-E.
    It generates 3D models and preview animations from text prompts,
    making it easy for game developers to create assets directly from
    natural language descriptions.

Features:
    - Input prompts via input.txt (line by line).
    - Generates 3D assets in both .OBJ and .GLB formats.
    - Creates preview .GIF animations for each asset.
    - Supports CUDA acceleration when available.
    - Batch generation for multiple variations per prompt.

Author:
    Your Name <rezagina68@gmail.com>
    Organization: BMMission
    Repository: https://github.com/BMMission/BM3D-AG

License:
    MIT License. See LICENSE file for details.

Version:
    1.0.0
"""

import torch
import os
import hashlib
from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
from shap_e.util.notebooks import decode_latent_mesh, create_pan_cameras, decode_latent_images
from PIL import Image
import trimesh


# ==========================
# Device setup (CUDA if available)
# ==========================
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# ==========================
# Load models
# ==========================
print("🔄 Loading models...")
xm = load_model('transmitter', device=device)
model = load_model('text300M', device=device)
diffusion = diffusion_from_config(load_config('diffusion'))

# ==========================
# Input & Output paths
# ==========================
INPUT_FILE = "input.txt"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def make_model_main(prompt: str):
    """
    Generate a 3D asset from a text prompt.

    Args:
        prompt (str): The text description of the desired asset.
    """
    print(f"\n⚡ Generating asset for prompt: {prompt}")

    # Generation parameters
    batch_size = 4                # Multiple variations per prompt
    guidance_scale = 17.0
    render_mode = 'nerf'
    size = 256
    karras_steps = 96
    sigma_min = 1e-3
    sigma_max = 180
    s_churn = 0

    # Sample latents from the diffusion model
    latents = sample_latents(
        batch_size=batch_size,
        model=model,
        diffusion=diffusion,
        guidance_scale=guidance_scale,
        model_kwargs=dict(texts=[prompt] * batch_size),
        progress=True,
        clip_denoised=True,
        use_fp16=True,
        use_karras=True,
        karras_steps=karras_steps,
        sigma_min=sigma_min,
        sigma_max=sigma_max,
        s_churn=s_churn,
    )

    # Camera setup
    cameras = create_pan_cameras(size, device)

    # Consistent filenames
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:6]
    base_name = f"asset_{prompt_hash}"

    # Decode & save results
    for i, latent in enumerate(latents):
        asset_name = f"{base_name}_{i}"
        asset_path = os.path.join(OUTPUT_DIR, asset_name)

        # Preview GIF
        images = decode_latent_images(xm, latent, cameras, rendering_mode=render_mode)
        images[0].save(f"{asset_path}.gif", save_all=True, append_images=images[1:], loop=0, duration=50)

        # 3D Model (.obj + .glb)
        t = decode_latent_mesh(xm, latent).tri_mesh()
        with open(f'{asset_path}.obj', 'w') as f:
            t.write_obj(f)

        mesh = trimesh.load(f'{asset_path}.obj')
        mesh.export(f'{asset_path}.glb', file_type='glb')

        print(f"✅ Generated: {asset_path}.glb")

    print(f"🎉 Done! Saved {batch_size} assets for '{prompt}' in '{OUTPUT_DIR}/'")


# ==========================
# Main execution
# ==========================
if __name__ == "__main__":
    if not os.path.exists(INPUT_FILE):
        print(f"❌ No {INPUT_FILE} found. Please provide one with prompts (line by line).")
        exit(1)

    with open(INPUT_FILE, "r") as f:
        prompts = [line.strip() for line in f if line.strip()]

    if not prompts:
        print("❌ No prompts found in input.txt.")
        exit(1)

    for p in prompts:
        make_model_main(p)
