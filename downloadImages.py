import os
import json
import requests
from helpers import *

def download_image(image_url, save_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)


def process_products(json_file_path):
    with open(json_file_path, "r") as file:
        products = json.load(file)

    count = 0
    for product in products:
        count += 1

        # if the thumbnail doesn't exist, move on to the next entry
        if product["thumbnail"] == None:
            continue

        product_id = product["id"]
        image_url = product["thumbnail"]["url"]
        image_id = product["thumbnail"]["id"]

        # Create a directory for the product ID
        dir_path = os.path.join(f"Vendor_OG_Images/{json_file_name}", str(product_id))
        os.makedirs(dir_path, exist_ok=True)

        # Define the path where the image will be saved
        # image_file_name = os.path.splitext(image_url.split('/')[-1])[0] + '.png'

        image_file_name = str(image_id) + ".png"
        # print("Imagefilename: ", image_file_name)

        # print(image_file_name)
        save_path = os.path.join(dir_path, image_file_name)

        # Download and save the image
        download_image(image_url, save_path)
        print(f"Downloaded {image_file_name} to {dir_path}")
    print(count)


def download_gallery_images(json_data):
    with open(json_data, "r") as file:
        items = json.load(file)

    count = 0
    for item in items:
        folder_name = str(item["id"])
        if item["images"] is not None:
            os.makedirs(
                f"Vendor_OG_Images/{json_file_name}/{folder_name}/GalleryImages/",
                exist_ok=True,
            )
            for image in item["images"]:
                image_url = image["url"]
                # if we can actually open the image, and the image is not already a square ratio, download and save to OG image dir
                if (
                    openImageURL(image_url) == True
                    and isSquareImage(image_url) == False
                ):
                    image_id = str(image["id"])  # for the name
                    file_name = os.path.join(
                        f"Vendor_OG_Images/{json_file_name}/{folder_name}/GalleryImages/",
                        image_id + ".png",
                    )
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        with open(file_name, "wb") as f:
                            f.write(response.content)
                        print(f"Downloaded Gallery Image from {image_url}")
                    else:
                        print(f"Failed to download image {image_id} from {image_url}")
                else:
                    print(
                        "Gallery image either can't be opened or it is already a square ratio: "
                        + str(count)
                    )
                    count += 1


# Download Thumbnail and Gallery Images - can definitely combine these functions
# DONT COMBINE - sometimes the response just breaks so sometimes need to download gallery img's separately
# vendor = 'Edith'



#createJSONFiles(vendors)

# YO YO MAKE SURE YOU RUN createJSONFIles() and fill in the data BEFORE running the for loop
for vendor in vendors:
    json_file_path = f"JSON/{vendor}.json"

    # Extract name for folder creation
    base_name = os.path.basename(json_file_path)
    json_file_name = os.path.splitext(base_name)[0]

    process_products(json_file_path)
    download_gallery_images(json_file_path)
