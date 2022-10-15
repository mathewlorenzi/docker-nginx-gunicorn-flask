import os
import base64
import logging
from datetime import datetime
from flask import Flask, render_template, request, send_from_directory, jsonify, json
#from flask.logging import create_logger
#from numpy import isin
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.debug = True

#logging.basicConfig(level=logging.DEBUG)

# TODO log rotate
logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logging.warning('Start') 

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

class AppImage:
    def __init__(self):
        dt_obj = str(datetime.now())
        dt_obj = dt_obj.replace(" ", "")
        #print(dt_obj)
        self.filenameWithStamp = dt_obj + ".png"
        self.hasData = False
    def copyFrom(self, src):
        self.filenameWithStamp = src.filenameWithStamp
        self.hasData = src.hasData
    def Print(self):
        print(self.filenameWithStamp, self.hasData)
        
class BufferImages:
    def __init__(self, maxLength: int, directory: str):
        self.directory = directory
        self.maxLength = maxLength
        self.buffer = []
        self.lastRecordedIndex = -1
        # self.replacedImageFilename = None
        self.oldestRecordedImage = None
        for i in range(self.maxLength):
            appImage = AppImage();
            self.buffer.append(appImage)
    def insert(self, inputImage: AppImage):
        index_nimage = self.lastRecordedIndex + 1# NextImageNotReadyYetForUploadAsNot
        if index_nimage >= self.maxLength:
            index_nimage = 0
        
        # if self.lastRecordedIndex >= 0:
        #    self.replacedImageFilename = self.buffer[self.lastRecordedIndex].filenameWithStamp;
        
        self.buffer[index_nimage].copyFrom(inputImage)
        #now the image is in the buffer, fully saved, so it is available for the client => update index
        self.lastRecordedIndex = index_nimage;

        self.oldestRecordedImage = self.lastRecordedIndex + 1
        if self.oldestRecordedImage >= self.maxLength:
            self.oldestRecordedImage = 0

    def deleteOldest(self):
        if self.oldestRecordedImage is not None:
            pathImage = os.path.join(self.directory, self.buffer[self.oldestRecordedImage].filenameWithStamp)
            if self.buffer[self.oldestRecordedImage].hasData is False:                
                msg = "[INFO]oldest image cannot be deleted as it does not have any data (was not recorded before): " + pathImage
                return (msg, True)    
            if os.path.exists(pathImage) is False:
                msg = "[ERROR]oldest image cannot be deleted as it does not exists on disk: " + pathImage
                return (msg, False)
            if os.path.isfile(pathImage) is False:
                msg = "[ERROR]oldest image cannot be deleted as it is not a file: " + pathImage
                return (msg, False)
            os.remove(pathImage)
            if os.path.exists(pathImage) is True:
                msg = "[ERROR]oldest image was not successfully deleted, it still exist on disk: " + pathImage
                return (msg, False)
            if os.path.isfile(pathImage) is True:
                msg = "[ERROR]oldest image was not successfully deleted, it still is an existing file: " + pathImage
                return (msg, False)
            msg = "[INFO]oldest image was successfully deleted: " + pathImage
            self.buffer[self.oldestRecordedImage].hasData = False
            return (msg, True)
        msg = "[INFO]oldest image not yet recorded: cannot be yet deleted"
        return (msg, True)
        

    def Print(self):
        for i in range(self.maxLength):
            print(i, end=":")
            self.buffer[i].Print()

OUTPUT_PATH = os.path.join(APP_ROOT, "..", "..", "images")
logging.debug("check output folder: "+str(OUTPUT_PATH))
if os.path.exists(OUTPUT_PATH) is False:
    os.mkdir(OUTPUT_PATH)

bufferImages = BufferImages(maxLength=10, directory=OUTPUT_PATH)

#app.debug = True

@app.route("/")
def index():
#    app.logger.debug("/ endpoint: pid: " + str(os.getpid()))

    data = {"data": "Hello Camera3"}
    return jsonify(data)

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
    if isinstance(imagestr, str) is False:
        print("error decoding string")
    else:
        appImage = AppImage()
        filename = appImage.filenameWithStamp
        print("/image save ", filename)
        with open(os.path.join(bufferImages.directory, filename), 'wb') as f:
            #f.write(base64.decodestring(imagestr.split(',')[1].encode()))
            f.write(base64.b64decode(imagestr.split(',')[1].encode()))
            appImage.hasData = True
            bufferImages.insert(appImage)
            print("/image image ready at ", 
                bufferImages.lastRecordedIndex, 
                bufferImages.buffer[bufferImages.lastRecordedIndex].filenameWithStamp, 
                #" replaced image to be del: ", bufferImages.replacedImageFilename
                " oldest image to be del: ", bufferImages.oldestRecordedImage, 
                bufferImages.buffer[bufferImages.oldestRecordedImage].filenameWithStamp, 
                )
            bufferImages.Print()
            (msg, succ) = bufferImages.deleteOldest()
            print(succ, msg)
            if succ is True:
                bufferImages.Print()
            else:
                logging.error(msg)
                #app.logger.error(msg)

    # unused but lets return something
    data = {"data": "Received image"}
    return jsonify(data)

@app.route("/getimage", methods=['GET'])
def getImage():
    filename = os.path.join(bufferImages.directory, bufferImages.buffer[bufferImages.lastRecordedIndex].filenameWithStamp)
    with open( filename, mode="rb" ) as f:
       imageContent = f.read().decode("iso-8859-1")
       #(open(input_filename, "rb").read()).decode("iso-8859-1")
       dict_out = {
           "filename": filename,
           "stream": imageContent
       }
       return dict_out

@app.route("/camera", methods=['GET'])
def upload():
    #here pass a parameter url for the post image inside render template
    #app.logger.debug("/camera endpoint: pid: " + str(os.getpid()))
   return render_template("camera.html")

# called by c++ client
@app.route("/lastimage", methods=["GET"])
def getlastimage():
    # filename = os.path.join(get_test_dir(get_root_dir()), "data", "small.jpg")
    filenameWithStamp = bufferImages.buffer[bufferImages.lastRecordedIndex].filenameWithStamp
    pathImage = os.path.join("images", filenameWithStamp)

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
        imageContent = f.read().decode("iso-8859-1")
        #(open(input_filename, "rb").read()).decode("iso-8859-1")
        dict_out = {
            "information": "OK",
            "filenameWithStamp": filenameWithStamp,
            "stream": imageContent,
            "details": "none"
        }
        return dict_out

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
