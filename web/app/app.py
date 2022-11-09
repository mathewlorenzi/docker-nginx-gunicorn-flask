
import os
import sys
import base64
from base64 import b64encode
import logging
from time import sleep


# in docker, local files cannot be found: add current path to python path:
file_path = os.path.dirname(os.path.realpath(__file__))
if file_path not in sys.path:
    sys.path.insert(1, file_path)
# printRootStructure(dirname=sys.path[0], indent=0)

from flask import Flask, render_template, request, jsonify, json#, flash send_from_directory
from buffer_images import STR_UNKNOWN, BufferClients, NOSAVE, SAVE_WITH_TIMESTAMPS, SAVE_WITH_UNIQUE_FILENAME
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

FLIP = 0

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.abspath( os.path.join(APP_ROOT, "..", "..", "database_clients_camera") )
logger.debug("check output folder: "+str(OUTPUT_PATH))
if os.path.exists(OUTPUT_PATH) is False:
    os.mkdir(OUTPUT_PATH)

bufferClients = BufferClients(MODE_SAVE_TO_DISK=MODE_SAVE_TO_DISK, database_main_path_all_clients=OUTPUT_PATH, debugapp=False)
if bufferClients.initSucc is False:
    logger.debug("BufferClients initialisation failed: " + bufferClients.initMsg)
    exit(1)

class LocalConfig:
    def __init__(self):
        self.flip=0

localconfig = LocalConfig()


# populate_fake_images(OUTPUT_PATH=OUTPUT_PATH, sampleImagePath="sample.png")
# exit(1)

# def load_sample(imagePath):
#     with open(imagePath, mode="rb") as fsample:
#         img_data = fsample.read()
#         encoded = b64encode(img_data)
#         decoded_img = encoded.decode('utf-8')
#         uri_result = f"data:image/jpeg;base64,{decoded_img}"
#         #mime = "image/jpeg"
#         #uri_result = "data:%s;base64,%s" % (mime, encoded)
#         return uri_result
# uri_result = load_sample("todel.png")

@app.route("/hello")
def hello():
    logger.debug("/hello endpoint: pid: " + str(os.getpid()))
    #print("[DEBUG]/hello endpoint: pid: ", str(os.getpid()))
    data = {"data": "Hello Camera3"}
    # uri_result = load_sample("sample.png")
    return jsonify(data)

@app.route("/result")
def result():
    print("/result localconfig.flip", localconfig.flip)
    logger.debug("/result endpoint: " + str(localconfig.flip))
    # data = {"data": "Hello Camera3"}
    # return jsonify(data)

    if localconfig.flip == 0:
        imgPath = "sample.png"
        localconfig.flip = 1
    else:
        imgPath = "todel.png"
        localconfig.flip = 0

    print("/result imgPath", imgPath)

    with open(imgPath, mode="rb") as fsample:
        img_data = fsample.read()
        encoded = b64encode(img_data)
        decoded_img = encoded.decode('utf-8')
        #uri_result = f"data:image/jpeg;base64,{decoded_img}"
        #mime = "image/jpeg"
        #uri_result = "data:%s;base64,%s" % (mime, encoded)
        return (decoded_img, 200)

    return ("YYYYYYYYYYYYYYYYYEEEEEEESS", 200)

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

# this is called within the camera.html: var url = 'https://www.ecovision.ovh:81/image';sam
@app.route("/image", methods=['POST'])
def image():

    # bytes to string
    jsonstr = request.data.decode('utf8')
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
            return ("OK", 200)
    return ("OK", 200)

@app.route("/camera", methods=['GET'])
def upload():
    logger.debug("/camera endpoint" + str(request.method))
    return render_template("camera.html", usedUrl = str(request.url_root), nameId = STR_UNKNOWN)#, uri_result=uri_result)

