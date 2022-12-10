# from datetime import datetime
import os
import sys
# import base64
# from base64 import b64encode
import logging
# from time import sleep
# from charset_normalizer import detect
import psutil
import threading

# from PIL import Image, ImageDraw

# # in docker, local files cannot be found: add current path to python path:
file_path = os.path.dirname(os.path.realpath(__file__))
if file_path not in sys.path:
    sys.path.insert(1, file_path)
# # printRootStructure(dirname=sys.path[0], indent=0)

from flask import Flask, jsonify, request, json#, render_template, request, jsonify, json#, flash send_from_directory
from buffer_images import STR_UNKNOWN, load_sample, BufferClients, NOSAVE, SAVE_WITH_TIMESTAMPS, SAVE_WITH_UNIQUE_FILENAME
from utils import get_encoded_img #convertDatetimeToString, convertStringTimestampToDatetimeAndMicrosecValue
# import requests

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
OUTPUT_PATH = os.path.abspath( os.path.join(APP_ROOT, "..", "database_clients_camera") )
logger.debug("check output folder: "+str(OUTPUT_PATH))
if os.path.exists(OUTPUT_PATH) is False:
    os.mkdir(OUTPUT_PATH)

bufferClients = BufferClients(type="camimage", MODE_SAVE_TO_DISK=MODE_SAVE_TO_DISK, database_main_path_all_clients=OUTPUT_PATH, debugapp=False)
if bufferClients.initSucc is False:
    logger.debug("BufferClients initialisation failed: " + bufferClients.initMsg)
    exit(1)

# V1 ecovisionResults => old2.py
# v2 ecovisionResults
ecovisionResults = BufferClients(type="resultmag", MODE_SAVE_TO_DISK=MODE_SAVE_TO_DISK, database_main_path_all_clients=OUTPUT_PATH, debugapp=False)
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


@app.route("/backend")
def backend():
    logger.debug("/backend endpoint: pid: " + str(os.getpid()))
    data = {"data": "Hello backend"}
    return jsonify(data)

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

def record_image_or_result(inputBufferClient: BufferClients, imageContentStr: str, camId: str):
    # now = datetime.now()
    # date_time = convertDatetimeToString(now)
    
    #timestamp = data["timestamp"]
    # print(" ... record_image_or_result: sent at ", timestamp, " vs now ", date_time)
    #imageContentStr = data["image"]
    nameId = camId # data["nameId"]
    #usedUrl = data["usedUrl"]
    #logger.debug("/image: nameId: " + nameId + " usedUrl: " + usedUrl)
    if isinstance(imageContentStr, str) is False or isinstance(nameId, str) is False:
        logger.error("/image: nameId is not a string:" + str(nameId))
        return ("KO: nameId is not a string", nameId, 400)
    else:
        # look if existing active camera
        indexClient = inputBufferClient.getClientIndex(nameId=nameId)
        if indexClient is None:
            logger.info("/image: nameId:" + nameId + " new client")
            (_msg, indexClient) = inputBufferClient.insertNewClient(nameId=nameId)
            if indexClient is None:
                errMsg = "/image: nameId:" + nameId + " failed inserting new client " + _msg
                logger.error(errMsg)
                return (errMsg, nameId, 400)

        # check really necessary ?
        indexClient = inputBufferClient.getClientIndex(nameId=nameId)
        if indexClient is None:
            logger.error("/image: nameId:" + nameId + " failed finding client")
            return ("KO: Failed finding client or inserting new client " + nameId, nameId, 400)
        
        logger.debug("/image: nameId:" + nameId + " indexClient: " + str(indexClient))


        # while(inputBufferClient.buff[indexClient].lockOnUpload is True){
        #     logger.info("/image: lock active, wait a bit, for camId" + nameId)
        #     time.sleep(1)
        # }
        # lockOnUpload = False
        # imageToBeUploaded = AppImage()

        (msg, succ) = inputBufferClient.buff[indexClient].insertNewImage(logger=logger, imageContent=imageContentStr)
        if succ is False:
            logger.error(msg)
            return ("KO: failed saving new image", nameId, 400)
        else:
            logger.info(msg)

            # camId = nameId
            # logger.debug("/result_image2 endpoint")
            # v1
            # if camId in ecovisionResults.trackResultsImage:
            #     return (ecovisionResults.trackResultsImage[camId], nameId, 200)
            # else:
            #     return ("ok but image result from ecovision not ready yet for " + camId, nameId, 202)
            # v2 return a blank image if not ready
            # indexECO = bufferEcovisionResults.getClientIndex(nameId=nameId)
            # if indexECO is None:
            #     logger.error("/image: nameId:" + nameId + " failed finding client in ecovision results")
            #     return (HERE blank image, nameId, 202)
            # bufferEcovisionResults.buff[indexECO].get last image
        
            # HERE    

            return ("OK", nameId, 200)
    return ("OK", nameId, 200)

