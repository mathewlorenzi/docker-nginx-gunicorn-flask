import os
import requests
# import cv2
from datetime import datetime
import json
import base64
import time
import threading

#https://stackoverflow.com/questions/60091029/python-requests-post-image-with-json-data

SAMPLE_IMAGE="sample.png"
MAIN_URL = "http://127.0.0.1:5000"
camIds = ["peter", "paul", "jack", "UNKNOWN"]


class SimulatorClientPostImage(threading.Thread):
  
    def __init__(self, camId:str, intervalSec):
        threading.Thread.__init__(self)
        print("SimulatorClientPostImage")
        self.intervalSec = intervalSec
        self.output_pipe = None
        self.camId = camId
        with open(SAMPLE_IMAGE, "rb") as f:
            im_bytes = f.read()  
            # string_img = base64.b64encode(cv2.imencode("sample.png", img)[1]).decode()
            self.im_b64 = base64.b64encode(im_bytes).decode("utf8")
        self._stop_event = threading.Event()
    def stop(self):
        self._stop_event.set()
        return self._stop_event.is_set()
    #def stopped(self):
    def run(self):
        print('SimulatorClientPostImage camId', camId)
        while(True):
            url = MAIN_URL+"/image"
            content = {'image': self.im_b64, 'nameId': self.camId, 'usedUrl': url}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            response = requests.post(url, data=json.dumps(content), headers=headers)
            print(response)        
            time.sleep(self.intervalSec)

def populate_fake_images():
    # img = cv2.imread("sample.png")

    with open("sample.png", "rb") as f:
        im_bytes = f.read()  
        # string_img = base64.b64encode(cv2.imencode("sample.png", img)[1]).decode()
        im_b64 = base64.b64encode(im_bytes).decode("utf8")

        for camId in camIds:
            print(camId)
            for nb in range(10):
                url = MAIN_URL+"/image"
                content = {'image': im_b64, 'nameId': camId, 'usedUrl': url}
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                response = requests.post(url, data=json.dumps(content), headers=headers)

                print(response)

                time.sleep(1)

# populate_fake_images()
# exit(0)

# keep posting fake image every 10 intervalSec
intervalSec = 15
threads = []
for camId in camIds:
    thread = SimulatorClientPostImage(camId=camId, intervalSec=intervalSec)
    thread.start()
    threads.append(thread)

# and keep in the same time, getting what has been posted
while True:
    active_client_cam = requests.get(url=MAIN_URL+"/active_client_cam")
    json_data_res = json.loads(active_client_cam.content.decode("utf-8"))
    json_data = json_data_res.get("data")
    for el in json_data:
        camId = str(el)
        
        print("...request")
        lastimage = str(requests.get(MAIN_URL+"/last_image/"+camId))#.content.decode("utf-8"))
        '''url_get_image_filename = MAIN_URL+"/last_image_filename/"+camId
        url_get_image_content = MAIN_URL+"/last_image_content/"+camId
        url_get_image_isuploaded = MAIN_URL+"/is_last_image_uploaded/"+camId

        getimage_filename = str(requests.get(url_get_image_filename).content.decode("utf-8"))
        getimage_isuploaded1 = str(requests.get(url_get_image_isuploaded).content.decode("utf-8"))
        getimage_content = requests.get(url_get_image_content)
        getimage_isuploaded2 = str(requests.get(url_get_image_isuploaded).content.decode("utf-8"))

        print(camId, "filename:", getimage_filename, "isuploaded:", getimage_isuploaded1, getimage_isuploaded2)
        
        filenameWithStamp = os.path.splitext(getimage_filename)[0]
        filenameExt = os.path.splitext(getimage_filename)[1]
        current_image_path = os.path.join("todel_"+str(camId)+filenameExt)
        # print("current_image_path:", current_image_path)

        # OK, just for debug, saving current image at same location always
        # print(current_image_path)
        with open(current_image_path, mode="wb") as fout:
            fout.write(getimage_content.content)
        '''

    time.sleep(5)