import sys
import os
import logging
import psutil
import threading
import argparse
import time
import socket
import base64
from datetime import datetime
from PIL import Image

# # in docker, local files cannot be found: add current path to python path:
file_path = os.path.dirname(os.path.realpath(__file__))
if file_path not in sys.path:
    sys.path.insert(1, file_path)
# # printRootStructure(dirname=sys.path[0], indent=0)

from flask import Flask, jsonify, request#, json#, render_template, request, jsonify, json#, flash send_from_directory
from flask import make_response
from buffer_images import STR_UNKNOWN, load_sample, BufferClients, NOSAVE, SAVE_WITH_TIMESTAMPS, SAVE_WITH_UNIQUE_FILENAME
from utils import isascii, isBase64, IMGEXT, get_encoded_img, split_images #convertDatetimeToString, convertStringTimestampToDatetimeAndMicrosecValue
from utils_api import record_image_or_result, lastsample, lastfilename, getOutputDir
from manager import ManagerEcovisionS
import json

DEBUG = False
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
log.disabled = True
logging.getLogger("urllib3").setLevel(logging.ERROR)

HOST='0.0.0.0'
PORT=5555
WITH_MANAGER=True
MODE_SAVE_TO_DISK = SAVE_WITH_TIMESTAMPS # for mmap version and no more tcp   NOSAVE
if WITH_MANAGER is False:
    print(" .............. WARNING, debug withiut manager activated: save to dosk images") 
    time.sleep(1)


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


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.abspath( os.path.join(APP_ROOT, "..", "database_clients_camera") )
print("[DEBUG]check output folder: "+str(OUTPUT_PATH))
if os.path.exists(OUTPUT_PATH) is False:
    os.mkdir(OUTPUT_PATH)

bufferClients = BufferClients(type="camimage", MODE_SAVE_TO_DISK=MODE_SAVE_TO_DISK, database_main_path_all_clients=OUTPUT_PATH, debugapp=False)
if bufferClients.initSucc is False:
    print("[DEBUG]BufferClients initialisation failed: " + bufferClients.initMsg)
    exit(1)

ecovisionResults = BufferClients(type="resultmag", MODE_SAVE_TO_DISK=MODE_SAVE_TO_DISK, database_main_path_all_clients=OUTPUT_PATH, debugapp=False)
if ecovisionResults.initSucc is False:
    print("[DEBUG]ecovisionResults initialisation failed: " + ecovisionResults.initMsg)
    exit(1)

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

            # print(' ... ... delete ? one image ?')
            deletedOneClient = True
            while deletedOneClient is True:
                deletedOneClient = bufferClients.deleteOneTooOldConnectedClient(maxDeltaAge=self.maxDeltaAge, debug=self.debug)

            # print(' ... ... delete ? one result ?')
            deletedOneClient = True
            while deletedOneClient is True:
                deletedOneClient = ecovisionResults.deleteOneTooOldConnectedClient(maxDeltaAge=self.maxDeltaAge, debug=self.debug)

            # print(' ... ... mmaps_getResults')
            # ecovisionResults.mmaps_getResults(maxAgeInSec=30, debug=self.debug)

            self._stop_event.wait(self.intervalSec) # check every N sec                
        print('end client watcher')




@app.route('/result/<string:camId>', methods=['GET'])
def result_api(camId: str):
    print(" ... ... camId", camId)

    

    # here lastresult(camId: str, take_care_of_already_uploaded: bool=True):
    
    with open("red.jpg", "rb") as f:
        # with open("house-thumbs-up.gif", "rb") as f:
        image_binary = f.read()

        # response = make_response(base64.b64encode(image_binary))
        # # response.headers.set('Content-Type', 'image/gif')
        # response.headers.set('Content-Type', 'image/jpg')
        # # response.headers.set('Content-Disposition', 'attachment', filename='image.gif')
        # response.headers.set('Content-Disposition', 'attachment', filename='red.jpg')
        # # return response

        return base64.b64encode(image_binary), 200



