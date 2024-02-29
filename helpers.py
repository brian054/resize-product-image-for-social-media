import requests
import os
import json
from PIL import Image
from io import BytesIO


def openImageURL(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # throw exception if http error
        image = Image.open(BytesIO(response.content))
        return True
    except Exception as e:
        print("Fail: ", e)
        return False


def isSquareImage(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    width, height = img.size
    return width == height

# Create JSON files for a list of vendor names
def createJSONFiles(vendors):
    for vendor in vendors:
        file_path = os.path.join('JSON', f'{vendor}.json')
        with open(file_path, 'w') as json_file:
            json.dump('', json_file)

vendors = [
    "XenaTherapies",
    "AuburnLeathercrafters",
    "NewCreationsVictorian",
    "SunHeat",
    "HuberdShoeGrease",
    "LetsGel",
    "BeWellLabs",
    "DevourTools",
    "BarrelArt",
    "MicrobeFiber",
    "BubMutha",
    "USACoasters",
    "SpaPure",
    "BetterWhey"
]
# createJSONFiles(vendors)

# working
url = "https://madeinusastrapiblob.blob.core.windows.net/uploads/assets/13194_4_7d1a697049"

# non-working
url2 = "https://madeinusastrapiblob.blob.core.windows.net/uploads/assets/13133_3_36528b490a"

# ex usage
# print(openImageURL(url))
# openImageURL("https://madeinusastrapiblob.blob.core.windows.net/uploads/assets/13194_4_7d1a697049")

# print(isSquareImage("https://madeinusastrapiblob.blob.core.windows.net/uploads/assets/entrepreneur_briefcase_T_670_NVY_657922a0ce.jpg"))
# print(isSquareImage("https://madeinusastrapiblob.blob.core.windows.net/uploads/assets/entrepreneur_briefcase_T_670_WAX_GRY_219f576e71.png"))
# print(isSquareImage("https://madeinusastrapiblob.blob.core.windows.net/uploads/assets/entrepreneur_briefcase_T_670_WAX_KHK_a96c358b5e.jpg"))
# print(isSquareImage("https://madeinusastrapiblob.blob.core.windows.net/uploads/assets/entrepreneur_briefcase_T_670_ROY_463e6b978f.png"))
#print(isSquareImage(""))
