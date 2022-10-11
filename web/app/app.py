import os
import base64
from flask import Flask, render_template, request, send_from_directory, jsonify, json
#from numpy import isin
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

OUTPUT_PATH = os.path.join(APP_ROOT, "results")
if os.path.exists(OUTPUT_PATH) is False:
    os.mkdir(OUTPUT_PATH)

app.debug = True

@app.route("/")
def index():
    app.logger.debug("/ endpoint: pid: " + str(os.getpid()))

    data = {"data": "Hello Camera3"}
    return jsonify(data)

@app.route("/image", methods=['POST'])
def image():
    app.logger.debug("/image endpoint: pid: " + str(os.getpid()))

    # return render_template("upload.html")
    # return send_from_directory('/images','test.jpeg')
    # print(request)

    # DATA: b'{"email":"hello@user.com","response":{"name":"Tester"},"image":"data:image/png;base64,iVBORw0KGgoAAAANSUh
    #print("DATA:", request.data)

    # bytes to string
    # jsonstr: {"email":"hello@user.com","response":{"name":"Tester"},"image":"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUAAAA
    jsonstr = request.data.decode('utf8')

    # string to json
    data = json.loads(jsonstr)

    # we could go further into beauty
    #s = json.dumps(data, indent=4, sort_keys=True)
    #print(s)


    # ok
    #print("email:", data["email"])
    #print("response:", data["response"])
    #print("image data:", data["image"])

    imagestr = data["image"]
    if isinstance(imagestr, str) is False:
        print("error decoding string")
    else:
        captured_image_path = os.path.join(OUTPUT_PATH, "sample.png") 
        with open(captured_image_path, 'wb') as f:
            #f.write(base64.decodestring(imagestr.split(',')[1].encode()))
            f.write(base64.b64decode(imagestr.split(',')[1].encode()))

    # unused but lets return something
    data = {"data": "Received image"}
    return jsonify(data)

@app.route("/camera", methods=['GET'])
def upload():

    here pass a parameter url for the post image inside render template

    app.logger.debug("/camera endpoint: pid: " + str(os.getpid()))
    return render_template("camera.html")

#if __name__ == "__main__":
#    app.run(port=5000, debug=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