@app.route("/backend")
def backend():
    print("[DEBUG]/backend endpoint: pid: " + str(os.getpid()))
    data = {"data": "Hello backend"}
    return jsonify(data)

def get_image_to_return(status2: int, content: dict, logger):
    colourImg = None
    msg = None
    _succ = False
    if status2 == 200:
        # TODO how to write timestamp in data or display it somewhere in html
        if content["hasData"] == "False":
            msg = "[ERROR]lastsample returned ok but dict hasData is False"
            # logger.error(msg)
            print("[ERROR]", msg)
            colourImg = 'red'
        elif content["uploaded"] == "True":
            msg = "[ERROR]lastsample returned 200 with alreaddy uploaded: should be a 202 code: "
            # logger.error(msg)
            print("[ERROR]", msg)
            colourImg = 'red'
        else:
            _succ = True
    else:
        msg = "/image: " + content
        if status2 == 404 or status2 == 405:
            colourImg = "red"
            # logger.error(msg + " => reply with " + colourImg)
            print("[ERROR]", msg, " => reply with " + colourImg)
        elif status2 == 400:
            colourImg = "orange"
            # logger.warn(msg + " => reply with " + colourImg)
            print("[ERROR]", msg, " => reply with " + colourImg)
        elif status2 == 204:
            colourImg = "green"
            # logger.warn(msg + " => reply with " + colourImg)
            print("[ERROR]", msg, " => reply with " + colourImg)
        else:
            colourImg = "red"
            #logger.error(msg + " => reply with " + colourImg)
            print("[ERROR]", msg, " => reply with " + colourImg)
    return (_succ, colourImg)


