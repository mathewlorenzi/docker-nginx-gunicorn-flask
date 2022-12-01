# camera -> capture -> POST(/image) -------> server record last image 
#                                   <------- returns last result (from ecovision)
#                                                               <----------  GET(/lastimage) <- ecovision
#                                            returns last image -----------> ecovision
#                                                   last result <----------- POST(/result) ecovision

from datetime import datetime
import os
import sys
# import base64
from base64 import b64encode
import logging
from time import sleep
from charset_normalizer import detect
import psutil
import threading

# import io
#import cStringIO
from PIL import Image, ImageDraw

# TODO remove a client cam when the webpage /camera is closed

# in docker, local files cannot be found: add current path to python path:
file_path = os.path.dirname(os.path.realpath(__file__))
if file_path not in sys.path:
    sys.path.insert(1, file_path)
# printRootStructure(dirname=sys.path[0], indent=0)

from flask import Flask, render_template, request, jsonify, json#, flash send_from_directory
from buffer_images import STR_UNKNOWN, load_sample, BufferClients, NOSAVE, SAVE_WITH_TIMESTAMPS, SAVE_WITH_UNIQUE_FILENAME
import requests

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# TODO log rotate
#logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
#logging.basicConfig(level=logging.DEBUG, format=f'%(asctime)s %(levelname)s : %(message)s')
logging.basicConfig(level=logging.INFO, format=f'%(asctime)s %(levelname)s : %(message)s')
logger = logging.getLogger(__name__)
logger.warning('Start') 
# printRootStructure(dirname='./',indent=0)
#app.debug = True

MODE_SAVE_TO_DISK = NOSAVE
#MODE_SAVE_TO_DISK = SAVE_WITH_UNIQUE_FILENAME

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.abspath( os.path.join(APP_ROOT, "..", "..", "database_clients_camera") )
logger.debug("check output folder: "+str(OUTPUT_PATH))
if os.path.exists(OUTPUT_PATH) is False:
    os.mkdir(OUTPUT_PATH)

bufferClients = BufferClients(MODE_SAVE_TO_DISK=MODE_SAVE_TO_DISK, database_main_path_all_clients=OUTPUT_PATH, debugapp=False)
if bufferClients.initSucc is False:
    logger.debug("BufferClients initialisation failed: " + bufferClients.initMsg)
    exit(1)

# V1 ecovisionResults => old2.py
# v2 ecovisionResults
ecovisionResults = BufferClients(MODE_SAVE_TO_DISK=MODE_SAVE_TO_DISK, database_main_path_all_clients=OUTPUT_PATH, debugapp=False)
if ecovisionResults.initSucc is False:
    logger.debug("ecovisionResults initialisation failed: " + ecovisionResults.initMsg)
    exit(1)

# populate_fake_images(OUTPUT_PATH=OUTPUT_PATH, sampleImagePath="sample.png")
# exit(1)
# uri_result = load_sample("todel.png")

class WatchActiveClients(threading.Thread):
    def __init__(self, maxDeltaAge: int=30, intervalSec: int=30, debug: bool=False):
        threading.Thread.__init__(self)
        self.output_pipe = None
        self.intervalSec = intervalSec
        self.maxDeltaAge = maxDeltaAge
        self.debug = debug
        logging.info("WatchActiveClients")
        self._stop_event = threading.Event()
    def stop(self):
        self._stop_event.set()
    def stopped(self):
        return self._stop_event.is_set()  
    def run(self):
        print('starting client watcher')
        while(True):
            deletedOneClient = True
            while deletedOneClient is True:
                deletedOneClient = bufferClients.deleteOneTooOldConnectedClient(maxDeltaAge=self.maxDeltaAge, debug=self.debug)
            deletedOneClient = True
            while deletedOneClient is True:
                deletedOneClient = ecovisionResults.deleteOneTooOldConnectedClient(maxDeltaAge=self.maxDeltaAge, debug=self.debug)
            self._stop_event.wait(self.intervalSec) # check every N sec                
        print('end client watcher')

watchActiveClients = WatchActiveClients()
watchActiveClients.start()
#watchActiveClients.join() # this make the main thread to wait for it to end (run functin ends or stop _stop_event line is done)

@app.route("/hello")
def hello():
    logger.debug("/hello endpoint: pid: " + str(os.getpid()))
    #print("[DEBUG]/hello endpoint: pid: ", str(os.getpid()))
    data = {"data": "Hello Camera3"}
    # uri_result = load_sample("sample.png")
    return jsonify(data)

@app.route("/camera", methods=['GET'])
def upload():
    logger.debug("/camera endpoint" + str(request.method))
    return render_template("camera.html", usedUrl = str(request.url_root), nameId = STR_UNKNOWN)#, uri_result=uri_result)

