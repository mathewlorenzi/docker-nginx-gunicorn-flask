


# Envoyé: jeudi 27 octobre 2022 à 19:40
# De: "etienne corvee" <etienne.corvee@caramail.com>
# À: "etienne corvee" <etienne.corvee@caramail.com>
# Objet: TODO server_simul
"""import python modules"""
import os
#import io
import sys
# import shutil
# import uuid
# import json
# import signal
import cv2
# import numpy as np
# import base64
import logging
import time
# from logging.handlers import RotatingFileHandler
# import werkzeug
# from werkzeug.utils import secure_filename
# from werkzeug.middleware.shared_data import SharedDataMiddleware
from datetime import datetime
import shutil
from flask import (
    Flask,
    request,
    render_template,
    Response,
    send_from_directory,
    send_file,
    jsonify,
    redirect,
)
from flask.logging import create_logger
    
def get_root_dir() -> str:
    """returns the path of the root directory"""
    head, _ = os.path.split(os.path.dirname(__file__))
    return os.path.abspath(os.path.join(head))

def update_python_path_with_root_folder() -> None:
    """add to PYTHONPATH the path of the root folder of this project"""
    if os.path.abspath(get_root_dir()) not in sys.path:
        sys.path.append(get_root_dir())
  
OUTPUT_DIR="output_server_simul"
camIds = ["peter", "paul", "jack", "UNKNOWN"]  
def populate_fake_images():
    if os.path.isdir(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.mkdir(OUTPUT_DIR)
    for dir in camIds:
        os.mkdir(os.path.join(OUTPUT_DIR, dir))
    img = cv2.imread("sample.png")
    for dir in camIds:
        for nb in range(10):
            now = datetime.now()
            date_time = now.strftime("%m-%d-%YT%H:%M:%S.%f")[:-3]
            print("date_time:", dir, date_time)
            cv2.imwrite(os.path.join(OUTPUT_DIR, dir, date_time+".jpg"), img)
            time.sleep(0.5)
  
# populate_fake_images()
# exit(1)
  
update_python_path_with_root_folder()
  
# app = Flask(__name__, template_folder=get_templates_dir(get_root_dir()))
app = Flask(__name__)
logger = create_logger(app)
  
# Set to debug level and create log file
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger.setLevel(logging.DEBUG)
# handler = RotatingFileHandler(log_path, maxBytes=10000, backupCount=1)
# handler.setLevel(logging.DEBUG)
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# app.secret_key = "D0Zr98j/3yX R~XHH!jmN]LWX/,?FM"
# app.config["PERMANENT_SESSION_LIFETIME"] = 30  # la session dure x secondes
# #app.config["APPLICATION_ROOT"] = "/appname/"
  
@app.route("/status", methods=["GET"])
def appstatus():
    return ("UP", 200)
  
# download / display
@app.route("/uploads/<filename>", methods=["GET"])
def uploaded_file(filename: str) -> Response:
    """download a result file form the uploads folder"""
    # this line is covered in test function: test_download_file_in_uploads_folder (test_routes.py)
    return send_from_directory(
        get_uploads_dir(get_root_dir()), filename
    )  # pragma: no cover
  
@app.route("/active_client_cam_all_images", methods=["GET"])
def active_client_cam_all_images():
#@app.route("/active_client_cam/<int:maxagesec>", methods=["GET"])
#def active_client_cam(maxagesec: int):
    #print("maxagesec: ", maxagesec)
    listout = []
    for dir in camIds:
        for file in os.listdir(os.path.join(OUTPUT_DIR, dir)):
            listout.append((dir, file))
            #print(dir, file)
    #return (listout, 200)
    return jsonify(data=listout), 200
  
@app.route("/active_client_cam", methods=["GET"])
def active_client_cam():
#@app.route("/active_client_cam/<int:maxagesec>", methods=["GET"])
#def active_client_cam(maxagesec: int):
    #print("maxagesec: ", maxagesec)
    listout = []
    for dir in camIds:
        listout.append(dir)
    return jsonify(data=listout), 200
  
@app.route("/uploaded_image/<string:camId>/<string:filename>", methods=["GET"])
def uploaded_image(camId: str, filename: str):
    inputpath = os.path.join(OUTPUT_DIR, camId, filename)
    print(inputpath)
    with open(inputpath, mode="rb") as f:
        return (f.read(), 200)
    return ("KO", 400)
  
@app.route("/last_image_content/<string:camId>", methods=["GET"])
def last_image_content(camId: str):
    # take first encountered filename as last recorded one
    for filename in os.listdir(os.path.join(OUTPUT_DIR, camId)): 
        inputpath = os.path.join(OUTPUT_DIR, camId, filename)
        print(inputpath)
        with open(inputpath, mode="rb") as f:
            return (f.read(), 200)
    return ("KO", 400)
  
@app.route("/last_image_filename/<string:camId>", methods=["GET"])
def last_image_filename(camId: str):
    # take first encountered filename as last recorded one
    for filename in os.listdir(os.path.join(OUTPUT_DIR, camId)): 
        #inputpath = os.path.join(OUTPUT_DIR, camId, filename)
        print("return:->"+filename+"<-")
        return (filename, 200)
    return ("KO", 400)
  
if __name__ == "__main__":
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.run(host="0.0.0.0", port=5000)  # pragma: no cover