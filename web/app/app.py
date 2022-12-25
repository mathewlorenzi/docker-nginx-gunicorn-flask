
import os
import sys
import logging

# in docker, local files cannot be found: add current path to python path:
# file_path = os.path.dirname(os.path.realpath(__file__))
# if file_path not in sys.path:
#     sys.path.insert(1, file_path)
# printRootStructure(dirname=sys.path[0], indent=0)

from flask import Flask, render_template, request, jsonify, json
#from utils import get_encoded_img, get_cpu_ram_disk
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

# TODO automatic
#BACKEND_URL = 'http://127.0.0.1:5555'
BACKEND_URL = 'http://backend:5555'

@app.route("/hello")
def hello():
    print("[DEBUG]/hello endpoint: pid: " + str(os.getpid()))
    data = {"data": "Hello Camera3"}
    # uri_result = load_sample("sample.png")
    return jsonify(data)

@app.route("/camera", methods=['GET'])
def upload():
    print("[DEBUG]/camera endpoint" + str(request.method))
    return render_template("camera.html", usedUrl = str(request.url_root), nameId = STR_UNKNOWN)#, uri_result=uri_result)

@app.route('/update_values', methods= ['GET'])
def update_values():
    (cpu, ram, disk) = get_cpu_ram_disk()
    return jsonify(cpu=cpu, ram=ram, disk=disk)


@app.route('/', methods=['GET', 'POST'])
def mainroute():
    print("[DEBUG]/ main endpoint: pid: " + str(os.getpid()))
    if request.method == 'GET':
        return render_template('form.html')
    elif request.method == 'POST':
        print("[DEBUG]redirect to camera with name: " + request.form['username'] + " with captureInterval " + request.form['captureInterval'] + " from " + request.url_root)
        return render_template('camera.html', usedUrl = str(request.url_root), nameId = request.form['username'], captureInterval = request.form['captureInterval'])#, uri_result=uri_result)

# this is called within the camera.html: var url = 'https://www.ecovision.ovh:81/image';sam
# the camera, javascript post its image to this endpoint
@app.route("/image", methods=['POST'])
def image():
    # print("[INFO]/image POST")

    # content = {'image': self.im_b64, 'nameId': self.camId, 'usedUrl': 'frontend'}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(BACKEND_URL+"/record_image", data=request.data, headers=headers)
    # print(response)
    # print(response.content)
    # print(response.status_code)
    # return ("debug", 200)
    return (response.content, response.status_code)
    #post("http://backend/record_image", data=)
    #(msg, camId, status) = record_image_or_result(inputBufferClient=bufferClients, info="input")
    # the camera.html (client) exects the result as a reply or a red image if ecovision did not reply a fresh result yet

        
# # reply to ecovision
# @app.route("/result", methods=['POST'])
# def result():
#     print("[INFO]/result POST")
#     response = requests.post(BACKEND_URL+"/record_result", data=request.data)
#     return (response.content, response.status_code)
#     #(msg, camId, status) = record_image_or_result(inputBufferClient=ecovisionResults, info="result")
#     #return (msg, status)


@app.route("/lastimage/<string:camId>", methods=["GET"])
def lastimage(camId: str, take_care_of_already_uploaded: bool=True):
    response = requests.get(BACKEND_URL+"/lastimage/"+camId, data=request.data)
    return (response.content, response.status_code)
    # print("[INFO]/lastimage GET")
    # data[camId] = camId
    # data[careUpload] = reauest[]
    # get('http://backend/lastimage/: str, take_care_of_already_uploaded: bool=True):
    # # return lastsample(camId=camId, inputBufferClient=bufferClients, take_care_of_already_uploaded=take_care_of_already_uploaded)

@app.route("/lastresult/<string:camId>", methods=["GET"])
def lastresult(camId: str, take_care_of_already_uploaded: bool=True):
    response = requests.get(BACKEND_URL+"/lastresult/"+camId, data=request.data)
    return (response.content, response.status_code)
    # data[camId] = camId
    # data[careUpload] = reauest[]
    # get('http://backend/lastimage/: str, take_care_of_already_uploaded: bool=True):
    # #print("[INFO]/lastresult GET")
    # #return lastsample(camId=camId, inputBufferClient=ecovisionResults, take_care_of_already_uploaded=take_care_of_already_uploaded)

# called by python thread manager for c++ cleint ecovision
@app.route("/active_clients", methods=["GET"])
def active_clients():
    (listClients, statusCode) = requests.get(BACKEND_URL+"/active_clients")
    return (listClients, statusCode)

@app.route("/active_client_cam", methods=["GET"])
def active_client_cam():
    url = BACKEND_URL+"/active_client_cam"
    response = requests.get(url)
    listClients = response.content  #bytes: b'{\n  "data": []\n}\n'
    return (listClients, response.status_code)

if __name__ == '__main__':
    # to allow flask tu run in a thread add use_reloader=False, otherwise filewatcher thread blosk stuff
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    # shit i lost code about thread sessionrunner i think