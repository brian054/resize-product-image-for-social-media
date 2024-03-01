import os

# For the custom import I need to rename all the OG images
# the same, so extracting all those names for easy copy and paste

# WAIT HOLLUP
# they're all jpegs instead of pngs so why not just store the 2 images
# in the same folder, then instead of manually renaming all of them you can just
# run a quick script to rename everything based on the .png name. Awesome 

# Use this script to rename all the new jpegs with the png names before removing
# the pngs and then convert all the images to png (99.9% sure resizing code already doing this for us)

# Go through BestNest folder

# Run through each folder in the vendor folder, rename the new OG image based on the png's name
def rename_images(dir):
    for folder in os.listdir(dir):
        folder_path = os.path.join(dir, folder)
        if os.path.isdir(folder_path):
            png_file = None
            other_file = None

            # Find the png file
            for file in os.listdir(folder_path):
                if file.endswith('.png'):
                    png_file = file
                else:
                    other_file = file

            # Rename
            if png_file and other_file:
                base_name = os.path.splitext(png_file)[0]
                if base_name.isdigit():
                    new_name = base_name + os.path.splitext(other_file)[1]
                    os.rename(os.path.join(folder_path, other_file), os.path.join(folder_path, new_name))
                    print(f"Renamed {other_file} to {new_name}")

def delete_pngs(dir):
    for folder in os.listdir(dir):
        folder_path = os.path.join(dir, folder)
        if os.path.isdir(folder_path):
            png_file = None

            # Find the png file
            for file in os.listdir(folder_path):
                if file.endswith('.png'):
                    png_file = file

            # Delete png
            if png_file:
                os.remove(os.path.join(folder_path, png_file))


dir = 'Vendor_OG_Images/BestNest'
#rename_images(dir)
#delete_pngs(dir)












