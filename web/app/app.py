import os
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
bufferClients = BufferClients(database_main_path_all_clients=OUTPUT_PATH)

#app.debug = True

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

    imagestr = data["image"]
    nameId = data["nameId"]
    usedUrl = data["usedUrl"]
    #logger.debug("/image: name:" + nameId + " usedUrl " + usedUrl)
    #print("[DEBUG]/image: name:", nameId, " usedUrl ", usedUrl)
    logger.debug("/image: nameId:" + nameId)
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
@app.route("/lastimage_filename/<string:nameId>", methods=["GET"])
def lastimage_filename(nameId: str):
    logger.debug("/lastimage_filename nameId " + str(nameId))
    #print("[DEBUG]/lastimage_filename nameId ", nameId)
    if nameId is None:
        return ("nameId not present in url", 400)    
    if nameId == "":
        return ("nameId is empty in url", 400)
    
    index = bufferClients.getClientIndex(nameId)
    if index is None:
        return ("no client with nameId: " + nameId, 400)
    
    lastRecordedIndex = bufferClients.buff[index].bufferImages.lastRecordedIndex

    filenameWithStamp = bufferClients.buff[index].bufferImages.buffer[lastRecordedIndex].filenameWithStamp
    
    #pathImage = os.path.join("images", filenameWithStamp) 
    
    return (filenameWithStamp, 200)

# called by c++ client
@app.route("/lastimage/<string:nameId>", methods=["GET"])
def getlastimage(nameId: str):
    #print("[DEBUG]/lastimage: nameId: ", nameId)
    # filename = os.path.join(get_test_dir(get_root_dir()), "data", "small.jpg")
    # filenameWithStamp = bufferImages.buffer[bufferImages.lastRecordedIndex].filenameWithStamp
    # pathImage = os.path.join("images", filenameWithStamp)

    (filenameWithStamp, succ) = lastimage_filename(nameId = nameId)
    if succ != 200:
        return (filenameWithStamp, 400)

    index = bufferClients.getClientIndex(nameId)
    if index is None:
        return ("no client with nameId although we found it last image filename: " + nameId, 400)

    pathImage = os.path.join(bufferClients.buff[index].outputDir, filenameWithStamp)

    #print("[DEBUG]/lastimage: =======> ", pathImage)
    if os.path.exists(pathImage) is False:
        msg = "[ERROR]/getlastimage image does not exists on disk: " + pathImage
        dict_out = {
            "information": "KO",
            "details": msg
        }
        logger.error(  msg)
        return dict_out
    if os.path.isfile(pathImage) is False:
        msg = "[ERROR]/getlastimage image exist but is not a valid file: " + pathImage
        dict_out = {
            "information": "KO",
            "details": msg
        }
        logger.error(msg)
        return dict_out

    with open( pathImage, mode="rb" ) as f:
       imageContent = f.read()
       return imageContent
       # TODO why no more displayed in webrowser

# called by python thread manager for c++ cleint ecovision
@app.route("/active_clients", methods=["GET"])
def active_clients():
    list = []
    for clientEl in bufferClients.buff:
        list.append(clientEl.clientId)
    return (list, 200)
        

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

