"""
Convert PNG logo to ICO format for Windows taskbar icon
"""
from PIL import Image
import os

# Get paths
base_dir = os.path.dirname(os.path.abspath(__file__))
png_path = os.path.join(base_dir, "assets", "wfm main logo1.png")
ico_path = os.path.join(base_dir, "assets", "wfm_logo.ico")

# Load PNG and convert to ICO with multiple sizes
img = Image.open(png_path)

# Create ICO with multiple sizes (16, 32, 48, 64, 128, 256)
icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
img.save(ico_path, format='ICO', sizes=icon_sizes)

print(f"✅ ICO file created: {ico_path}")
print(f"   Sizes: {icon_sizes}")
