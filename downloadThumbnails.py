import os
import json
import requests

# Assuming your JSON data is stored in a file called 'products.json'
json_file_path = 'JSON/LibertyTableTopProducts.json'

def download_image(image_url, save_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)

def process_products(json_file_path):
    with open(json_file_path, 'r') as file:
        products = json.load(file)

    for product in products:
        product_id = product['id']
        image_url = product['thumbnail']['url']

        # Create a directory for the product ID
        dir_path = os.path.join('Vendor_OG_Images/LibertyTableTop', str(product_id))
        os.makedirs(dir_path, exist_ok=True)

        # Define the path where the image will be saved
        image_file_name = image_url.split('/')[-1]  # Extracts the file name from the URL
        save_path = os.path.join(dir_path, image_file_name)

        # Download and save the image
        download_image(image_url, save_path)
        print(f"Downloaded {image_file_name} to {dir_path}")

# Replace 'products.json' with the path to your actual JSON data file
process_products(json_file_path)