@app.route("/lastimage/<string:camId>", methods=["GET"])
def lastimage(camId: str):
    logger.debug("/lastimage camId " + str(camId))
    if camId is None:
        return ("camId not present in url", 400)    
    if camId == "":
        return ("nameId is empty in url", 400)
    
    index = bufferClients.getClientIndex(camId)
    if index is None:
        return ("no client with camId: " + camId, 400)

    lastRecordedIndex = bufferClients.buff[index].bufferImages.lastRecordedIndex
    logger.debug("/lastimage camId " + str(camId) + " lastRecordedIndex " + str(lastRecordedIndex))

    if lastRecordedIndex is None:
        msg = "lastRecordedIndex None: camId: " + camId
        logger.error(msg)
        return (msg, 400)
    if lastRecordedIndex < 0:
        msg = "lastRecordedIndex negative: camId: " + camId
        logger.error(msg)
        return (msg, 400)


    already_uploaded = bufferClients.buff[index].bufferImages.buffer[lastRecordedIndex].uploaded
    filename = bufferClients.buff[index].bufferImages.buffer[lastRecordedIndex].filenameWithStamp

    if already_uploaded is True:
        logger.warning("/lastimage camId " + str(camId) + " lastRecordedIndex " + str(lastRecordedIndex) + ", already uploaded")
        return ("already_uploaded", 204)

    dict_out = bufferClients.buff[index].bufferImages.buffer[lastRecordedIndex].getAsJsonData()

    bufferClients.buff[index].bufferImages.buffer[lastRecordedIndex].uploaded = True

    # OK
    # with open( "todel.png", mode="wb" ) as f:
    #     f.write(base64.b64decode(dict_out["contentBytes"].encode()))
        

    # return (jsonify(dict_out), 200)
    return (dict_out, 200)


# @app.route("/debug_last_recorded_index/<string:camId>", methods=["GET"])
# def debug_last_recorded_index(camId: str):
#     logger.debug("/debug_last_recorded_index camId " + str(camId))
#     if camId is None:
#         return ("camId not present in url", 400)    
#     if camId == "":
#         return ("nameId is empty in url", 400)
    
#     index = bufferClients.getClientIndex(camId)
#     if index is None:
#         return ("no client with camId: " + camId, 400)

#     lastRecordedIndex = bufferClients.buff[index].bufferImages.lastRecordedIndex
#     logger.debug("/debug_last_recorded_index camId " + str(camId) + " lastRecordedIndex " + str(lastRecordedIndex))
#     return (str(lastRecordedIndex), 200)



# # called by c++ client
# #@app.route("/lastimage_filename/<string:nameId>", methods=["GET"])
# @app.route("/last_image_filename/<string:camId>", methods=["GET"])
# def lastimage_filename(camId: str):
#     logger.debug("/lastimage_filename camId " + str(camId))
#     #print("[DEBUG]/lastimage_filename nameId ", nameId)
#     if camId is None:
#         return ("camId not present in url", 400)    
#     if camId == "":
#         return ("nameId is empty in url", 400)
    
#     index = bufferClients.getClientIndex(camId)
#     if index is None:
#         return ("no client with camId: " + camId, 400)
    
#     lastRecordedIndex = bufferClients.buff[index].bufferImages.lastRecordedIndex
#     logger.debug("/last_image_filename camId " + str(camId) + " lastRecordedIndex " + str(lastRecordedIndex))

#     filenameWithStamp = bufferClients.buff[index].bufferImages.buffer[lastRecordedIndex].filenameWithStamp
#     logger.debug("/last_image_filename camId " + str(camId) + " filenameWithStamp " + str(filenameWithStamp))
#     #pathImage = os.path.join("images", filenameWithStamp) 
    
#     return (filenameWithStamp, 200)

# # called by c++ client
# @app.route("/is_last_image_uploaded/<string:camId>", methods=["GET"])
# def is_last_image_uploaded(camId: str):
#     index = bufferClients.getClientIndex(camId)
#     if index is None:
#         msg = "no client with camId although we found it last image filename: " + camId
#         logger.error(msg)
#         return (msg, 400)
#     lastRecordedIndex = bufferClients.buff[index].bufferImages.lastRecordedIndex
#     logger.debug("/is_last_image_uploaded camId " + str(camId) + " lastRecordedIndex " + str(lastRecordedIndex))

#     uploaded = bufferClients.buff[index].bufferImages.buffer[lastRecordedIndex].uploaded
#     logger.debug("/is_last_image_uploaded camId " + str(camId) + " uploaded " + str(uploaded))
#     return (str(uploaded), 200)

# # called by c++ client
# #@app.route("/lastimage/<string:nameId>", methods=["GET"])
# @app.route("/last_image_content/<string:camId>", methods=["GET"])
# def lastimage_content(camId: str):
#     #print("[DEBUG]/lastimage: nameId: ", nameId)
#     # filename = os.path.join(get_test_dir(get_root_dir()), "data", "small.jpg")
#     # filenameWithStamp = bufferImages.buffer[bufferImages.lastRecordedIndex].filenameWithStamp
#     # pathImage = os.path.join("images", filenameWithStamp)

