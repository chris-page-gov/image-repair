import os
import urllib.request

os.makedirs("weights", exist_ok=True)

MODELS = {
    "GFPGANv1.4.pth":
      "https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth",
    "RealESRGAN_x4plus.pth":
      "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"
}

for name, url in MODELS.items():
    path = os.path.join("weights", name)
    if not os.path.exists(path):
        print(f"Downloading {name} ...")
        urllib.request.urlretrieve(url, path)
        print(f"Saved -> {path}")
    else:
        print(f"Already present -> {path}")
