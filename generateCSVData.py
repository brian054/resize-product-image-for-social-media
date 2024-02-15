# Generate the necessary CSV data to be put on our social media CSV
import json
import csv

# Define the list of strings for the fifth column
social_media_platforms = ["Facebook", "Instagram", "Twitter", "LinkedIn", "Google Merchant"]

# Read the JSON data
with open('JSON/AuburnLeather.json') as json_file:
    data = json.load(json_file)

# Prepare data for CSV
csv_data = []
for item in data:
    for platform in social_media_platforms:
        row = [
            item['id'],
            item['name'],
            item['seo']['metaTitle'],
            item['seo']['metaDescription'],
            platform
        ]
        csv_data.append(row)

# Write data to CSV
csv_filename = 'CSV/AuburnLeather.csv'
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'name', 'metaTitle', 'metaDescription', 'socialNetwork'])
    writer.writerows(csv_data)

print(f"CSV file '{csv_filename}' has been created.")

