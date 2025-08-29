import numpy as np
import pytest
import cv2
from ai_restoration_toolkit.restore_photos import correct_colour_lab

def test_correct_colour_lab_identity():
    img = np.ones((10, 10, 3), dtype=np.uint8) * 128
    result = correct_colour_lab(img, strength=0)
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
