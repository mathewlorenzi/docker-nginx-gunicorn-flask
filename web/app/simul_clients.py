
import requests
# import cv2
from datetime import datetime
import json
import base64
import time

#https://stackoverflow.com/questions/60091029/python-requests-post-image-with-json-data

camIds = ["peter", "paul", "jack", "UNKNOWN"]
def populate_fake_images():
    # img = cv2.imread("sample.png")

    with open("sample.png", "rb") as f:
        im_bytes = f.read()  
        # string_img = base64.b64encode(cv2.imencode("sample.png", img)[1]).decode()
        im_b64 = base64.b64encode(im_bytes).decode("utf8")

        for camId in camIds:
            print(camId)
            for nb in range(10):
                url = "http://127.0.0.1:5000/image"
                content = {'image': im_b64, 'nameId': camId, 'usedUrl': url}
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                response = requests.post(url, data=json.dumps(content), headers=headers)

                print(response)

                time.sleep(1)

populate_fake_images()