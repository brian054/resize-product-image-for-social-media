import json
from helpers import *

# Define the list of strings for the fifth column
social_media_platforms = ["Facebook", "Instagram", "Twitter", "LinkedIn", "GoogleMerchant", "Pinterest"] 

vendor = 'UPM'

# Read the JSON data
with open(f'JSON/{vendor}.json') as json_file:
    data = json.load(json_file)

# Create JSON for import
json_data = []
for item in data:
    product_id = item['id']
    #print("ID: ", product_id)
    product_name = item['name']

    # Thumbnail Setup
    thumbnail_id = item['thumbnail']['id']
    thumbnail_local_path = f'/Users/brian/Desktop/Python/Image-Resizer/Vendors_Resized_Images/{vendor}/{product_id}/RetailSite_{product_id}.png'
    thumbnail_entry = {
        "id": thumbnail_id,
        "local_path": thumbnail_local_path 
    }

    # Gallery Image JSON prep
    gallery_images_json = []
    gallery_images = item['images']
    if gallery_images is not None:
        #print("Gallery Item: ", gallery_item)
        count = 0
        for image in gallery_images:
            # I know you're violating DRY here, but we can fix later I need this to work properly first
            image_url = image['url']
            print(f"attempting gallery image #{count}")
            count += 1
            if openImageURL(image_url) == True and isSquareImage(image_url) == False:  
                image_id = image['id']
                #print("Image ID: ", image_id)
                local_path = f'/Users/brian/Desktop/Python/Image-Resizer/Vendors_Resized_Images/{vendor}/{product_id}/GalleryImages/{image_id}.png'
                new_gallery_image = {
                    'image_id': image_id,
                    'local_path': local_path
                }
                gallery_images_json.append(new_gallery_image)

    # Social Media JSON Prep
    social_media_json = []
    for platform in social_media_platforms:
        metaTitle = item['seo']['metaTitle']
        metaDescription = item['seo']['metaDescription']
        socialNetwork = platform
        local_path = f'/Users/brian/Desktop/Python/Image-Resizer/Vendors_Resized_Images/{vendor}/{product_id}/{platform}_{product_id}.png'

        social_media_entry = {
            'metaTitle': metaTitle,
            'metaDescription': metaDescription,
            'socialNetwork': socialNetwork,
            'local_path': local_path
        }
        social_media_json.append(social_media_entry)

    # now for the grand finale put it all together
    single_row_json = {
        'product_id': product_id,
        'product_name': product_name,
        'thumbnail': thumbnail_entry,
        'galleryImages': gallery_images_json,
        'seo': {'socialMedia': social_media_json}
    }
    json_data.append(single_row_json)

# Write to JSON file to be used for import in Javascript
json_fileName = f'JSON/ReadyForImport/{vendor}.json'
with open(json_fileName, 'w') as file:
    json.dump(json_data, file, indent=4)
    
print(f"JSON file '{json_fileName}' has been created.")


