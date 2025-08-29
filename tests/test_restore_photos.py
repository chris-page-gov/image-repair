import os
import tempfile
import shutil
import sys
from unittest import mock
import subprocess
from ai_restoration_toolkit import restore_photos

def test_ensure_weights_creates_files(monkeypatch):
    # Use a temp dir and mock urlretrieve to avoid real downloads
    with tempfile.TemporaryDirectory() as tmpdir:
        called = {}
        # Patch urlretrieve directly in restore_photos module
        def fake_urlretrieve(url, path):
            called[url] = path
            with open(path, 'wb') as f:
                f.write(b'0' * 1024)
        monkeypatch.setattr(restore_photos, 'urlretrieve', fake_urlretrieve)
        gfp_path, esr_path = restore_photos.ensure_weights(tmpdir)
        assert os.path.exists(gfp_path)
        assert os.path.exists(esr_path)
        assert gfp_path.endswith('GFPGANv1.4.pth')
        assert esr_path.endswith('realesr-general-x4v3.pth')
        assert len(called) == 2

def test_main_cli_runs(monkeypatch):
    # Create temp input/output dirs and a dummy image
    with tempfile.TemporaryDirectory() as tmpdir:
        in_dir = os.path.join(tmpdir, 'input')
        out_dir = os.path.join(tmpdir, 'output')
        os.makedirs(in_dir)
        os.makedirs(out_dir)
        img_path = os.path.join(in_dir, 'test.jpg')
        # Write a valid dummy image
        dummy_img = np.ones((10,10,3), dtype=np.uint8)*128
        cv2.imwrite(img_path, dummy_img)
        # Patch ensure_weights to avoid downloads
        monkeypatch.setattr(restore_photos, 'ensure_weights', lambda: ("dummy_gfp.pth", "dummy_esr.pth"))
        # Patch GFPGANer and RealESRGANer to no-op
        class DummyRestorer:
            def enhance(self, *a, **k):
                # For GFPGANer: return 3-tuple, for RealESRGANer: return 2-tuple
                if 'outscale' in k or (len(a) > 1 and isinstance(a[1], (int, float))):
                    return dummy_img.copy(), None  # RealESRGANer.enhance
                return None, None, dummy_img.copy()  # GFPGANer.enhance
        monkeypatch.setattr(restore_photos, 'GFPGANer', lambda *a, **k: DummyRestorer())
        monkeypatch.setattr(restore_photos, 'RealESRGANer', lambda *a, **k: DummyRestorer())
        sys_argv = sys.argv
        sys.argv = ["restore_photos.py", "--in", in_dir, "--out", out_dir, "--scale", "2", "--denoise", "8", "--colour", "yes"]
        try:
            restore_photos.main()
            # Check output file exists
            files = os.listdir(out_dir)
            assert any(f.endswith('.jpg') for f in files)
        finally:
            sys.argv = sys_argv
import numpy as np
import pytest
import cv2
from ai_restoration_toolkit.restore_photos import correct_colour_lab

def test_correct_colour_lab_identity():
    img = np.ones((10, 10, 3), dtype=np.uint8) * 128
    # correct_colour_lab expects a, b channels to be uint8 after processing
    result = correct_colour_lab(img, strength=0)
    assert result.dtype == np.uint8
    assert np.allclose(result, img)

def test_correct_colour_lab_shift():
    img = np.zeros((10, 10, 3), dtype=np.uint8)
    img[..., 0] = 100  # B
    img[..., 1] = 150  # G
    img[..., 2] = 200  # R
    result = correct_colour_lab(img, strength=0.5)
    assert result.shape == img.shape
    # Should still be a valid image
    assert result.dtype == np.uint8

def test_denoise_preserves_shape():
    img = np.random.randint(0, 255, (32, 32, 3), dtype=np.uint8)
    denoised = cv2.fastNlMeansDenoisingColored(img, None, 8, 8, 7, 21)
    assert denoised.shape == img.shape
    assert denoised.dtype == img.dtype
