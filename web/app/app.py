import os
import base64
from flask import Flask, render_template, request, send_from_directory, jsonify, json
#from numpy import isin
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

class AppImage:
    def __init__(self, filenameWithStamp: str):
        get current timestamp without space here instead
        self.filenameWithStamp = filenameWithStamp

class BufferImages:
    def __init__(self, maxLength: int, directory: str):
        self.directory = directory
        self.maxLength = maxLength
        self.buffer = []
        self.lastRecordedIndex = -1
    def insert(self, inputImage: AppImage):
        if self.lastRecordedIndex < 0:
            self.buffer.append(inputImage)
            self.lastRecordedIndex = 0
            if len(self.buffer) != 1:
                print("error inserting at 0")
                return False
        elif self.lastRecordedIndex == self.maxLength:
here
        self.lastRecordedIndex += 1 # -1->0, 9->10
        if self.lastRecordedIndex == self.maxLength:
            self.lastRecordedIndex = -1

lastindex 
-1 0
0 1
1 2

OUTPUT_PATH = os.path.join(APP_ROOT, "output")
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
    # bytes to string
    jsonstr = request.data.decode('utf8')
    # string to json
    data = json.loads(jsonstr)
    # we could go further into beauty: s = json.dumps(data, indent=4, sort_keys=True)

    imagestr = data["image"]
    if isinstance(imagestr, str) is False:
        print("error decoding string")
    else:

        filenameWithStamp = getCurrentTimestamp()

        with open(os.path.join(bufferImages.directory, filenameWithStamp), 'wb') as f:
            #f.write(base64.decodestring(imagestr.split(',')[1].encode()))
            f.write(base64.b64decode(imagestr.split(',')[1].encode()))

            appImage = AppImage(filenameWithStamp=filenameWithStamp)
            bufferImages.insert(appImage)

    # unused but lets return something
    data = {"data": "Received image"}
    return jsonify(data)

@app.route("/camera", methods=['GET'])
def upload():
    #here pass a parameter url for the post image inside render template
    #app.logger.debug("/camera endpoint: pid: " + str(os.getpid()))
   return render_template("camera.html")

# called by c++ client
@app.route("/getlastimage", methods=["GET"])
def image() -> str:
   filename = os.path.join(get_test_dir(get_root_dir()), "data", "small.jpg")
   with open( filename, mode="rb" ) as f:
       imageContent = f.read().decode("iso-8859-1")
       #(open(input_filename, "rb").read()).decode("iso-8859-1")
       dict_out = {
           "timestamp": "TODO_or_willbeinfilename",
           "filename": "small.jpg",
           "stream": imageContent
       }
       return dict_out

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
