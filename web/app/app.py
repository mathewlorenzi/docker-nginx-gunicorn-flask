import os
#import base64
import logging
from flask import Flask, render_template, request, send_from_directory, jsonify, json, flash
from flask import redirect
from buffer_images import STR_UNKNOWN, AppImage, ClientCamera, BufferClients

# https://github.com/fossasia/Flask_Simple_Form/blob/master/nagalakshmiv2004/Form.py

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#logging.basicConfig(level=logging.DEBUG)

# TODO log rotate
logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logging.warning('Start') 

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(APP_ROOT, "..", "..", "database_clients_camera")
logging.debug("check output folder: "+str(OUTPUT_PATH))
if os.path.exists(OUTPUT_PATH) is False:
    os.mkdir(OUTPUT_PATH)

#bufferImages = BufferImages(maxLength=10, directory=OUTPUT_PATH)
bufferClients = BufferClients(database_main_path_all_clients=OUTPUT_PATH)

#app.debug = True

@app.route("/hello")
def hello():
    logging.debug("/hello endpoint: pid: " + str(os.getpid()))
    print("[DEBUG]/hello endpoint: pid: ", str(os.getpid()))
    data = {"data": "Hello Camera3"}
    return jsonify(data)

@app.route('/', methods=['GET', 'POST'])
def mainroute():
    logging.debug("/ main endpoint: pid: " + str(os.getpid()))
    print("[DEBUG]/ main endpoint: pid: ", str(os.getpid()))
    if request.method == 'GET':
        return render_template('form.html')
    elif request.method == 'POST':
        logging.debug("redirect to camera with name: " + request.form['username'] + " from " + request.url_root)
        print("[DEBUG]redirect to camera with name: ", request.form['username'], " from ", request.url_root)
        #return redirect('/camera', name = request.form['username'])
        return render_template('camera.html', usedUrl = str(request.url_root), nameId = request.form['username'])

# this is called within the camera.html: var url = 'https://www.ecovision.ovh:81/image';
@app.route("/image", methods=['POST'])
def image():
    #app.logger("/image")
    logging.debug("/image")
    # bytes to string
    jsonstr = request.data.decode('utf8')
    # string to json
    data = json.loads(jsonstr)
    # we could go further into beauty: s = json.dumps(data, indent=4, sort_keys=True)

    imagestr = data["image"]
    nameId = data["nameId"]
    usedUrl = data["usedUrl"]
    logging.debug("/image: name:" + nameId + " usedUrl " + usedUrl)
    print("[DEBUG]/image: name:", nameId, " usedUrl ", usedUrl)
    if isinstance(imagestr, str) is False or isinstance(nameId, str) is False:
        print("error decoding string")
    else:

        # look if existing active camera
        indexClient = bufferClients.getClientIndex(nameId=nameId)
        if indexClient is None:
            logging.info("/image: name:" + nameId + " new client")
            print("[INFO]/image: name:", nameId, " new client")
            indexClient = bufferClients.insertNewClient(nameId=nameId)
        indexClient = bufferClients.getClientIndex(nameId=nameId)
        if indexClient is None:
            logging.error("/image: name:" + nameId + " failed finding client")
            print("[ERROR]/image: name:", nameId, " failed finding client")
            return ("Failed finding client or inserting new client " + nameId, 400)
        
        (msg, succ) = bufferClients.buff[indexClient].saveNewImage(imageContent=imagestr)
        if succ is False:
            logging.error(msg)
            print("[ERROR]", msg)
            # return (msg, 400)
            return ("KO", 400)
        else:
            logging.info(msg)
            print("[INFO]", msg)
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
        #         logging.info(msg)
        #         #bufferImages.Print()
        #     else:
        #         logging.error(msg)
        #         #app.logger.error(msg)

    # unused but lets return something
    # data = {"data": "Received image"}
    #return jsonify({"info":"ok"}, 200)
    return ("OK", 200)

@app.route("/camera", methods=['GET'])
def upload():
    logging.debug("/camera endpoint" + str(request.method))
    print("[DEBUG]/camera endpoint", request.method)
    #here pass a parameter url for the post image inside render template
    #app.logger.debug("/camera endpoint: pid: " + str(os.getpid()))
    return render_template("camera.html", usedUrl = str(request.url_root), nameId = STR_UNKNOWN)

# called by c++ client
@app.route("/lastimage_filename",  HERE nameId methods=["GET"])
def lastimage_filename():
    filenameWithStamp =  bufferImages.buffer[bufferImages.lastRecordedIndex].filenameWithStamp
    pathImage = os.path.join("images", filenameWithStamp) 

# called by c++ client
@app.route("/lastimage", methods=["GET"])
def getlastimage():
    print("[DEBUG]/lastimage: ")
    # filename = os.path.join(get_test_dir(get_root_dir()), "data", "small.jpg")
    filenameWithStamp = bufferImages.buffer[bufferImages.lastRecordedIndex].filenameWithStamp
    pathImage = os.path.join("images", filenameWithStamp)

    print("[DEBUG]/lastimage: ", pathImage)
    if os.path.exists(pathImage) is False:
        msg = "[ERROR]/getlastimage image does not exists on disk: " + pathImage
        dict_out = {
            "information": "KO",
            "details": msg
        }
        logging.error(msg)
        return dict_out
    if os.path.isfile(pathImage) is False:
        msg = "[ERROR]/getlastimage image exist but is not a valid file: " + pathImage
        dict_out = {
            "information": "KO",
            "details": msg
        }
        logging.error(msg)
        return dict_out

    with open( pathImage, mode="rb" ) as f:
       imageContent = f.read()
       return imageContent

# called by python thread manager for c++ cleint ecovision
@app.route("/active_clients", methods=["GET"])
def active_clients():
    for clientEl in bufferClients:
        

# TODO thread to remove unactive clients

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
