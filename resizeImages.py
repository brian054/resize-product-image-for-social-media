# Importing???
# Gabriel - consult with G to figure out what way we want to import - via JSON would be ideal

# ToDo ASAP: Clean up code my god - DRY

from PIL import Image, ImageOps
import os

# Define the size requirements for each platform
size_requirements = {
    'RetailSite': (400, 400),
    'Pinterest': (1000, 1500),
    'GoogleMerchant': (250, 250),
    'Facebook': (1200, 630),
    'LinkedIn': (1200, 627),
    'Twitter': (1200, 600),
    'Instagram': (1080, 1080)
}

def determine_retail_image_size(original_width, original_height):
    if original_width == original_height:
        return original_width
    # If not a square image, set size to be square based on max_dimension
    max_dimension = max(original_width, original_height)
    return round(max_dimension / 100) * 100

def resize_image(image_path, output_path, platform):
    # Open the image
    image = Image.open(image_path)

    # If image can't be opened return nothing and move on 
    # nope nope try opening the image in downloadImages.py, then if you can't open
    # it then don't ever store it in the OG folder to begin with

    # Convert to RGBA if RGB (JPEG)
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

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
    elif platform == 'RetailSite': 
        original_width, original_height = image.size
        target_size = determine_retail_image_size(original_width, original_height)
        required_size = (target_size, target_size) # really don't need this

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
        square_image = Image.new("RGBA", required_size, (255, 255, 255, 255))

        # Calculate the position to paste the resized image onto the square image
        paste_position = ((required_size[0] - new_width) // 2, (required_size[1] - new_height) // 2)

        # Paste the resized image onto the square image
        square_image.paste(resized_image, paste_position)

        # Update the resized_image variable to point to the square image
        resized_image = square_image
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
vendor = 'ScrollsUnlimited'
vendor_og_dir = f"Vendor_OG_Images/{vendor}"
vendor_resized_dir = f'Vendor_Resized_Images/{vendor}'

for product_id in sorted(os.listdir(vendor_og_dir)):
    if product_id.startswith('.'):
        continue 
    product_dir = os.path.join(vendor_og_dir, product_id)
    #print("product dir: ", product_dir)
    #print(product_id)
    if os.path.isdir(product_dir):
        for image_name in os.listdir(product_dir):
            if image_name.startswith('.'): #.DS_Store issue
                continue
            input_path = os.path.join(product_dir, image_name)
            if os.path.isfile(input_path):
                for platform, _ in size_requirements.items():
                    output_dir = os.path.join(vendor_resized_dir, product_id)
                    os.makedirs(output_dir, exist_ok=True)

                    # Modify image name based on platform
                    _, ext = os.path.splitext(image_name)
                    modified_image_name = f"{platform}_{product_id}{ext}"
                    print(modified_image_name)

                    output_path = os.path.join(output_dir, modified_image_name)
                    resize_image(input_path, output_path, platform)
    gallery_dir = os.path.join(product_dir, 'GalleryImages')
    #print("gallery dir: ", gallery_dir)
    if os.path.isdir(gallery_dir):
        # Run through each image in GalleryImages
        for image_name in os.listdir(gallery_dir):
            if image_name.startswith('.'):
                continue
            #print("image name: ", image_name)
            input_path = os.path.join(gallery_dir, image_name)
            #print("input path: ", input_path)
            if os.path.isfile(input_path):
                # Create output directory 
                # vendor_resized_dir + product_id + GalleryImages Folder
                output_dir = os.path.join(vendor_resized_dir, product_id, 'GalleryImages')
                os.makedirs(output_dir, exist_ok=True)
                #print("output_dir: ", output_dir)

                # Output path = just add the image name you need to output_dir
                output_path = os.path.join(output_dir, image_name)
                resize_image(input_path, output_path, 'RetailSite')



                


