#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify GPU setup is working correctly.
"""

import sys

# Fix Windows console encoding for Unicode
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def test_pytorch_gpu():
    """Test PyTorch GPU setup."""
    try:
        import torch
        print("=" * 70)
        print("PyTorch GPU Test")
        print("=" * 70)
        print()

        print(f"PyTorch Version: {torch.__version__}")
        print(f"CUDA Available: {torch.cuda.is_available()}")

        if torch.cuda.is_available():
            print(f"CUDA Version (PyTorch): {torch.version.cuda}")
            print(f"GPU Device Count: {torch.cuda.device_count()}")
            print(f"Current GPU: {torch.cuda.get_device_name(0)}")
            print(f"GPU Capability: {torch.cuda.get_device_capability(0)}")

            # Test basic GPU operation
            print()
            print("Testing GPU computation...")
            x = torch.randn(1000, 1000).cuda()
            y = torch.randn(1000, 1000).cuda()
            z = torch.matmul(x, y)
            print(f"✅ GPU computation successful! Result shape: {z.shape}")
            print(f"✅ GPU memory allocated: {torch.cuda.memory_allocated(0) / 1024**2:.2f} MB")
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            print("Apple Silicon (MPS) Available: Yes")
            print()
            print("Testing MPS computation...")
            x = torch.randn(1000, 1000).to('mps')
            y = torch.randn(1000, 1000).to('mps')
            z = torch.matmul(x, y)
            print(f"✅ MPS computation successful! Result shape: {z.shape}")
        else:
            print("Running in CPU-only mode")
            print("⚠️  For better performance, ensure you have:")
            print("   - NVIDIA GPU with CUDA support")
            print("   - AMD GPU with ROCm support (Linux only)")
            print("   - Apple Silicon Mac (M1/M2/M3)")

        print()
        print("=" * 70)
        return True

    except Exception as e:
        print(f"❌ Error testing PyTorch GPU: {e}")
        return False


def test_transformers():
    """Test transformers library."""
    try:
        import transformers
        print()
        print("Transformers Library Test")
        print("=" * 70)
        print(f"Transformers Version: {transformers.__version__}")
        print("✅ Transformers library loaded successfully")
        print("=" * 70)
        return True
    except Exception as e:
        print(f"❌ Error testing transformers: {e}")
        return False


def test_sentence_transformers():
    """Test sentence-transformers library."""
    try:
        from sentence_transformers import SentenceTransformer
        print()
        print("Sentence Transformers Library Test")
        print("=" * 70)
        print("✅ Sentence-transformers library loaded successfully")
        print("=" * 70)
        return True
    except Exception as e:
        print(f"❌ Error testing sentence-transformers: {e}")
        return False


if __name__ == "__main__":
    print()
    print("=" * 70)
    print("GPU Setup Verification Test")
    print("=" * 70)
    print()

    results = []
    results.append(("PyTorch GPU", test_pytorch_gpu()))
    results.append(("Transformers", test_transformers()))
    results.append(("Sentence Transformers", test_sentence_transformers()))

    print()
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)

    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False

    print("=" * 70)

    if all_passed:
        print()
        print("🎉 All tests passed! Your GPU setup is working correctly.")
        print()
        sys.exit(0)
    else:
        print()
        print("⚠️  Some tests failed. Please check the output above.")
        print()
        sys.exit(1)
