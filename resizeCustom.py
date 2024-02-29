# ToDo ASAP: Clean up code
from PIL import Image, ImageOps
import os

# May or may not need this not sure yet
# def determine_retail_image_size(original_width, original_height):
#     if original_width == original_height:
#         return original_width
#     # If not a square image, set size to be square based on max_dimension
#     max_dimension = max(original_width, original_height)
#     return round(max_dimension / 100) * 100

def resize_image(image_path, output_path, size):
    # Open the image
    image = Image.open(image_path)

    # Convert to RGBA if RGB (JPEG)
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    new_width, new_height = image.size

    # Resize the image 
    original_width, original_height = image.size
    target_size = size

    aspect_ratio = original_width / original_height
    if aspect_ratio > 1:  # Width is greater than height
        new_width = target_size
        new_height = int(new_width / aspect_ratio)
    else:  # Height is greater than width
        new_height = target_size
        new_width = int(new_height * aspect_ratio)

    # Resize the image to fit within the square
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Create a new square image with a white background
    square_image = Image.new("RGBA", [size, size], (255, 255, 255, 255))

    # Calculate the position to paste the resized image onto the square image
    paste_position = ((size - new_width) // 2, (size - new_height) // 2)

    # Paste the resized image onto the square image
    square_image.paste(resized_image, paste_position)

    # Update the resized_image variable to point to the square image
    resized_image = square_image
    
    # Save the resized image
    output_path = output_path if output_path.lower().endswith('.png') else output_path + '.png'
    resized_image.save(output_path)

    print(f'Resized image saved as: {output_path}')

# Start
vendor = 'BestNest'
vendor_og_dir = f"Vendor_OG_Images/{vendor}"
vendor_resized_dir = f'CustomResize/{vendor}'
new_size = 400

for product_id in sorted(os.listdir(vendor_og_dir)):
    if product_id.startswith('.'):
        continue 
    product_dir = os.path.join(vendor_og_dir, product_id)
    if os.path.isdir(product_dir):
        for image_name in os.listdir(product_dir):
            if image_name.startswith('.'): #.DS_Store issue
                continue
            input_path = os.path.join(product_dir, image_name)
            if os.path.isfile(input_path):
                # Create output directory
                output_dir = os.path.join(vendor_resized_dir, product_id)
                os.makedirs(output_dir, exist_ok=True)

                # Modify image name 
                _, ext = os.path.splitext(image_name)
                modified_image_name = f"{vendor}_{product_id}{ext}"

                output_path = os.path.join(output_dir, modified_image_name)
                resize_image(input_path, output_path, new_size)
    gallery_dir = os.path.join(product_dir, 'GalleryImages')
    if os.path.isdir(gallery_dir):
        # Run through each image in GalleryImages
        for image_name in os.listdir(gallery_dir):
            if image_name.startswith('.'):
                continue
            input_path = os.path.join(gallery_dir, image_name)
            if os.path.isfile(input_path):
                # Create output directory 
                output_dir = os.path.join(vendor_resized_dir, product_id, 'GalleryImages')
                os.makedirs(output_dir, exist_ok=True)

                # Output path 
                output_path = os.path.join(output_dir, image_name)
                resize_image(input_path, output_path, new_size)



                


