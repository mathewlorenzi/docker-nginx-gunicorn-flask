#from buffer_images import STR_UNKNOWN, load_sample, BufferClients, NOSAVE, SAVE_WITH_TIMESTAMPS, SAVE_WITH_UNIQUE_FILENAME
#from utils import convertDatetimeToString, convertStringTimestampToDatetimeAndMicrosecValue

'''MODE_SAVE_TO_DISK = NOSAVE
#MODE_SAVE_TO_DISK = SAVE_WITH_UNIQUE_FILENAME

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.abspath( os.path.join(APP_ROOT, "..", "..", "database_clients_camera") )
print("[DEBUG]check output folder: "+str(OUTPUT_PATH))
if os.path.exists(OUTPUT_PATH) is False:
    os.mkdir(OUTPUT_PATH)

bufferClients = BufferClients(type="camimage", MODE_SAVE_TO_DISK=MODE_SAVE_TO_DISK, database_main_path_all_clients=OUTPUT_PATH, debugapp=False)
if bufferClients.initSucc is False:
    print("[DEBUG]BufferClients initialisation failed: " + bufferClients.initMsg)
    exit(1)

# V1 ecovisionResults => old2.py
# v2 ecovisionResults
ecovisionResults = BufferClients(type="resultmag", MODE_SAVE_TO_DISK=MODE_SAVE_TO_DISK, database_main_path_all_clients=OUTPUT_PATH, debugapp=False)
if ecovisionResults.initSucc is False:
    print("[DEBUG]ecovisionResults initialisation failed: " + ecovisionResults.initMsg)
    exit(1)

# populate_fake_images(OUTPUT_PATH=OUTPUT_PATH, sampleImagePath="sample.png")
# exit(1)
# uri_result = load_sample("todel.png")

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
    print("[DEBUG]/result_image2 endpoint")
    if camId in ecovisionResults.trackResultsImage:
        return (ecovisionResults.trackResultsImage[camId], 200)
    else:
        return ("ko: image result2 not ready yet for " + camId, 204)
'''

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
'''

'''def record_image_or_result(inputBufferClient: BufferClients, info: str):
    # bytes to string
    jsonstr = request.data.decode('utf8')
    # if info=="result":
    #     print(jsonstr)
    # string to json
    data = json.loads(jsonstr)
    # we could go further into beauty: s = json.dumps(data, indent=4, sort_keys=True)

    # TODO check json fields

    now = datetime.now()
    date_time = convertDatetimeToString(now)
    
    timestamp = data["timestamp"]
    print(" ... record_image_or_result: sent at ", timestamp, " vs now ", date_time)
    imagestr = data["image"]
    nameId = data["nameId"]
    usedUrl = data["usedUrl"]
    print("[DEBUG]/image: nameId: " + nameId + " usedUrl: " + usedUrl)
    if isinstance(imagestr, str) is False or isinstance(nameId, str) is False:
        print("[ERROR]/image: nameId is not a string:" + str(nameId))
        return ("KO: nameId is not a string", nameId, 400)
    else:
        # look if existing active camera
        indexClient = inputBufferClient.getClientIndex(nameId=nameId)
        if indexClient is None:
            print("[INFO]/image: nameId:" + nameId + " new client")
            (_msg, indexClient) = inputBufferClient.insertNewClient(nameId=nameId)
            if indexClient is None:
                errMsg = "/image: nameId:" + nameId + " failed inserting new client " + _msg
                logger.error(errMsg)
                return (errMsg, nameId, 400)

        # check really necessary ?
        indexClient = inputBufferClient.getClientIndex(nameId=nameId)
        if indexClient is None:
            print("[ERROR]/image: nameId:" + nameId + " failed finding client")
            return ("KO: Failed finding client or inserting new client " + nameId, nameId, 400)
        
        print("[DEBUG]/image: nameId:" + nameId + " indexClient: " + str(indexClient))


        # while(inputBufferClient.buff[indexClient].lockOnUpload is True){
        #     print("[INFO]/image: lock active, wait a bit, for camId" + nameId)
        #     time.sleep(1)
        # }
        # lockOnUpload = False
        # imageToBeUploaded = AppImage()

        (msg, succ) = inputBufferClient.buff[indexClient].insertNewImage(logger=logger, imageContent=imagestr)
        if succ is False:
            logger.error(msg)
            return ("KO: failed saving new image", nameId, 400)
        else:
            logger.info(msg)

            # camId = nameId
            # print("[DEBUG]/result_image2 endpoint")
            # v1
            # if camId in ecovisionResults.trackResultsImage:
            #     return (ecovisionResults.trackResultsImage[camId], nameId, 200)
            # else:
            #     return ("ok but image result from ecovision not ready yet for " + camId, nameId, 202)
            # v2 return a blank image if not ready
            # indexECO = bufferEcovisionResults.getClientIndex(nameId=nameId)
            # if indexECO is None:
            #     print("[ERROR]/image: nameId:" + nameId + " failed finding client in ecovision results")
            #     return (HERE blank image, nameId, 202)
            # bufferEcovisionResults.buff[indexECO].get last image
        
            # HERE    

            return ("OK", nameId, 200)
    return ("OK", nameId, 200)
'''

'''def lastsample(camId: str, inputBufferClient: BufferClients, take_care_of_already_uploaded: bool=True):
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

    print("[DEBUG]lastsample camId " + str(camId) + "/" + inputBufferClient.TYPE)
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
    print("[INFO]lastsample camId " + str(camId) + " lastRecordedIndex " + str(lastRecordedIndex) + " /" + inputBufferClient.TYPE)

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
'''