@app.route("/record_image", methods=['POST'])
def record_image():

    print()
    print(" === record image ===")

    jsonstr = request.data.decode('utf8')
    data = json.loads(jsonstr)
    timestamp = data["timestamp"]
    # print(" ... /record_image: sent from camera.html at ", timestamp)
    imagestr = data["image"]  # if of type str, and not base64 encoded .... strange as in camer html we send 64 image/jpg
    # print(" ... ... RECEIVED FROM CAMERA HTML image type:", type(imagestr))
    # print("[DEBUG] ++++++++++++++++ camera returned ", type(imagestr), " isbase64encoded", isBase64(imagestr), "ascii ? ", isascii(imagestr))
    nameId = data["nameId"]
    # usedUrl = data["usedUrl"]

    # print(" ... /record_image: record_image_or_result: image ")
    (msg, camId, status) = record_image_or_result(inputBufferClient=bufferClients, camId=nameId, 
        imageContentStr=imagestr, 
        imageContentBytes=None, logger=logger, debug=DEBUG)

    

    # print(" ++++++ SLEEP ++++++ ", msg, camId, status)
    # time.sleep(10)

    if status != 200:
        print("[ERROR]FAILED fecord image")
        return (get_encoded_img(image_path=os.path.join(file_path, 'red.'+IMGEXT)), status)


    lastFilename = lastfilename(camId=camId, inputBufferClient=bufferClients)
    if lastFilename is None:
        return (get_encoded_img(image_path=os.path.join(file_path, 'red.'+IMGEXT)), 500)

    _outDir = getOutputDir(camId=camId, inputBufferClient=bufferClients)
    print(" ... ... this will be the input for ecovision", _outDir, lastFilename)
    

    GIVE_IT_TO_ME = False
    (content, status2) = lastsample(camId = camId, inputBufferClient=bufferClients, logger=logger, take_care_of_already_uploaded=GIVE_IT_TO_ME)
    # print(" ... /record_image: get lastsample returned status ", status2)
    if status2 != 200:
        print(" ... ... 1")
        print("[ERROR]get lastsample image recorded failed although we just recorded one")
        return (get_encoded_img(image_path=os.path.join(file_path, 'red.'+IMGEXT)), 200)
    (_succ, colourImg) = get_image_to_return(status2=status2, content=content, logger=logger)
    # no matter whether the result is available or not, the result to the post request if here 200
    if _succ is False:
        print(" ... ... 2")
        print("[ERROR]lastsample image failed")
        return (get_encoded_img(image_path=os.path.join(file_path, colourImg+'.'+IMGEXT)), 200)

    maxAgeInSec = 30

    nbTry = 0
    maxNbTry = 10
    resultPathImage = None
    while(resultPathImage is None and nbTry<maxNbTry):
        nbTry += 1
        clientIdList = bufferClients.getListClients()
        for client in bufferClients.buff:
            if client.clientId in clientIdList and client.clientId == camId:
                print(" ... ...  check if result arrived")
                print(" ... ... mmaps_getResults client Id", client.clientId)
                for filename in os.listdir(client.outputDir):
                    print(" ... ... check ", filename)
                    if filename.startswith("track2d-") and filename.endswith(".jpg"):
                        stamp = filename.replace("track2d-", "")
                        # stamp = stamp.replace(".jpg", "")
                        print(" ... ... ", filename, stamp)
                        # diff in seconds
                        pathImage = os.path.join(client.outputDir, filename)
                        if( datetime.now().timestamp() - os.path.getmtime(pathImage) > maxAgeInSec ):
                            print(" ... ... delete ", pathImage)
                            os.remove(pathImage)
                        else:
                            # check if already in buffer images
                            for bufMag in client.bufferImages.buffer:
                                print(" ... ... ", stamp, " VS ", bufMag.filenameWithStamp)
                                if stamp == bufMag.filenameWithStamp:
                                    resultPathImage = pathImage
        
        if resultPathImage is None:
            time.sleep(1)

    if resultPathImage is not None:
        (msgBack, camId, statusBack) = record_image_or_result(inputBufferClient=ecovisionResults, camId=nameId, 
            imageContentStr=None,
            imageContentBytes=HERE and where are the results with teimstamp saved 
            check not overwritten with images  in /paul
            
            received, logger=logger, debug=DEBUG)
        if statusBack != 200:
            print("[ERROR]FAILED record result:", msgBack)
            return (get_encoded_img(image_path=os.path.join(file_path, 'red.'+IMGEXT)), status)



    return (content["contentBytes"], 200)

    '''

    # ******************** does android at least get the red image
    #return (get_encoded_img(image_path=os.path.join(file_path, 'red.'+IMGEXT)), status)
    

    # image recorded successfully
    # now return as a reply the last result, if not already uploaded and if available (sent by ecovision)
    # if not available at all (no result client = ecovision never sent anything) then return a orange empty image
    # if result/client present (ecovision already sent something) but last image already uploaded => send a green empty image

    #DEBUGING = False # True: simply return the last image else return the last result (posted by ecovision)

    # instead of returning result, return the last image just to heck everything ok in image order buffer
    # if DEBUGING is True:
    #     GIVE_IT_TO_ME = False
    #     (content, status2) = lastsample(camId = camId, inputBufferClient=bufferClients, logger=logger, take_care_of_already_uploaded=GIVE_IT_TO_ME)
    #     if status2 == 200:
    #         return (content["contentBytes"], 200)
    #     else:
    #         return (get_encoded_img(image_path=os.path.join(file_path, 'red.'+IMGEXT)), 200)
    # else:
    # 405 error (that shoukd be handled by flask)
    # 404 programming error
    # 400 client/camId not present in list of current clients
    # 202 ok but already uploaded last image
    # 200 ok, last image returned

    (ecovisionPort, succPort) = bufferClients.getEcovisionPort(camId=camId)
    # print(" ......... camId", camId, "ecovisionPort:", ecovisionPort, "............")
    if succPort is False:
        print("[WARNING]no ecovision port for camid ", camId)
        return (get_encoded_img(image_path=os.path.join(file_path, 'red.'+IMGEXT)), 200) 

    # try replace tcp by method i used for tesseract docker run directly from command  and feed it image buffer ?   

    
    # ==========================
    # send a message to tcp server in eocivion code to get trakicing result
    # ==========================
    # Initialize a TCP client socket using SOCK_STREAM
    host_ip = HOST
    server_port = ecovisionPort


    if WITH_MANAGER is False:
        server_port = 6789 
        print(" ................ without manager ...............ecovisionPort server_port", server_port)
    

    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False
    receivedResult = False
    try:
        # Establish connection to TCP server and exchange data
        #print(" .... connect ...")
        tcp_client.connect((host_ip, server_port))

        #print(" .... connected")
        connected = True


        GIVE_IT_TO_ME = False
        (content, status2) = lastsample(camId = camId, inputBufferClient=bufferClients, logger=logger, take_care_of_already_uploaded=GIVE_IT_TO_ME)
        # print(" ... /record_image: get lastsample returned status ", status2)
        if status2 != 200:
            print("[ERROR]get lastsample image recorded failed although we just recorded one")
            return (get_encoded_img(image_path=os.path.join(file_path, 'red.'+IMGEXT)), 200)
        (_succ, colourImg) = get_image_to_return(status2=status2, content=content, logger=logger)
        # no matter whether the result is available or not, the result to the post request if here 200
        if _succ is False:
            print("[ERROR]lastsample image failed")
            return (get_encoded_img(image_path=os.path.join(file_path, colourImg+'.'+IMGEXT)), 200) 


        # TODO hasData, uploaded ? ......... ?
    
        data = base64.b64decode(content['contentBytes'].encode())
                
        # print(" ... ... ", type(data))
        dataSplit = split_images(data)
        index = 0
        for chunk in dataSplit:
            nb = tcp_client.send(chunk)
            # print(index, "type", type(chunk), "len", len(chunk), "sent", nb)
            index+=1
        received = b""
        while True:
            # print(index, "receving...")
            curr = tcp_client.recv(2048)
            # print(len(curr))
            received += curr
            if len(curr) < 2048:
                receivedResult = True
                break

        # [DEBUG] ++++++++++++++++ ecovisoin returned  <class 'bytes'>  isbase64encoded False encoding utf-8
        # received is of type bytes, utf-8 encoded, and not base64 encoded
        # print("[DEBUG] ++++++++++++++++ ecovisoin returned ", type(received), " isbase64encoded", isBase64(received), "encoding", json.detect_encoding(received))
        received = base64.b64encode(received)
    finally:
        tcp_client.close()
        # print("[ERROR]tcp connection failed, return red image")
        # return (get_encoded_img(image_path=os.path.join(file_path, 'red.'+IMGEXT)), 200)
        time.sleep(1)

    print("[INFO]connected and reciedv resuklt", connected, receivedResult)
    if connected is True and receivedResult is True:
        print(" === === record result ===. ===")
        (msgBack, camId, statusBack) = record_image_or_result(inputBufferClient=ecovisionResults, camId=nameId, 
            imageContentStr=None,
            imageContentBytes=received, logger=logger, debug=DEBUG)
        if statusBack != 200:
            print("[ERROR]FAILED record result:", msgBack)
            return (get_encoded_img(image_path=os.path.join(file_path, 'red.'+IMGEXT)), status)

        (contentBack, statusBack) = lastsample(camId = camId, inputBufferClient=ecovisionResults, logger=logger, take_care_of_already_uploaded=GIVE_IT_TO_ME)
        # print(" ... /record_image: get lastsample of result returned status ", statusBack)
        if statusBack != 200:
            print("[ERROR]get lastsample result recorded failed although we just recorded one")
            return (get_encoded_img(image_path=os.path.join(file_path, 'red.'+IMGEXT)), 200)
        
        (_succBack, colourImg) = get_image_to_return(status2=statusBack, content=contentBack, logger=logger)
        if _succBack is True:
            print("[INFO]reply with result content saved at ", content["dateTime"])
            
            # ok with firefox but not with android
            # return (contentBack["contentBytes"], 200) # jpeg now
            
            data = contentBack["contentBytes"]
            # print("[DEBUG] ++++++++++++++++ ", type(data), " isbase64encoded", isBase64(data), "ascii ? ", isascii(data))
            # [DEBUG] ++++++++++++++++  <class 'str'>  isbase64encoded True ascii ?  True
            
            # print("[DEBUG] ++++++++++++++++ ", type(data), " isbase64encoded", isBase64(data), "ascii ? ", isascii(data))
            
            data = data.encode("ascii")
            #print("[DEBUG] ++++++++++++++++ ", type(data), " isbase64encoded", isBase64(data), "encoding", json.detect_encoding(data))
            #[DEBUG] ++++++++++++++++  <class 'bytes'>  isbase64encoded True encoding utf-8

            # === OK but still not ok on android
            # return (data, 200) # jpeg now

            # for android
            data = base64.decodebytes(data)
            with open("temp.jpg", mode="wb") as ftemp:
                ftemp.write(data)
            img1 = Image.open("temp.jpg")
            img1.save("temp.png")
            with open("temp.png", mode="rb") as ftemp:
                data = ftemp.read()
                data = base64.b64encode(data)
                return (data, 200)
        else:
            return (get_encoded_img(image_path=os.path.join(file_path, colourImg+'.'+IMGEXT)), 200) 
    else:
        return (get_encoded_img(image_path=os.path.join(file_path, 'red.'+IMGEXT)), 200) 
    '''
    

