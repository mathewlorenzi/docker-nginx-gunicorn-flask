import os

print(" .... docker debug: curr dir: ", os.getcwd())

files = [f for f in os.listdir('.') if os.path.isdir(f)]
for f in files:
    print(" .... docker debug: ", f)
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    print(" .... docker debug: ", f)

# import os.path as P
# for topdir, subdirs, files in os.walk("./"):
#   print("    " * topdir.count(P.sep), P.basename(topdir))
#   for f in sorted(files):
#     print("    " * (topdir.count(P.sep) + 1), f)

import os
def printRootStructure(dirname,indent=0):
    for i in range(indent):
        print("   ", end=",")
    print(os.path.basename(dirname))
    if os.path.basename(dirname) != 'venv' and os.path.basename(dirname) != '.git':
        if os.path.isdir(dirname):
            for files in os.listdir(dirname):
                printRootStructure(os.path.join(dirname,files),indent+1) # changed

printRootStructure(dirname='./',indent=0)

# os.chdir(os.path.dirname(__file__))

#import base64
#import threading
import logging
from flask import Flask, render_template, request, jsonify, json#, flash send_from_directory
#from flask import redirect
from buffer_images import STR_UNKNOWN, BufferClients #AppImage, ClientCamera, 
#from file_watcher import SessionRunner

# https://github.com/fossasia/Flask_Simple_Form/blob/master/nagalakshmiv2004/Form.py

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#logging.basicConfig(level=logging.DEBUG)

# TODO log rotate
#logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logging.basicConfig(level=logging.DEBUG, format=f'%(asctime)s %(levelname)s : %(message)s')
logger = logging.getLogger(__name__)
logger.warning('Start') 

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.abspath( os.path.join(APP_ROOT, "..", "..", "database_clients_camera") )
logger.debug("check output folder: "+str(OUTPUT_PATH))
if os.path.exists(OUTPUT_PATH) is False:
    os.mkdir(OUTPUT_PATH)

#bufferImages = BufferImages(maxLength=10, directory=OUTPUT_PATH)
# if bufferImages.success is False: ...
bufferClients = BufferClients(database_main_path_all_clients=OUTPUT_PATH)

#app.debug = True

# import shutil
# import cv2
# import time
# from datetime import datetime
# def populate_fake_images(OUTPUT_PATH: str, sampleImagePath: str):
#     camIds = ["peter", "paul", "jack", "UNKNOWN"]
#     if os.path.exists(OUTPUT_PATH):
#         shutil.rmtree(OUTPUT_PATH)
#     os.mkdir(OUTPUT_PATH)
#     for dir in camIds:
#         os.mkdir(os.path.join(OUTPUT_PATH, dir))
#     img = cv2.imread(sampleImagePath)
#     for dir in camIds:
#         for nb in range(10):
#             now = datetime.now()
#             date_time = now.strftime("%m-%d-%YT%H:%M:%S.%f")[:-3]
#             print("date_time:", dir, date_time)
#             cv2.imwrite(os.path.join(OUTPUT_PATH, dir, date_time+".jpg"), img)
#             time.sleep(0.5)
#     return camIds
  
# populate_fake_images(OUTPUT_PATH=OUTPUT_PATH, sampleImagePath="sample.png")
# exit(1)

@app.route("/hello")
def hello():
    logger.debug("/hello endpoint: pid: " + str(os.getpid()))
    #print("[DEBUG]/hello endpoint: pid: ", str(os.getpid()))
    data = {"data": "Hello Camera3"}
    return jsonify(data)

@app.route('/', methods=['GET', 'POST'])
def mainroute():
    logger.debug("/ main endpoint: pid: " + str(os.getpid()))
    #print("[DEBUG]/ main endpoint: pid: ", str(os.getpid()))
    if request.method == 'GET':
        return render_template('form.html')
    elif request.method == 'POST':
        logger.debug("redirect to camera with name: " + request.form['username'] + " from " + request.url_root)
        #print("[DEBUG]redirect to camera with name: ", request.form['username'], " from ", request.url_root)
        #return redirect('/camera', name = request.form['username'])
        return render_template('camera.html', usedUrl = str(request.url_root), nameId = request.form['username'])

