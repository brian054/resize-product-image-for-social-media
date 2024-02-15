# use a query string to download img urls 
# use those img urls to download (automatically via python) all the imgs you need instead
# of manually going into each product to extract the image. 

# But First
# Let's correctly resize one product image
# Then try 5-10 at once
# Once that's done -> Try the query string to download all img's
# if you have all the imgs then boom run the script until it resizes everything

# Importing???
# For now just manually -> eventually would like to import via 

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

# def resize_and_pad_image_for_platform(input_path, output_path, platform):
#     """
#     Resizes and pads an image based on the platform's size requirements,
#     with specific logic for Google non-apparel and apparel to ensure the image
#     is larger than minimum size requirements and as close to 1:1 aspect ratio as possible.

#     Args:
#     - input_path: The path to the input image.
#     - output_path: The path where the resized and padded image will be saved.
#     - platform: The name of the platform (e.g., 'google_non_apparel', 'google_apparel', 'facebook', 'linkedin', 'twitter', 'instagram').
#     """

#     # Get the required size for the platform
#     target_size = size_requirements.get(platform)
#     if not target_size:
#         print(f"Platform '{platform}' not recognized.")
#         return

#     target_width, target_height = target_size

#     try:
#         with Image.open(input_path) as img:
#             original_width, original_height = img.size
            
#             # Check if the image is already larger than the minimum requirement
#             if platform in ['GoogleMerchant'] and original_width > target_width and original_height > target_height:
#                 # Resize to get as close to 1:1 aspect ratio as possible
#                 new_size = max(original_width, original_height)
#                 img = img.resize((new_size, new_size), Image.Resampling.LANCZOS)
#             else:
#                 # Calculate the new size, preserving the aspect ratio
#                 ratio = min(target_width / original_width, target_height / original_height)
#                 new_size = (int(original_width * ratio), int(original_height * ratio))
#                 img = img.resize(new_size, Image.Resampling.LANCZOS)

#             # For non-Google platforms, or if the Google image is resized above, pad to target dimensions
#             if platform not in ['GoogleMerchant']:
#                 # Create a new image with a white background and the target size
#                 new_img = Image.new("RGB", (target_width, target_height), (255, 255, 255))
#                 # Paste the resized image onto the center of the new image
#                 new_img.paste(img, ((target_width - new_size[0]) // 2, (target_height - new_size[1]) // 2))
#                 img = new_img

#             # Check if the output directory exists, create it if not
#             output_dir = os.path.dirname(output_path)
#             if not os.path.exists(output_dir):
#                 os.makedirs(output_dir, exist_ok=True)
#                 print(f"Created directory {output_dir}")

#             # Save the new image
#             img.save(output_path)
#             print(f"Image saved to {output_path}")
#     except Exception as e:
#         print(f"An error occurred: {e}")

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
        new_image = Image.new("RGBA", required_size, (0, 0, 0, 0))

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

# for key, value in size_requirements.items():
#     output_path = f"Vendors_Resized_Images/LibertyTableTop/testImage_{key}.jpeg"
#     resize_and_pad_image_for_platform('images/testImage.jpeg', output_path, key)

# Example usage for Google non-apparel
# resize_image('images/test.jpeg', 'resizedImages/testImage/testNewGM.png', 'GoogleMerchant')
# resize_image('images/test.jpeg', 'resizedImages/testImage/testNewFB.png', 'Facebook')
# resize_image('images/test.jpeg', 'resizedImages/testImage/testNewLI.png', 'LinkedIn')
# resize_image('images/test.jpeg', 'resizedImages/testImage/testNewTwitter.png', 'Twitter')
# resize_image('images/test.jpeg', 'resizedImages/testImage/testNewInsta.png', 'Instagram')

# Define the base directories
vendor_og_dir = 'Vendor_OG_Images/KR_Creative'
vendor_resized_dir = 'Vendor_Resized_Images/KR_Creative'

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


# Below is for generating those locally hosted folders - not all images have white background so I'm gonna
# try some AI stuff to help with those issues.

# from PIL import Image, ImageOps
# import os

# # Size requirements with a special note for Google Merchant
# size_requirements = {
#     'GoogleMerchant': (100, 100),  # Minimum size
#     'Facebook': (1200, 630),
#     'LinkedIn': (1200, 627),
#     'Twitter': (1200, 600),
#     'Instagram': (1080, 1080)
# }

# def resize_and_pad_image_for_platform(input_path, output_path, platform):
#     """
#     Resizes and pads an image based on the platform's size requirements.
#     For Google Merchant, ensure the image is larger than 100x100 and the product occupies 75% of the view.
#     """
#     target_size = size_requirements.get(platform)
#     if not target_size:
#         print(f"Platform '{platform}' not recognized.")
#         return

#     target_width, target_height = target_size

#     try:
#         with Image.open(input_path) as img:
#             original_width, original_height = img.size

#             if platform == 'GoogleMerchant':
#                 # Ensure the image meets the minimum size requirement
#                 if original_width > target_width and original_height > target_height:
#                     # Calculate the resize factor to make the product occupy 75% of the viewing area
#                     resize_factor = 0.75
#                     new_width = int(original_width * resize_factor)
#                     new_height = int(original_height * resize_factor)
#                     if new_width < target_width or new_height < target_height:
#                         # Ensure the image is not resized below the minimum dimensions
#                         ratio = max(target_width / original_width, target_height / original_height)
#                         new_size = (int(original_width * ratio), int(original_height * ratio))
#                     else:
#                         new_size = (new_width, new_height)
#                 else:
#                     # Resize the image to meet the minimum size requirement if it's too small
#                     ratio = max(target_width / original_width, target_height / original_height)
#                     new_size = (int(original_width * ratio), int(original_height * ratio))
#             else:
#                 # Calculate the new size, preserving the aspect ratio for other platforms
#                 ratio = min(target_width / original_width, target_height / original_height)
#                 new_size = (int(original_width * ratio), int(original_height * ratio))
            
#             # Resize the image
#             img = img.resize(new_size, Image.Resampling.LANCZOS)

#             if platform != 'GoogleMerchant':
#                 # Create a new image with a white background for non-Google Merchant platforms
#                 new_img = Image.new("RGB", (target_width, target_height), (255, 255, 255))
#                 # Paste the resized image onto the center of the new image
#                 new_img.paste(img, ((target_width - new_size[0]) // 2, (target_height - new_size[1]) // 2))
#                 img = new_img

#             # Ensure the output directory exists
#             output_dir = os.path.dirname(output_path)
#             os.makedirs(output_dir, exist_ok=True)

#             # Save the new image
#             img.save(output_path)
#             print(f"Image saved to {output_path}")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Define the base directories
# vendor_og_dir = 'Vendor_OG_Images/LibertyTableTop'
# vendor_resized_dir = 'Vendor_Resized_Images/LibertyTableTop'

# for product_id in os.listdir(vendor_og_dir):
#     product_dir = os.path.join(vendor_og_dir, product_id)
#     print(product_id)
#     # if os.path.isdir(product_dir):
#     #     for image_name in os.listdir(product_dir):
#     #         input_path = os.path.join(product_dir, image_name)
#     #         if os.path.isfile(input_path):
#     #             for platform, _ in size_requirements.items():
#     #                 output_path = f"{vendor_resized_dir}/{product_id}/{platform}/{image_name}"
#     #                 resize_and_pad_image_for_platform(input_path, output_path, platform)

    



