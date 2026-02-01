
import os
from PIL import Image

image_dir = "images"
files_to_convert = {
    "anna0.png": {"quality": 80, "resize": (720, 1280)}, # Resize to target dimensions
    "Listinoprezzi.png": {"quality": 90, "resize": None}, # Keep original size if text, high quality
}

files_to_delete = [
    "anna1.png",
    "anna2.png",
    "anna3.png"
]

print("Starting optimization...")

for f, options in files_to_convert.items():
    path = os.path.join(image_dir, f)
    if os.path.exists(path):
        try:
            img = Image.open(path)
            rgb_im = img.convert('RGB')
            
            # Resize if needed
            if options["resize"]:
                # Maintain aspect ratio
                target_w, target_h = options["resize"]
                # Calculate new height based on width to keep aspect ratio
                aspect_ratio = img.width / img.height
                new_w = target_w
                new_h = int(new_w / aspect_ratio)
                
                # If resizing makes it larger, skip
                if new_w < img.width:
                    rgb_im = rgb_im.resize((new_w, new_h), Image.Resampling.LANCZOS)
                    print(f"Resized {f} to {new_w}x{new_h}")
            
            new_filename = os.path.splitext(f)[0] + ".jpg"
            new_path = os.path.join(image_dir, new_filename)
            rgb_im.save(new_path, quality=options["quality"], optimize=True)
            
            old_size = os.path.getsize(path)
            new_size = os.path.getsize(new_path)
            print(f"Converted {f} ({old_size//1024}KB) -> {new_filename} ({new_size//1024}KB)")
            
            # Delete original
            os.remove(path)
            print(f"Deleted original {f}")
            
        except Exception as e:
            print(f"Error converting {f}: {e}")
    else:
        print(f"{f}: Not found")

for f in files_to_delete:
    path = os.path.join(image_dir, f)
    if os.path.exists(path):
        try:
            os.remove(path)
            print(f"Deleted unused file {f}")
        except Exception as e:
            print(f"Error deleting {f}: {e}")
    else:
        print(f"{f}: Already deleted")