# this is called within the camera.html: var url = 'https://www.ecovision.ovh:81/image';
@app.route("/image", methods=['POST'])
def image():
    #app.logger("/image")
    #logger.debug("/image")
    # bytes to string
    jsonstr = request.data.decode('utf8')
    # string to json
    data = json.loads(jsonstr)
    # we could go further into beauty: s = json.dumps(data, indent=4, sort_keys=True)

    # TODO check json fields
    
    imagestr = data["image"]
    nameId = data["nameId"]
    usedUrl = data["usedUrl"]
    #logger.debug("/image: name:" + nameId + " usedUrl " + usedUrl)
    #print("[DEBUG]/image: name:", nameId, " usedUrl ", usedUrl)
    logger.debug("/image: nameId: " + nameId + " usedUrl: " + usedUrl)
    if isinstance(imagestr, str) is False or isinstance(nameId, str) is False:
        #print("error decoding string")
        logger.error("/image: nameId is not a string:" + str(nameId))
        return ("KO: nameId is not a string", 400)
    else:

        # look if existing active camera
        indexClient = bufferClients.getClientIndex(nameId=nameId)
        if indexClient is None:
            logger.info("/image: nameId:" + nameId + " new client")
            #print("[INFO]/image: name:", nameId, " new client")
            indexClient = bufferClients.insertNewClient(nameId=nameId)
        indexClient = bufferClients.getClientIndex(nameId=nameId)
        if indexClient is None:
            logger.error("/image: nameId:" + nameId + " failed finding client")
            #print("[ERROR]/image: name:", nameId, " failed finding client")
            return ("KO: Failed finding client or inserting new client " + nameId, 400)
        
        logger.info("/image: nameId:" + nameId + " indexClient: " + str(indexClient))

        (msg, succ) = bufferClients.buff[indexClient].saveNewImage(logger=logger, imageContent=imagestr)
        if succ is False:
            logger.error(msg)
            #print("[ERROR]", msg)
            # return (msg, 400)
            return ("KO: failed saving new image", 400)
        else:
            logger.debug(msg)
            #print("[INFO]", msg)
            # return (msg, 200)
            return ("OK", 200)

        # appImage = AppImage()
        # if appImage.success is Flse ...
        # filename = appImage.filenameWithStamp
        # print("/image save ", filename)
        # with open(os.path.join(bufferImages.directory, filename), 'wb') as f:
        #     #f.write(base64.decodestring(imagestr.split(',')[1].encode()))
        #     f.write(base64.b64decode(imagestr.split(',')[1].encode()))
        #     appImage.hasData = True
        #     bufferImages.insert(appImage)
        #     print("/image image ready at ", 
        #         bufferImages.lastRecordedIndex, 
        #         bufferImages.buffer[bufferImages.lastRecordedIndex].filenameWithStamp, 
        #         #" replaced image to be del: ", bufferImages.replacedImageFilename
        #         " oldest image to be del: ", bufferImages.oldestRecordedImage, 
        #         bufferImages.buffer[bufferImages.oldestRecordedImage].filenameWithStamp, 
        #         )
        #     #bufferImages.Print()
        #     (msg, succ) = bufferImages.deleteOldest()
        #     print(succ, msg)
        #     if succ is True:
        #         logger.info(msg)
        #         #bufferImages.Print()
        #     else:
        #         logger.error(msg)
        #         #app.logger.error(msg)

    # unused but lets return something
    # data = {"data": "Received image"}
    #return jsonify({"info":"ok"}, 200)
    return ("OK", 200)

@app.route("/camera", methods=['GET'])
def upload():
    logger.debug("/camera endpoint" + str(request.method))
    #print("[DEBUG]/camera endpoint", request.method)
    #here pass a parameter url for the post image inside render template
    #app.logger.debug("/camera endpoint: pid: " + str(os.getpid()))
    return render_template("camera.html", usedUrl = str(request.url_root), nameId = STR_UNKNOWN)

# called by c++ client
#@app.route("/lastimage_filename/<string:nameId>", methods=["GET"])
@app.route("/last_image_filename/<string:camId>", methods=["GET"])
def lastimage_filename(camId: str):
    logger.debug("/lastimage_filename camId " + str(camId))
    #print("[DEBUG]/lastimage_filename nameId ", nameId)
    if camId is None:
        return ("camId not present in url", 400)    
    if camId == "":
        return ("nameId is empty in url", 400)
    
    index = bufferClients.getClientIndex(camId)
    if index is None:
        return ("no client with camId: " + camId, 400)
    
    lastRecordedIndex = bufferClients.buff[index].bufferImages.lastRecordedIndex

    filenameWithStamp = bufferClients.buff[index].bufferImages.buffer[lastRecordedIndex].filenameWithStamp
    
    #pathImage = os.path.join("images", filenameWithStamp) 
    
    return (filenameWithStamp, 200)

