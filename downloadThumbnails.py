import os
import json
import requests

# Download Gallery Img's - just make a new function 
# Just put them in Vendor_OG_Images/Vendor/productID/GalleryImgs/
#
# Then generateCSVData for those GalleryImg's
#   = where they'll be saved??? 
#   = then resize them using the same algorithm that the retailsite images are 
#   = using. At that point, we're good just need to generate maybe 10 
#   = vendors in advance, then look into importing and talk about in stand up

json_file_path = 'JSON/AuburnLeather.json'

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

def download_gallery_images(json_data):
    with open(json_data, 'r') as file:
        items = json.load(file)

    for item in items:
        folder_name = str(item['id'])
        os.makedirs(f'Vendor_OG_Images/{json_file_name}/{folder_name}/GalleryImages/', exist_ok=True)
        for image in item['images']:
            image_url = image['url']
            image_id = str(image['id']) # for the name
            file_name = os.path.join(f'Vendor_OG_Images/{json_file_name}/{folder_name}/GalleryImages/', image_id + '.png')
            response = requests.get(image_url)
            if response.status_code == 200:
                with open(file_name, 'wb') as f:
                    f.write(response.content)
            else:
                print("Failed to download image {image_id} from {image_url}")

process_products(json_file_path)
json_gallery = 'JSON/AuburnLeather_Gallery.json'
download_gallery_images(json_gallery)