#     #(filenameWithStamp, succ) = lastimage_filename(camId = camId)
#     #if succ != 200:
#     #    return (filenameWithStamp, 400)

#     index = bufferClients.getClientIndex(camId)
#     if index is None:
#         return ("no client with camId although we found it last image filename: " + camId, 400)

#     lastRecordedIndex = bufferClients.buff[index].bufferImages.lastRecordedIndex
#     logger.debug("/last_image_content camId " + str(camId) + " lastRecordedIndex " + str(lastRecordedIndex))

#     if lastRecordedIndex is None:
#         msg = "lastRecordedIndex None: camId: " + camId
#         logger.error(msg)
#         return (msg, 400)
#     if lastRecordedIndex < 0:
#         msg = "lastRecordedIndex negative: camId: " + camId
#         logger.error(msg)
#         return (msg, 400)

#     filenameWithStamp = bufferClients.buff[index].bufferImages.buffer[lastRecordedIndex].filenameWithStamp
#     logger.debug("/last_image_content camId " + str(camId) + " filenameWithStamp " + str(filenameWithStamp))
    
#     pathImage = os.path.join(bufferClients.buff[index].outputDir, filenameWithStamp)

#     #print("[DEBUG]/lastimage: =======> ", pathImage)
#     if os.path.exists(pathImage) is False:
#         msg = "[ERROR]/getlastimage image does not exists on disk: " + pathImage
#         # dict_out = {
#         #     "information": "KO",
#         #     "details": msg
#         # }
#         logger.error(  msg)
#         return (msg, 400)
#     if os.path.isfile(pathImage) is False:
#         msg = "[ERROR]/getlastimage image exist but is not a valid file: " + pathImage
#         # dict_out = {
#         #     "information": "KO",
#         #     "details": msg
#         # }
#         logger.error(msg)
#         # return (dict_out, 400)
#         return (msg, 400)

#     with open( pathImage, mode="rb" ) as f:
#         imageContent = f.read()
#         bufferClients.buff[index].bufferImages.buffer[lastRecordedIndex].uploaded = True
#         logger.info("uploading image content to client")
#         return (imageContent, 200)
#         # TODO why no more displayed in webrowser

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

# @app.route("/uploaded_image/<string:camId>/<string:filename>", methods=["GET"])
# def uploaded_image(camId: str, filename: str):
#     inputpath = os.path.join(bufferClients.database_main_path_all_clients, camId, filename)
#     # inputpath = os.path.join(OUTPUT_DIR, camId, filename)
#     print(inputpath)
#     if os.path.isfile(inputpath) is False:
#         return ("file is not valid", 400)
#     if os.path.exists(inputpath) is False:
#         return ("file does not exist", 400)
#     with open(inputpath, mode="rb") as f:
#         return (f.read(), 200)
#     return ("KO", 400)
  
# @app.route("/last_image_content/<string:camId>", methods=["GET"])
# def last_image_content(camId: str):
#     # take first encountered filename as last recorded one
#     for filename in os.listdir(os.path.join(OUTPUT_DIR, camId)): 
#         inputpath = os.path.join(OUTPUT_DIR, camId, filename)
#         print(inputpath)
#         with open(inputpath, mode="rb") as f:
#             return (f.read(), 200)
#     return ("KO", 400)
  
# @app.route("/last_image_filename/<string:camId>", methods=["GET"])
# def last_image_filename(camId: str):
#     inputpath = os.path.join(bufferClients.database_main_path_all_clients, camId, filename)
#     # take first encountered filename as last recorded one
#     for filename in os.listdir(os.path.join(OUTPUT_DIR, camId)): 
#         #inputpath = os.path.join(OUTPUT_DIR, camId, filename)
#         print("return:->"+filename+"<-")
#         return (filename, 200)
#     return ("KO", 400)

# TODO thread to remove unactive clients

if __name__ == '__main__':

    # to allow flask tu run in a thread add use_reloader=False, otherwise filewatcher thread blosk stuff
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    # thread id keeps increasing : every time there is a request: is this normal ? threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)).start()
    #threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)).start()

    # filesWatcher = SessionRunner(thread_id=0, mainDir="database_clients_camera", maxNbFiles=10, maxFileAgeMinutes=60, intervalSec=10)
    # logger.debug("start filesWatcher")
    # filesWatcher.start()
    # logger.debug("join")
    # filesWatcher.join()