@app.route('/update_values', methods= ['GET'])
def update_values():
    per_cpu = psutil.cpu_percent(percpu=True)
    mean_cpu = 0.0
    counter=0
    for idx, usage in enumerate(per_cpu):
        print(f"CORE_{idx+1}: {usage}%")
        mean_cpu += float(usage)
        counter+=1
    if counter > 0:
        mean_cpu /= float(counter)
    cpu=round(mean_cpu)

    mem_usage = psutil.virtual_memory().percent
    print("ram", mem_usage)
    ram=round(mem_usage)

    disk_usage = psutil.disk_usage("./").percent
    print("disk_usage", disk_usage)
    disk=round(disk_usage)

    return jsonify(cpu=cpu, ram=ram, disk=disk)

# v1 ecovisionResults
# @app.route("/result/<string:camId>", methods=['POST'])
# def result(camId: str):
#     # bytes to string
#     jsonstr = request.data.decode('utf8')
#     print(" ........ camId ", camId)
#     # print(" ........ result ->", jsonstr, "<-")
#     #print(type(jsonstr))
#     # string to json
#     data = json.loads(jsonstr)

#     # v1 ecovision
#     # ecovisionResults.trackResultsImage[camId] = data['png']
    

#     return ("ok", 200)

# v1 ecovision
'''@app.route("/result_image2/<string:camId>", methods=['GET'])
def result_image2(camId: str):
    print("/result_image2")
    logger.debug("/result_image2 endpoint")
    if camId in ecovisionResults.trackResultsImage:
        return (ecovisionResults.trackResultsImage[camId], 200)
    else:
        return ("ko: image result2 not ready yet for " + camId, 204)
'''

# if using mydb in another docker: it worked
@app.route("/test_mydb")
def test_mydb():
    logger.debug("/test_mydb 127.0.0.1:5001 ")
    response = requests.get("http://mydb:5001")
    logger.debug("response:" + str(response.status_code) + ", content: " + str(response.content))
    return (response.content, 200)

@app.route('/', methods=['GET', 'POST'])
def mainroute():
    logger.debug("/ main endpoint: pid: " + str(os.getpid()))
    if request.method == 'GET':
        return render_template('form.html')
    elif request.method == 'POST':
        logger.debug("redirect to camera with name: " + request.form['username'] + " from " + request.url_root)
        return render_template('camera.html', usedUrl = str(request.url_root), nameId = request.form['username'])#, uri_result=uri_result)

def record_image_or_result(inputBufferClient: BufferClients, info: str):
    # bytes to string
    jsonstr = request.data.decode('utf8')
    # if info=="result":
    #     print(jsonstr)
    # string to json
    data = json.loads(jsonstr)
    # we could go further into beauty: s = json.dumps(data, indent=4, sort_keys=True)

    # TODO check json fields
    
    imagestr = data["image"]
    nameId = data["nameId"]
    usedUrl = data["usedUrl"]
    logger.debug("/image: nameId: " + nameId + " usedUrl: " + usedUrl)
    if isinstance(imagestr, str) is False or isinstance(nameId, str) is False:
        logger.error("/image: nameId is not a string:" + str(nameId))
        return ("KO: nameId is not a string", 400)
    else:
        # look if existing active camera
        indexClient = bufferClients.getClientIndex(nameId=nameId)
        if indexClient is None:
            logger.info("/image: nameId:" + nameId + " new client")
            (_msg, indexClient) = bufferClients.insertNewClient(nameId=nameId)
            if indexClient is None:
                errMsg = "/image: nameId:" + nameId + " failed inserting new client " + _msg
                logger.error(errMsg)
                return (errMsg, 400)

        # check really necessary ?
        indexClient = bufferClients.getClientIndex(nameId=nameId)
        if indexClient is None:
            logger.error("/image: nameId:" + nameId + " failed finding client")
            return ("KO: Failed finding client or inserting new client " + nameId, 400)
        
        logger.debug("/image: nameId:" + nameId + " indexClient: " + str(indexClient))


        # while(bufferClients.buff[indexClient].lockOnUpload is True){
        #     logger.info("/image: lock active, wait a bit, for camId" + nameId)
        #     time.sleep(1)
        # }
        # lockOnUpload = False
        # imageToBeUploaded = AppImage()

        (msg, succ) = bufferClients.buff[indexClient].insertNewImage(logger=logger, imageContent=imagestr)
        if succ is False:
            logger.error(msg)
            return ("KO: failed saving new image", 400)
        else:
            logger.info(msg)

            # camId = nameId
            # logger.debug("/result_image2 endpoint")
            # v1
            # if camId in ecovisionResults.trackResultsImage:
            #     return (ecovisionResults.trackResultsImage[camId], 200)
            # else:
            #     return ("ok but image result from ecovision not ready yet for " + camId, 202)
            # v2 return a blank image if not ready
            # indexECO = bufferEcovisionResults.getClientIndex(nameId=nameId)
            # if indexECO is None:
            #     logger.error("/image: nameId:" + nameId + " failed finding client in ecovision results")
            #     return (HERE blank image, 202)
            # bufferEcovisionResults.buff[indexECO].get last image
        
            # HERE    

            return ("OK", 200)
    return ("OK", 200)