# called by c++ client
@app.route("/is_last_image_uploaded/<string:camId>", methods=["GET"])
def is_last_image_uploaded(camId: str):
    index = bufferClients.getClientIndex(camId)
    if index is None:
        msg = "no client with camId although we found it last image filename: " + camId
        logger.error(msg)
        return (msg, 400)
    lastRecordedIndex = bufferClients.buff[index].bufferImages.lastRecordedIndex
    uploaded = bufferClients.buff[index].bufferImages.buffer[lastRecordedIndex].uploaded
    return (str(uploaded), 200)

# called by c++ client
#@app.route("/lastimage/<string:nameId>", methods=["GET"])
@app.route("/last_image_content/<string:camId>", methods=["GET"])
def lastimage_content(camId: str):
    #print("[DEBUG]/lastimage: nameId: ", nameId)
    # filename = os.path.join(get_test_dir(get_root_dir()), "data", "small.jpg")
    # filenameWithStamp = bufferImages.buffer[bufferImages.lastRecordedIndex].filenameWithStamp
    # pathImage = os.path.join("images", filenameWithStamp)

    #(filenameWithStamp, succ) = lastimage_filename(camId = camId)
    #if succ != 200:
    #    return (filenameWithStamp, 400)

    index = bufferClients.getClientIndex(camId)
    if index is None:
        return ("no client with camId although we found it last image filename: " + camId, 400)

    lastRecordedIndex = bufferClients.buff[index].bufferImages.lastRecordedIndex
    if lastRecordedIndex is None:
        msg = "lastRecordedIndex None: camId: " + camId
        logger.error(msg)
        return (msg, 400)
    if lastRecordedIndex < 0:
        msg = "lastRecordedIndex negative: camId: " + camId
        logger.error(msg)
        return (msg, 400)

    filenameWithStamp = bufferClients.buff[index].bufferImages.buffer[lastRecordedIndex].filenameWithStamp
    
    pathImage = os.path.join(bufferClients.buff[index].outputDir, filenameWithStamp)

    #print("[DEBUG]/lastimage: =======> ", pathImage)
    if os.path.exists(pathImage) is False:
        msg = "[ERROR]/getlastimage image does not exists on disk: " + pathImage
        # dict_out = {
        #     "information": "KO",
        #     "details": msg
        # }
        logger.error(  msg)
        return (msg, 400)
    if os.path.isfile(pathImage) is False:
        msg = "[ERROR]/getlastimage image exist but is not a valid file: " + pathImage
        # dict_out = {
        #     "information": "KO",
        #     "details": msg
        # }
        logger.error(msg)
        # return (dict_out, 400)
        return (msg, 400)

    with open( pathImage, mode="rb" ) as f:
        imageContent = f.read()
        bufferClients.buff[index].bufferImages.buffer[lastRecordedIndex].uploaded = True
        logger.info("uploading image content to client")
        return (imageContent, 200)
        # TODO why no more displayed in webrowser

# called by python thread manager for c++ cleint ecovision
@app.route("/active_clients", methods=["GET"])
def active_clients():
    list = []
    for clientEl in bufferClients.buff:
        list.append(clientEl.clientId)
    return (list, 200)
        
# not stateless
# @app.route("/active_client_cam_all_images", methods=["GET"])
# def active_client_cam_all_images():
# #@app.route("/active_client_cam/<int:maxagesec>", methods=["GET"])
# #def active_client_cam(maxagesec: int):
#     #print("maxagesec: ", maxagesec)
#     listout = []
#     for dir in camIds:
#         for file in os.listdir(os.path.join(OUTPUT_DIR, dir)):
#             listout.append((dir, file))
#             #print(dir, file)
#     #return (listout, 200)
#     return jsonify(data=listout), 200


@app.route("/active_client_cam", methods=["GET"])
def active_client_cam():
#@app.route("/active_client_cam/<int:maxagesec>", methods=["GET"])
#def active_client_cam(maxagesec: int):
    #print("maxagesec: ", maxagesec)
    listout = bufferClients.getListClients()
    logger.info("/active_client_cam returns "+str(listout))
    return jsonify(data=listout), 200
    # listout = []
    # for dir in camIds:
    #     listout.append(dir)
    # return jsonify(data=listout), 200

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

