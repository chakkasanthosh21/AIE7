# Quick Image Display - Copy this into a Jupyter notebook cell

# Method 1: Simple display (most common)
from IPython.display import Image, display

# Display the image from current directory
display(Image('image.png'))

# Method 2: With custom size
display(Image('image.png', width=400, height=300))

# Method 3: Display images from other directories
display(Image('../02_Embeddings_and_RAG/images/docchain_img.png', width=400))

# Method 4: List all images in current directory
import glob

image_files = glob.glob('*.png') + glob.glob('*.jpg') + glob.glob('*.jpeg')
print(f"Found {len(image_files)} images: {image_files}")

# Display all images found
for img_file in image_files:
    print(f"Displaying: {img_file}")
    display(Image(img_file, width=300)) 