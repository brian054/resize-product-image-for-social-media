import requests
from PIL import Image
from io import BytesIO

def openImageURL(url):
    try:
        response = requests.get(url)
        response.raise_for_status() # throw exception if http error
        image = Image.open(BytesIO(response.content))
        return True
    except Exception as e:
        print("Fail: ", e)
        return False


# working
url = "https://madeinusastrapiblob.blob.core.windows.net/uploads/assets/13194_4_7d1a697049"

# non-working
url2 = "https://madeinusastrapiblob.blob.core.windows.net/uploads/assets/13133_3_36528b490a"

# ex usage
#print(openImageURL(url))
#openImageURL("https://madeinusastrapiblob.blob.core.windows.net/uploads/assets/13194_4_7d1a697049")