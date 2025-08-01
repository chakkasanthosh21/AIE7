# Image Display Examples for Jupyter Notebooks
# Run these cells in your Jupyter notebook

# Method 1: Using IPython.display (Recommended)
from IPython.display import Image, display

# Display image from current directory
display(Image('image.png'))

# Display image with custom width
display(Image('image.png', width=400))

# Display image with custom height
display(Image('image.png', height=300))

# Display image with both width and height
display(Image('image.png', width=500, height=400))

# Method 2: Using matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Display image using matplotlib
img = mpimg.imread('image.png')
plt.figure(figsize=(10, 8))
plt.imshow(img)
plt.axis('off')  # Hide axes
plt.show()

# Method 3: Using PIL (Python Imaging Library)
from PIL import Image as PILImage

# Open and display image
pil_img = PILImage.open('image.png')
display(pil_img)

# Method 4: Using HTML (for more control)
from IPython.display import HTML

# Display image using HTML
html_code = f'<img src="image.png" width="400" height="300" alt="Session 12 Image">'
display(HTML(html_code))

# Method 5: Display images from other directories
# Display image from 02_Embeddings_and_RAG/images
display(Image('../02_Embeddings_and_RAG/images/docchain_img.png', width=400))
display(Image('../02_Embeddings_and_RAG/images/inline_answer_sample.png', width=400))

# Method 6: List all images in current directory
import os
import glob

# Find all image files in current directory
image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp']
image_files = []
for ext in image_extensions:
    image_files.extend(glob.glob(ext))

print("Images found in current directory:")
for img_file in image_files:
    print(f"- {img_file}")
    display(Image(img_file, width=300))

# Method 7: Display multiple images in a grid
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Create a grid of images
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Load and display images
img1 = mpimg.imread('image.png')
img2 = mpimg.imread('../02_Embeddings_and_RAG/images/docchain_img.png')

axes[0].imshow(img1)
axes[0].set_title('Session 12 Image')
axes[0].axis('off')

axes[1].imshow(img2)
axes[1].set_title('DocChain Image')
axes[1].axis('off')

plt.tight_layout()
plt.show() 