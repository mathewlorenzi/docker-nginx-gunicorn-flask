# from datetime import datetime
# import base64
# from base64 import b64encode
# from time import sleep
# from charset_normalizer import detect
#from base64 import base64
# import requests

# TODO filewatcher ... or in camera.html launch a second sceript to do this job
# TODO or manager.py to send a clean endpoint to do filewatcher job.
# TODO or look for flask refreshing option

# get username from form
# https://github.com/fossasia/Flask_Simple_Form/blob/master/nagalakshmiv2004/Form.py

# from PIL import Image, ImageDraw

# V1 ecovisionResults => old2.py
# v2 ecovisionResults

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




    # now = datetime.now()
    # date_time = convertDatetimeToString(now)    
    #timestamp = data["timestamp"]
    # print(" ... record_image_or_result: sent at ", timestamp, " vs now ", date_time)
    #imageContentStr = data["image"]