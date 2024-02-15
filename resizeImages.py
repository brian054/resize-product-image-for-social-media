# Importing???
# Gabriel - consult with G to figure out what way we want to import - via CSV would be ideal

from PIL import Image, ImageOps
import os

# Define the size requirements for each platform
size_requirements = {
    'GoogleMerchant': (100, 100),
    'Facebook': (1200, 630),
    'LinkedIn': (1200, 627),
    'Twitter': (1200, 600),
    'Instagram': (1080, 1080)
}

def resize_image(image_path, output_path, platform):
    # Open the image
    image = Image.open(image_path)

    # Convert to RGBA if RGB (JPEG)
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    # Define platform-specific size requirements
    size_requirements = {
        'GoogleMerchant': (100, 100),
        'Facebook': (1200, 630),
        'LinkedIn': (1200, 627),
        'Twitter': (1200, 600),
        'Instagram': (1080, 1080)
    }

    # Check if the platform is valid
    if platform not in size_requirements:
        raise ValueError(f'Invalid platform: {platform}')

    # Get the required size for the platform
    required_size = size_requirements[platform]

    new_width, new_height = image.size

    # Resize the image 
    if platform == 'GoogleMerchant':
        original_width, original_height = image.size
        if original_width < required_size[0] or original_height < required_size[1]:
            aspect_ratio = original_width / original_height
            if aspect_ratio > 1:
                new_width = max(original_width, required_size[0])
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = max(original_height, required_size[1])
                new_width = int(new_height * aspect_ratio)
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    else:
        # Calculate the scaling factor to fit the image within the required dimensions
        original_width, original_height = image.size
        width_scale = required_size[0] / original_width
        height_scale = required_size[1] / original_height
        scale_factor = min(width_scale, height_scale)

        # Resize the image using the scaling factor
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Create a new image with a transparent background and the exact required dimensions
        new_image = Image.new("RGBA", required_size, (255, 255, 255, 255))

        # Calculate the position to paste the resized image onto the new image
        paste_position = ((required_size[0] - new_width) // 2, (required_size[1] - new_height) // 2)

        # Paste the resized image onto the new image
        new_image.paste(resized_image, paste_position)

        # Update the resized_image variable to point to the new image
        resized_image = new_image

    # Save the resized image
    #resized_image_path = f'resized_{platform}_{image_path}'
    output_path = output_path if output_path.lower().endswith('.png') else output_path + '.png'
    resized_image.save(output_path)

    print(f'Resized image saved as: {output_path}')

# Define the base directories
vendor_og_dir = 'Vendor_OG_Images/AuburnLeather'
vendor_resized_dir = 'Vendor_Resized_Images/AuburnLeather'

for product_id in sorted(os.listdir(vendor_og_dir)):
    if product_id.startswith('.'):
        continue 
    product_dir = os.path.join(vendor_og_dir, product_id)
    #print(product_id)
    if os.path.isdir(product_dir):
        for image_name in os.listdir(product_dir):
            input_path = os.path.join(product_dir, image_name)
            if os.path.isfile(input_path):
                for platform, _ in size_requirements.items():
                    output_dir = os.path.join(vendor_resized_dir, product_id)
                    os.makedirs(output_dir, exist_ok=True)

                    # Modify image name based on platform
                    _, ext = os.path.splitext(image_name)
                    modified_image_name = f"{platform}_{product_id}{ext}"
                    print(modified_image_name)

                    #output_path = f"{vendor_resized_dir}/{product_id}/{platform}/{image_name}"
                    output_path = os.path.join(output_dir, modified_image_name)
                    resize_image(input_path, output_path, platform)