@app.route("/lastimage/<string:camId>", methods=["GET"])
def lastimage(camId: str, take_care_of_already_uploaded: bool=True):
    print("[INFO]/lastimage GET")
    return lastsample(camId=camId, inputBufferClient=bufferClients, take_care_of_already_uploaded=take_care_of_already_uploaded)

@app.route("/lastresult/<string:camId>", methods=["GET"])
def lastresult(camId: str, take_care_of_already_uploaded: bool=True):
    print("[INFO]/lastresult GET")
    return lastsample(camId=camId, inputBufferClient=ecovisionResults, take_care_of_already_uploaded=take_care_of_already_uploaded)

# called by python thread manager for c++ cleint ecovision
# @app.route("/active_clients", methods=["GET"])
# def active_clients():
#     list = []
#     for clientEl in bufferClients.buff:
#         list.append(clientEl.clientId)
#     print("[DEBUG]/active_clients " + str(list))
#     return (list, 200)

@app.route("/active_client_cam", methods=["GET"])
def active_client_cam():
    listout = bufferClients.getListClients()
    # print("[INFO]/active_client_cam returns "+str(listout))
    return jsonify(data=listout), 200
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ecovision threads manager')
    parser.add_argument('--ecovisionPath', metavar='ecovisionPath', required=True,
                        help='the ecovisionPath') # "/home/ecorvee/Projects/EcoVision/ecplatform2"
    parser.add_argument('--sharedVolume', metavar='sharedVolume', required=True,
                        help='sharedVolume bet ecovision and backend') # "/home/ecorvee/Projects/WEBAPP/docker-nginx-gunicorn-flask/database_clients_camera"
    parser.add_argument('--debug', action='store_true', default=False)
    args = parser.parse_args()
    if WITH_MANAGER is True:
        manager = ManagerEcovisionS(host=HOST, port=PORT, 
            ecovisionPath=args.ecovisionPath, 
            sharedVolume=args.sharedVolume,
            debug=args.debug)
        manager.start()

    watchActiveClients = WatchActiveClients()
    watchActiveClients.start()

    # to allow flask tu run in a thread add use_reloader=False, otherwise filewatcher thread blosk stuff
    app.run(debug=False, host=HOST, port=PORT, use_reloader=False)
