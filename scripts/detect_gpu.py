#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GPU Detection Script - Detects available GPU and determines correct PyTorch installation.

This script runs BEFORE installing PyTorch to determine which version to install.
"""

import subprocess
import platform
import sys
import json
import os

# Fix Windows console encoding for Unicode
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def detect_nvidia_gpu():
    """
    Detect NVIDIA GPU using nvidia-smi.
    Returns: (has_gpu, gpu_name, cuda_version) or (False, None, None)
    """
    try:
        # Try to run nvidia-smi
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=name,driver_version', '--format=csv,noheader'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0 and result.stdout.strip():
            lines = result.stdout.strip().split('\n')
            gpu_name = lines[0].split(',')[0].strip()
            driver_version = lines[0].split(',')[1].strip()

            # Get CUDA version from nvidia-smi output
            # Method 1: Try to get from nvidia-smi general output
            cuda_version = None
            try:
                cuda_result = subprocess.run(
                    ['nvidia-smi'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                if cuda_result.returncode == 0:
                    # Parse CUDA version from output like "CUDA Version: 12.8"
                    for line in cuda_result.stdout.split('\n'):
                        if 'CUDA Version:' in line:
                            cuda_version = line.split('CUDA Version:')[1].strip().split()[0]
                            break
            except:
                pass

            return True, gpu_name, cuda_version
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        pass

    return False, None, None


def detect_amd_gpu():
    """
    Detect AMD GPU (ROCm support).
    Returns: (has_gpu, gpu_name)
    """
    system = platform.system()

    if system == "Linux":
        try:
            # Try rocm-smi
            result = subprocess.run(
                ['rocm-smi', '--showproductname'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0 and result.stdout.strip():
                # Parse output
                for line in result.stdout.split('\n'):
                    if 'GPU' in line and 'Card series' in line:
                        gpu_name = line.split(':')[1].strip()
                        return True, gpu_name
        except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
            pass

    return False, None


def detect_apple_silicon():
    """
    Detect Apple Silicon (M1/M2/M3).
    Returns: (has_mps, chip_name)
    """
    system = platform.system()

    if system == "Darwin":  # macOS
        try:
            # Check if running on Apple Silicon
            result = subprocess.run(
                ['sysctl', '-n', 'machdep.cpu.brand_string'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                cpu_brand = result.stdout.strip()
                if 'Apple' in cpu_brand:
                    return True, cpu_brand
        except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
            pass

    return False, None


def get_pytorch_install_command(gpu_info):
    """
    Generate the correct PyTorch installation command based on GPU detection.

    Args:
        gpu_info: Dictionary with GPU detection results

    Returns:
        (pip_command, description)
    """
    if gpu_info['nvidia_gpu']:
        cuda_version = gpu_info['cuda_version']

        # Determine CUDA version for PyTorch
        if cuda_version:
            try:
                cuda_major = int(cuda_version.split('.')[0])
                cuda_minor = int(cuda_version.split('.')[1]) if '.' in cuda_version else 0

                # Support for CUDA 12.x (12.1 through 12.8+)
                if cuda_major == 12:
                    # Use cu121 for CUDA 12.1-12.4, cu124 for CUDA 12.4+
                    if cuda_minor >= 4:
                        torch_package = "torch torchvision torchaudio"
                        index_url = "https://download.pytorch.org/whl/cu124"
                        desc = f"PyTorch with CUDA 12.4+ support for {gpu_info['gpu_name']} (CUDA {cuda_version})"
                    else:
                        torch_package = "torch torchvision torchaudio"
                        index_url = "https://download.pytorch.org/whl/cu121"
                        desc = f"PyTorch with CUDA 12.1 support for {gpu_info['gpu_name']} (CUDA {cuda_version})"

                # Support for CUDA 11.x
                elif cuda_major == 11:
                    torch_package = "torch torchvision torchaudio"
                    index_url = "https://download.pytorch.org/whl/cu118"
                    desc = f"PyTorch with CUDA 11.8 support for {gpu_info['gpu_name']} (CUDA {cuda_version})"

                # For future CUDA versions (13+), try latest CUDA 12 build
                else:
                    torch_package = "torch torchvision torchaudio"
                    index_url = "https://download.pytorch.org/whl/cu124"
                    desc = f"PyTorch with CUDA 12.4+ support for {gpu_info['gpu_name']} (detected CUDA {cuda_version})"

            except (ValueError, IndexError):
                # Fallback if version parsing fails
                torch_package = "torch torchvision torchaudio"
                index_url = "https://download.pytorch.org/whl/cu124"
                desc = f"PyTorch with CUDA 12.4+ support for {gpu_info['gpu_name']}"
        else:
            # No CUDA version detected, use latest CUDA 12 build
            torch_package = "torch torchvision torchaudio"
            index_url = "https://download.pytorch.org/whl/cu124"
            desc = f"PyTorch with CUDA 12.4+ support for {gpu_info['gpu_name']}"

        pip_cmd = f"pip install {torch_package} --index-url {index_url}"
        return pip_cmd, desc

    elif gpu_info['amd_gpu']:
        # AMD ROCm support (Linux only) - use latest stable ROCm
        torch_package = "torch torchvision torchaudio"
        index_url = "https://download.pytorch.org/whl/rocm6.2"
        desc = f"PyTorch with ROCm 6.2 support for {gpu_info['gpu_name']}"
        pip_cmd = f"pip install {torch_package} --index-url {index_url}"
        return pip_cmd, desc

    elif gpu_info['apple_silicon']:
        # Apple Silicon - use standard PyTorch (MPS support included)
        torch_package = "torch torchvision torchaudio"
        desc = f"PyTorch with Metal Performance Shaders (MPS) for {gpu_info['chip_name']}"
        pip_cmd = f"pip install {torch_package}"
        return pip_cmd, desc

    else:
        # CPU only
        torch_package = "torch torchvision torchaudio"
        desc = "PyTorch (CPU-only version)"
        pip_cmd = f"pip install {torch_package}"
        return pip_cmd, desc


def main():
    """Main detection logic."""
    print("=" * 70)
    print("GPU DETECTION SYSTEM")
    print("=" * 70)
    print()

    # Detect all GPU types
    nvidia_gpu, nvidia_name, cuda_version = detect_nvidia_gpu()
    amd_gpu, amd_name = detect_amd_gpu()
    apple_mps, apple_chip = detect_apple_silicon()

    # Build GPU info dictionary
    gpu_info = {
        'nvidia_gpu': nvidia_gpu,
        'gpu_name': nvidia_name,
        'cuda_version': cuda_version,
        'amd_gpu': amd_gpu,
        'amd_name': amd_name,
        'apple_silicon': apple_mps,
        'chip_name': apple_chip
    }

    # Display detection results
    print("Detection Results:")
    print("-" * 70)

    if nvidia_gpu:
        print(f"✅ NVIDIA GPU Detected: {nvidia_name}")
        if cuda_version:
            print(f"   CUDA Version: {cuda_version}")
        else:
            print(f"   CUDA Version: Unable to determine (will use CUDA 12.1)")
    else:
        print("❌ No NVIDIA GPU detected")

    print()

    if amd_gpu:
        print(f"✅ AMD GPU Detected: {amd_name}")
    else:
        print("❌ No AMD GPU detected")

    print()

    if apple_mps:
        print(f"✅ Apple Silicon Detected: {apple_chip}")
        print("   Metal Performance Shaders (MPS) will be available")
    else:
        print("❌ Not running on Apple Silicon")

    print()
    print("=" * 70)
    print()

    # Determine PyTorch installation
    pip_command, description = get_pytorch_install_command(gpu_info)

    print("Recommended PyTorch Installation:")
    print("-" * 70)
    print(f"Description: {description}")
    print(f"Command: {pip_command}")
    print()

    # Save configuration for setup script
    config = {
        'gpu_info': gpu_info,
        'pytorch_command': pip_command,
        'description': description
    }

    with open('.gpu_config.json', 'w') as f:
        json.dump(config, f, indent=2)

    print("✅ Configuration saved to .gpu_config.json")
    print()

    # Show expected speedup
    if nvidia_gpu or amd_gpu or apple_mps:
        print("🚀 Expected Performance:")
        print("   With GPU: ~5-10 seconds per evaluation")
        print("   Total lesson time: ~5-10 minutes")
        print()
        print("   This is 10-20x faster than CPU!")
    else:
        print("⚠️  CPU-Only Mode:")
        print("   With CPU: ~20-40 seconds per evaluation")
        print("   Total lesson time: ~15-25 minutes")
        print()
        print("   Consider using a machine with GPU for better performance.")

    print()
    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
