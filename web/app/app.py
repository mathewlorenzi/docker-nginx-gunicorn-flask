import os
import base64
import logging
from flask import Flask, render_template, request, send_from_directory, jsonify, json, flash
from flask import redirect
from buffer_images import AppImage, BufferImages

# https://github.com/fossasia/Flask_Simple_Form/blob/master/nagalakshmiv2004/Form.py

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#logging.basicConfig(level=logging.DEBUG)

# TODO log rotate
logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logging.warning('Start') 

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(APP_ROOT, "..", "..", "images")
logging.debug("check output folder: "+str(OUTPUT_PATH))
if os.path.exists(OUTPUT_PATH) is False:
    os.mkdir(OUTPUT_PATH)

bufferImages = BufferImages(maxLength=10, directory=OUTPUT_PATH)

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
        logging.debug("redirect to camera with name: " + request.form['username'])
        print("[DEBUG]redirect to camera with name: ", request.form['username'])
        #return redirect('/camera', name = request.form['username'])
        return render_template('camera.html', name = request.form['username'])

# @app.route('/form', methods=['GET', 'POST'])
# def contactform():
#     logging.debug("/form endpoint: pid: " + str(os.getpid()))
#     print("[DEBUG]/form endpoint: pid: ", str(os.getpid()))
# 	form = ContactForm()
# 	if request.method == 'GET':
# 		return render_template('contact.html', form=form)
# 	elif request.method == 'POST':
# 		if form.validate() == False:
# 			flash('All fields are required !')
# 			return render_template('contact.html', form=form)
# 		else:
# 			msg = Message(form.subject.data, sender='[SENDER EMAIL]', recipients=['your reciepients gmail id'])
# 			msg.body = """
# 			from: %s &lt;%s&gt
# 			%s
# 			"""% (form.name.data, form.email.data, form.message.data)
# 			mail.send(msg)
# 			return redirect(url_for('index'))
# 		return '<h1>Form submitted!</h1>'  

# @app.route('/contact', methods=['POST', 'GET'])
# def contact():
#     form = ContactForm()
#     if form.validate_on_submit():        
#         print('-------------------------')
#         print(request.form['name'])
#         print(request.form['email'])
#         print(request.form['subject'])
#         print(request.form['message'])       
#         print('-------------------------')
#         send_message(request.form)
#         return redirect('/success')      
#     return render_template('views/contacts/contact.html', form=form)

# @app.route('/success')
# def success():
#     return redirect('/camera') # return render_template('views/home/index.html')

def send_message(message):
    print(message.get('name'))
    #msg = Message(message.get('subject'), sender = message.get('email'),
    #        recipients = ['id1@gmail.com'],
    #        body= message.get('message')
    #)  
    #mail.send(msg)

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
    # data = {"data": "Received image"}
    return jsonify(data)

# @app.route("/getimage", methods=['GET'])
# def getImage():
#     filename = os.path.join(bufferImages.directory, bufferImages.buffer[bufferImages.lastRecordedIndex].filenameWithStamp)
#     with open( filename, mode="rb" ) as f:
#        imageContent = f.read().decode("iso-8859-1")
#        #(open(input_filename, "rb").read()).decode("iso-8859-1")
#        dict_out = {
#            "filename": filename,
#            "stream": imageContent
#        }
#        return dict_out

@app.route("/camera", methods=['GET'])
def upload():
    logging.debug("/camera endpoint" + str(request.method))
    print("[DEBUG]/camera endpoint", request.method)
    #here pass a parameter url for the post image inside render template
    #app.logger.debug("/camera endpoint: pid: " + str(os.getpid()))
    return render_template("camera.html")

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


#TODO at start (or using a deamon thread) clean all images before curernt timestamp 

    # with open( pathImage, mode="rb" ) as f:
    #     imageContent = f.read().decode("iso-8859-1")
    #     #(open(input_filename, "rb").read()).decode("iso-8859-1")
    #     dict_out = {
    #         "information": "OK",
    #         "filenameWithStamp": filenameWithStamp,
    #         "stream": imageContent,
    #         "details": "none"
    #     }
    #     return dict_out

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