@app.route("/record_image", methods=['POST'])
def record_image():
    jsonstr = request.data.decode('utf8')
    data = json.loads(jsonstr)
    timestamp = data["timestamp"]
    print(" ... record_image: sent at ", timestamp)
    imagestr = data["image"]
    nameId = data["nameId"]
    # usedUrl = data["usedUrl"]
    (msg, camId, status) = record_image_or_result(inputBufferClient=bufferClients, imageContentStr=imagestr, camId=nameId)
    if status != 200:
        return (get_encoded_img(image_path=os.path.join(file_path, 'red".png')), status)
    else:
        # image recorded successfully
        # now return as a reply the last result, if not already uploaded and if available (sent by ecovision)
        # if not available at all (no result client = ecovision never sent anything) then return a orange empty image
        # if result/client present (ecovision already sent something) but last image already uploaded => send a green empty image

        DEBUGING = False # True: simply return the last image else return the last result (posted by ecovision)

        # instead of returning result, return the last image just to heck everything ok in image order buffer
        if DEBUGING is True:
            GIVE_IT_TO_ME = False
            (content, status2) = lastsample(camId = camId, inputBufferClient=bufferClients, take_care_of_already_uploaded=GIVE_IT_TO_ME)
            if status2 == 200:
                return (content["contentBytes"], 200)
            else:
                return (get_encoded_img(image_path=os.path.join(file_path, 'red.png')), 200)
        else:
            # 405 error (that shoukd be handled by flask)
            # 404 programming error
            # 400 client/camId not present in list of current clients
            # 202 ok but already uploaded last image
            # 200 ok, last image returned
            GIVE_IT_TO_ME = False
            (content, status2) = lastsample(camId = camId, inputBufferClient=ecovisionResults, take_care_of_already_uploaded=GIVE_IT_TO_ME)
        
            colourImg = None
            msg = None
            _succ = False
            if status2 == 200:
                # TODO how to write timestamp in data or display it somewhere in html
                if content["hasData"] == "False":
                    msg = "[ERROR]lastsample returned ok but dict hasData is False"
                    logger.error(msg)
                    colourImg = 'red'
                elif content["uploaded"] == "True":
                    msg = "[ERROR]lastsample returned 200 with alreaddy uploaded: should be a 202 code: "
                    logger.error(msg)
                    colourImg = 'red'
                else:
                    _succ = True
            else:
                msg = "/image: " + content
                if status2 == 404 or status2 == 405:
                    colourImg = "red"
                    logger.error(msg + " => reply with " + colourImg)
                elif status2 == 400:
                    colourImg = "orange"
                    logger.warn(msg + " => reply with " + colourImg)
                elif status2 == 204:
                    colourImg = "green"
                    logger.warn(msg + " => reply with " + colourImg)
                else:
                    colourImg = "red"
                    logger.error(msg + " => reply with " + colourImg)

        # no matter whether the result is available or not, the result to the post request if here 200
        if _succ is True:
            print(" ... .... reply with content saved at ", content["dateTime"])
            return (content["contentBytes"], 200)
        else:
            return (get_encoded_img(image_path=os.path.join(file_path, colourImg+'.png')), 200) 

@app.route("/record_result", methods=['POST'])
def record_result():
    jsonstr = request.data.decode('utf8')
    data = json.loads(jsonstr)
    timestamp = data["timestamp"]
    print(" ... record_result: sent at ", timestamp)
    imagestr = data["image"]
    nameId = data["nameId"]
    #return ("debug", 200)
    # usedUrl = data["usedUrl"]
    #return record_image_or_result(inputBufferClient=ecovisionResults, imageContentStr=imagestr, camId=nameId)
    (msg, camId, status) = record_image_or_result(inputBufferClient=ecovisionResults, imageContentStr=imagestr, camId=nameId)
    return (msg, status)

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

    # 405 error (that shoukd be handled by flask)
    # 404 programming error
    # 400 client/camId not present in list of current clients
    # 204 ok but already uploaded last image
    # 200 ok, last image returned

    logger.debug("lastsample camId " + str(camId) + "/" + inputBufferClient.TYPE)
    if camId is None:
        msg = "camId in None in url" + " /" + inputBufferClient.TYPE
        logger.error(msg)
        return (msg, 405)    
    if camId == "":
        msg = "nameId is empty in url" + " /" + inputBufferClient.TYPE
        logger.error(msg)
        return (msg, 405)
    
    index = inputBufferClient.getClientIndex(camId)
    if index is None:
        msg = "client/camId not present in list of current clients: " + camId + " /" + inputBufferClient.TYPE
        logger.debug(msg)
        return (msg, 400)

    lastRecordedIndex = inputBufferClient.buff[index].bufferImages.lastRecordedIndex
    logger.info("lastsample camId " + str(camId) + " lastRecordedIndex " + str(lastRecordedIndex) + " /" + inputBufferClient.TYPE)

    if lastRecordedIndex is None:
        msg = "lastRecordedIndex None: camId: " + camId + " /" + inputBufferClient.TYPE
        logger.error(msg)
        return (msg, 404)
    if lastRecordedIndex < 0:
        msg = "lastRecordedIndex negative: camId: " + camId + " /" + inputBufferClient.TYPE
        logger.error(msg)
        return (msg, 404)


    already_uploaded = inputBufferClient.buff[index].bufferImages.buffer[lastRecordedIndex].uploaded
    filename = inputBufferClient.buff[index].bufferImages.buffer[lastRecordedIndex].filenameWithStamp

    if take_care_of_already_uploaded is True:
        if already_uploaded is True:
            logger.warning("lastsample camId " + str(camId) + " lastRecordedIndex " + str(lastRecordedIndex) + ", already uploaded" + " /" + inputBufferClient.TYPE)
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
    logger.info("/lastimage GET")
    return lastsample(camId=camId, inputBufferClient=bufferClients, take_care_of_already_uploaded=take_care_of_already_uploaded)

@app.route("/lastresult/<string:camId>", methods=["GET"])
def lastresult(camId: str, take_care_of_already_uploaded: bool=True):
    logger.info("/lastresult GET")
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
    app.run(debug=True, host='0.0.0.0', port=5555, use_reloader=False)
    # shit i lost code about thread sessionrunner i think