# this is called within the camera.html: var url = 'https://www.ecovision.ovh:81/image';sam
# the camera, javascript post its image to this endpoint
@app.route("/image", methods=['POST'])
def image():
    (msg, status) = record_image_or_result(inputBufferClient=bufferClients, info="input")
    # the camera.html (client) exects the result as a reply or a blank image if ecovision did not reply a fresh result yet
    if status != 200:
        with open( "blank.png", mode="rb" ) as f:
            imageContent = f.read()
            logger.info("sending a blank image as a reply")
            print(" =================================== ")
            return (imageContent, status)
        return ("KO wrong path to blank image", 400)
    else:
        camId = TODO to retrie it from record_image_or_result
        and add some info in inputBufferClients class to distinguish from result or input images 
        (content, status2) = lastsample(camId = camId, inputBufferClient=ecovisionResults, take_care_of_already_uploaded=True)

# reply to ecovision
@app.route("/result", methods=['POST'])
def result():
    return record_image_or_result(inputBufferClient=ecovisionResults, info="result")

def lastsample(camId: str, inputBufferClient: BufferClients, take_care_of_already_uploaded: bool=True):
    # called by httpclient or ecovision :
    # prog_v2.h
    #   httpRequestUtils getRequester;
    #   httpRequestUtils postRequester; 
    # prog_exe_v2.cpp
    #   getRequester.getRequestImage(...)
    #   postRequester.postRequestJsonMessage(...)
    # curl_request.h
    #   httpRequestUtils::getRequestImage(...)          ==>  url /lastimage/camId ... getCurler
    #   httpRequestUtils::postRequestJsonMessage(...)   ==>  url /result/camId ... postCurler
    #   /result/

    logger.debug("/lastimage camId " + str(camId))
    if camId is None:
        return ("camId not present in url", 400)    
    if camId == "":
        return ("nameId is empty in url", 400)
    
    index = inputBufferClient.getClientIndex(camId)
    if index is None:
        return ("no client with camId: " + camId, 400)

    lastRecordedIndex = inputBufferClient.buff[index].bufferImages.lastRecordedIndex
    logger.debug("/lastimage camId " + str(camId) + " lastRecordedIndex " + str(lastRecordedIndex))

    if lastRecordedIndex is None:
        msg = "lastRecordedIndex None: camId: " + camId
        logger.error(msg)
        return (msg, 400)
    if lastRecordedIndex < 0:
        msg = "lastRecordedIndex negative: camId: " + camId
        logger.error(msg)
        return (msg, 400)


    already_uploaded = inputBufferClient.buff[index].bufferImages.buffer[lastRecordedIndex].uploaded
    filename = inputBufferClient.buff[index].bufferImages.buffer[lastRecordedIndex].filenameWithStamp

    if take_care_of_already_uploaded is True:
        if already_uploaded is True:
            logger.warning("/lastimage camId " + str(camId) + " lastRecordedIndex " + str(lastRecordedIndex) + ", already uploaded")
            return ("already_uploaded", 204)
            
    dict_out = inputBufferClient.buff[index].bufferImages.buffer[lastRecordedIndex].getAsJsonData()

    if take_care_of_already_uploaded is True:
        inputBufferClient.buff[index].bufferImages.buffer[lastRecordedIndex].uploaded = True

    # OK
    # with open( "todel.png", mode="wb" ) as f:
    #     f.write(base64.b64decode(dict_out["contentBytes"].encode()))
        

    # return (jsonify(dict_out), 200)
    return (dict_out, 200)

@app.route("/lastimage/<string:camId>", methods=["GET"])
def lastimage(camId: str, take_care_of_already_uploaded: bool=True):
    return lastsample(camId=camId, inputBufferClient=bufferClients, take_care_of_already_uploaded=take_care_of_already_uploaded)

@app.route("/lastresult/<string:camId>", methods=["GET"])
def lastresult(camId: str, take_care_of_already_uploaded: bool=True):
    return lastsample(camId=camId, inputBufferClient=ecovisionResults, take_care_of_already_uploaded=take_care_of_already_uploaded)

# called by python thread manager for c++ cleint ecovision
@app.route("/active_clients", methods=["GET"])
def active_clients():
    list = []
    for clientEl in bufferClients.buff:
        list.append(clientEl.clientId)
    logger.debug("/active_clients " + str(list))
    return (list, 200)

@app.route("/active_client_cam", methods=["GET"])
def active_client_cam():
    listout = bufferClients.getListClients()
    logger.info("/active_client_cam returns "+str(listout))
    return jsonify(data=listout), 200

if __name__ == '__main__':
    # to allow flask tu run in a thread add use_reloader=False, otherwise filewatcher thread blosk stuff
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    # shit i lost code about thread sessionrunner i think