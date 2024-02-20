# Generate the necessary CSV data to be put on our social media CSV
import json
#import csv

# Define the list of strings for the fifth column
social_media_platforms = ["Facebook", "Instagram", "Twitter", "LinkedIn", "Google Merchant"]

vendor = 'KR_Creative'

# Read the JSON data
with open(f'JSON/{vendor}.json') as json_file:
    data = json.load(json_file)

# Prepare data for CSV
#csv_data = []
# Changing to JSON instead, easier import 
json_data = []
for item in data:
    for platform in social_media_platforms:
        id = item['id']
        row = {
            'id': id,
            'name': item['name'],
            'metaTitle': item['seo']['metaTitle'],
            'metaDescription': item['seo']['metaDescription'],
            'socialNetwork': platform,
            'local_path': f'/Users/brian/Desktop/Python/Image-Resizer/Vendors_Resized_Images/{vendor}/{id}/{platform}_{id}.png',
        }
        json_data.append(row)
        # row = [
        #     id,
        #     item['name'],
        #     item['seo']['metaTitle'],
        #     item['seo']['metaDescription'],
        #     platform,
        #     f'/Users/brian/Desktop/Python/Image-Resizer/Vendors_Resized_Images/{vendor}/{id}/{platform}_{id}.png'
        # ]
        #csv_data.append(row)

# Write to CSV
# csv_filename = f'CSV/{vendor}.csv'
# with open(csv_filename, mode='w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['id', 'name', 'metaTitle', 'metaDescription', 'socialNetwork', 'local path'])
#     writer.writerows(csv_data)
# Write to JSON instead
json_fileName = f'JSON/ReadyForImport/{vendor}.json'
with open(json_fileName, 'w') as file:
    json.dump(json_data, file, indent=4)

# ----------------------------------------
    
# Read in gallery JSON data
with open(f'JSON/{vendor}_Gallery.json') as json_file:
    gallery_data = json.load(json_file)
    
# # Prepare data for CSV
# csv_gallery_data = []
# Prep data for new JSON
json_gallery_data = []
for item in gallery_data:
    #print("Images: ", item['images'])
    if item['images'] is None:
        continue # move on to next iteration

    product_id = item['id']
    product_name = item['name']
    for galleryImage in item['images']:
        #print("GalleryImage: ", galleryImage) # contains id and url
        row = {
            'product_id': product_id,
            'product_name': product_name,
            'image_id': galleryImage['id'],
            'local_path': f'/Users/brian/Desktop/Python/Image-Resizer/Vendors_Resized_Images/{vendor}/{product_id}/GalleryImages/{galleryImage["id"]}.png',
        }
        json_gallery_data.append(row)
        # image_id = galleryImage['id']
        # row = [
        #     product_id,
        #     product_name,
        #     image_id,
        #     #item['images'],
        #     f'/Users/brian/Desktop/Python/Image-Resizer/Vendors_Resized_Images/{vendor}/{product_id}/GalleryImages/{image_id}.png'
        # ]
        # csv_gallery_data.append(row)

# Write gallery data to new CSV
# csv_gallery_filename = f'CSV/{vendor}_Gallery.csv'
# with open(csv_gallery_filename, mode='w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['product_id', 'product_name', 'image_id', 'local_path'])
#     writer.writerows(csv_gallery_data)
# Write to CSV instead
json_gallery_filename = f'JSON/ReadyForImport/{vendor}_Gallery.json'
with open(json_gallery_filename, 'w') as file:
    json.dump(json_gallery_data, file, indent=4)

#print(f"CSV file '{csv_filename}' has been created.")
print(f"JSON file '{json_fileName}' and '{json_gallery_filename}' has been created.")


