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

# Don't get so stuck on the overall picture right now, just make it work and
# then we can figure out the best way to go about importing the resized. 

from PIL import Image, ImageOps
import os

# Define the size requirements for each platform
size_requirements = {
    'google_non_apparel': (100, 100),
    'google_apparel': (250, 250),
    'facebook': (1200, 630),
    'linkedin': (1200, 627),
    'twitter': (1200, 600),
    'instagram': (1080, 1080)
}

def resize_and_pad_image_for_platform(input_path, output_path, platform):
    """
    Resizes and pads an image based on the platform's size requirements,
    with specific logic for Google non-apparel and apparel to ensure the image
    is larger than minimum size requirements and as close to 1:1 aspect ratio as possible.

    Args:
    - input_path: The path to the input image.
    - output_path: The path where the resized and padded image will be saved.
    - platform: The name of the platform (e.g., 'google_non_apparel', 'google_apparel', 'facebook', 'linkedin', 'twitter', 'instagram').
    """

    # Get the required size for the platform
    target_size = size_requirements.get(platform)
    if not target_size:
        print(f"Platform '{platform}' not recognized.")
        return

    target_width, target_height = target_size

    try:
        with Image.open(input_path) as img:
            original_width, original_height = img.size
            
            # Check if the image is already larger than the minimum requirement
            if platform in ['google_non_apparel', 'google_apparel'] and original_width > target_width and original_height > target_height:
                # Resize to get as close to 1:1 aspect ratio as possible
                new_size = max(original_width, original_height)
                img = img.resize((new_size, new_size), Image.Resampling.LANCZOS)
            else:
                # Calculate the new size, preserving the aspect ratio
                ratio = min(target_width / original_width, target_height / original_height)
                new_size = (int(original_width * ratio), int(original_height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)

            # For non-Google platforms, or if the Google image is resized above, pad to target dimensions
            if platform not in ['google_non_apparel', 'google_apparel']:
                # Create a new image with a white background and the target size
                new_img = Image.new("RGB", (target_width, target_height), (255, 255, 255))
                # Paste the resized image onto the center of the new image
                new_img.paste(img, ((target_width - new_size[0]) // 2, (target_height - new_size[1]) // 2))
                img = new_img

            # Check if the output directory exists, create it if not
            output_dir = os.path.dirname(output_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
                print(f"Created directory {output_dir}")

            # Save the new image
            img.save(output_path)
            print(f"Image saved to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage for Google non-apparel
# resize_and_pad_image_for_platform('path/to/your/image.jpg', 'path/to/your/resized_image_google_non_apparel.jpg', 'google_non_apparel')
# resize_and_pad_image_for_platform('images/testImage.jpeg', 'resizedImages/testImage/testImageFB.jpeg', 'facebook')
# resize_and_pad_image_for_platform('images/testImage.jpeg', 'resizedImages/testImage/testImageIG.jpeg', 'instagram')

for key, value in size_requirements.items():
    output_path = f"resizedImages/testImage/testImage_{key}.jpeg"
    resize_and_pad_image_for_platform('images/testImage.jpeg', output_path, key)
    # print(key)
    # print(value)

# Example usage
# resize_image('images/testImage.jpeg', 'resizedImages/testImage/testImage.jpeg', 'facebook')



