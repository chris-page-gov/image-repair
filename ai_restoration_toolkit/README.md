
# AI Photo Restoration Toolkit

This toolkit restores and upscales old or damaged photos using GFPGAN (face restoration) and Real-ESRGAN (upscaling), with additional color and sharpness enhancements for scanned prints.

---

## 🔧 Setup Instructions (One-Time)

1. Install dependencies (Python 3.9+ recommended):

   ```bash
   pip install realesrgan gfpgan basicsr facexlib
   ```

2. Download pretrained models:
   - GFPGAN v1.4: [GFPGAN v1.4 model](https://github.com/TencentARC/GFPGAN/releases/download/v1.4/GFPGANv1.4.pth)
   - Real-ESRGAN x2 or x4: [Real-ESRGAN models](https://github.com/xinntao/Real-ESRGAN/releases/tag/v0.1.0)

3. Put the `.pth` model files in a folder like `./weights/`.

---

## 🖼️ Restoration Pipeline (Python Script)

```python
from PIL import Image
import cv2
from gfpgan import GFPGANer
from realesrgan import RealESRGANer

# Load GFPGAN for face restoration
restorer = GFPGANer(
	model_path='weights/GFPGANv1.4.pth',
	upscale=2,
	arch='clean',
	channel_multiplier=2
)

# Load Real-ESRGAN for background upscaling
bg_restorer = RealESRGANer(
	model_path='weights/RealESRGAN_x2plus.pth',
	scale=2
)

# Input image
input_path = "photo1.jpg"
img = cv2.imread(input_path, cv2.IMREAD_COLOR)

# Step 1: Face restoration with GFPGAN
cropped_faces, restored_faces, restored_img = restorer.enhance(
	img, has_aligned=False, only_center_face=False, paste_back=True
)

# Step 2: Upscale whole image with Real-ESRGAN
restored_img, _ = bg_restorer.enhance(restored_img, outscale=2)

# Save output
cv2.imwrite("photo1_restored.jpg", restored_img)
print("✅ Saved: photo1_restored.jpg")
```

---

## 🎯 What You’ll Get

- Faces reconstructed (eyes, mouth, hair sharper & more natural).
- Whole photo upscaled with better detail and less noise.
- Skin tones corrected by GFPGAN’s learned priors.

---

For more details, see the main project README and comments in `restore_photos.py`.
