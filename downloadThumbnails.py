import os
import json
import requests

# Assuming your JSON data is stored in a file called 'products.json'
json_file_path = 'JSON/KR_Creative.json'

# Extract name for folder creation
base_name = os.path.basename(json_file_path)
json_file_name = os.path.splitext(base_name)[0]


def download_image(image_url, save_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)

def process_products(json_file_path):
    with open(json_file_path, 'r') as file:
        products = json.load(file)

    count = 0
    for product in products:
        count += 1
        product_id = product['id']
        image_url = product['thumbnail']['url']

        # Create a directory for the product ID
        dir_path = os.path.join(f'Vendor_OG_Images/{json_file_name}', str(product_id))
        os.makedirs(dir_path, exist_ok=True)

        # Define the path where the image will be saved
        image_file_name = os.path.splitext(image_url.split('/')[-1])[0] + '.png'
        #print(image_file_name)
        save_path = os.path.join(dir_path, image_file_name)

        # Download and save the image
        download_image(image_url, save_path)
        print(f"Downloaded {image_file_name} to {dir_path}")
    print(count)

# Replace 'products.json' with the path to your actual JSON data file
process_products(json_file_path)
