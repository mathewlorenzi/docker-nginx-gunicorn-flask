
#FLIP = 0

class LocalConfig:
    def __init__(self):
        self.flip=0
        self.check_activated = False
        # self.last_connection = datetime
        # HERE
        
localconfig = LocalConfig()


# V1 ecovisionResults
# class EcovisionResults:
#     def __init__(self):
#         self.trackResultsImage = {}
#         #self.recttblr = []
# ecovisionResults = EcovisionResults()
'''@app.route("/result/<string:camId>", methods=['POST'])
def result(camId: str):
    # bytes to string
    jsonstr = request.data.decode('utf8')
    print(" ........ camId ", camId)
    # print(" ........ result ->", jsonstr, "<-")
    #print(type(jsonstr))
    # string to json
    data = json.loads(jsonstr)

    ecovisionResults.trackResultsImage[camId] = data['png']

    # OK
    # with open("./tempdebug.png", mode="wb") as ftdg:
    #     content = base64.b64decode(data['png'].encode())
    #     ftdg.write(content)

    # print(" ........ result ", request.data)
    # print(" ........ result ", request.form)
    # print(" ........ result ", request.content_encoding)
    # print(" ........ result ", jsonstr, "camId", camId)
    # print(" ........ result camId", camId, "data", data)
    #  ........ result -> { "nbtracks" : 1, "type" :  "tblr" , " 1 "  : [ 2, 121, 175, 317 ] } <-
    # return (data, 200)
    
    # OK but we dont care anymore
    # if 'nbtracks' in data:
    #     print(" ........ data['nbtracks'] ", data['nbtracks'])
    #     if not 'type' in data:
    #         msg = '[ERROR]type not present in json data'
    #         print(msg)
    #         return (msg, 400)
        
        
    #     # get last image
    #     dictLastImageTuple = lastimage(camId, take_care_of_already_uploaded=False)
    #     #print(" ........ dictLastImageTuple len ", len(dictLastImageTuple))
    #     print(" ........ dictLastImageTuple[0]", type(dictLastImageTuple[0]))
    #     print(" ........ dictLastImageTuple[1]", type(dictLastImageTuple[1]))
    #     if isinstance(dictLastImageTuple[0], dict) is False:
    #         msg = '[ERROR]message content in tuple returned from /lastimage is not a string'
    #         print(msg)
    #         return (msg, 400)
    #     if isinstance(dictLastImageTuple[1], int) is False:
    #         msg = '[ERROR]http code error in tuple returned from /lastimage is not an int'
    #         print(msg)
    #         return (msg, 400)
    #     if dictLastImageTuple[1] != 200:
    #         msg = '[ERROR]http code error returned from /lastimage is: ' + str(dictLastImageTuple[1])
    #         print(msg)
    #         return (msg, 400)

    #     dictLastImage = dictLastImageTuple[0]
    #     print(" ........ dictLastImage ", type(dictLastImage))
    #     if 'dateTime' not in dictLastImage:
    #         msg = '[ERROR]dateTime no in data returned from /lastimage'
    #         print(msg)
    #         return (msg, 400)
    #     if 'filenameWithStamp' not in dictLastImage:
    #         msg = '[ERROR]filenameWithStamp no in data returned from /lastimage'
    #         print(msg)
    #         return (msg, 400)
    #     if 'hasData' not in dictLastImage:
    #         msg = '[ERROR]hasData no in data returned from /lastimage'
    #         print(msg)
    #         return (msg, 400)
    #     # do i use it here ?
    #     if 'uploaded' not in dictLastImage:
    #         msg = '[ERROR]uploaded no in data returned from /lastimage'
    #         print(msg)
    #         return (msg, 400)
    #     if 'contentBytes' not in dictLastImage:
    #         msg = '[ERROR]contentBytes no in data returned from /lastimage'
    #         print(msg)
    #         return (msg, 400)
        
    #     if isinstance(dictLastImage['hasData'], str) is False:
    #         msg = '[ERROR]hasData is not a string in data returned from /lastimage:' + str(type(dictLastImage['hasData']))
    #         print(msg)
    #         return (msg, 400)

    #     if dictLastImage['hasData'] != "True":
    #         msg = '[WARNING]hasData is false in data returned from /lastimage'
    #         print(msg)
    #         return (msg, 202)

    #     # TODO a function to check all and not none and tpes

    #     print(" ........ type(dictLastImage['contentBytes']) ", type(dictLastImage['contentBytes']))
    #     contentByteStr = dictLastImage['contentBytes']
    #     ecovisionResults.trackResultsImage = contentByteStr

    #     # TODO avoid writing to disk
    #     # instead: 
    #     # im1 = im.tobytes("xbm", "rgb")
    #     # img = Image.frombuffer("L", (10, 10), im1, 'raw', "L", 0, 1)
    #     with open("debug.png", mode="wb") as fdebugout:
    #         fdebugout.write(base64.b64decode(contentByteStr.encode()))        
    #     rimg = Image.open("debug.png")        
    #     rimg_draw = ImageDraw.Draw(rimg)
    #     rimg_draw.rectangle((10, 10, 30, 30), fill=None, outline=(255, 0, 0))
    #     rimg.save("debug.png")
    #     # then replace the todel or ? by this one
        
    #     chec_nbTracks = 0
    #     ecovisionResults.recttblr = []
    #     for el in data:
    #         if el != 'nbtracks' and el != 'type':
    #             chec_nbTracks += 1
    #             print(" ........ el ", el)
    #             # print(" ........ el data ", data[el])
    #             if data['type'] == 'tblr':
    #                 print(" ........ tblr ", el, data[el][0], data[el][1], data[el][2], data[el][3])
    #                 ecovisionResults.recttblr.append(data[el])
    #                 # draw rectangle on result_image
    #             elif data['type'] == 'tltrblbr-rc':
    #                 return ("tltrblbr-rc not yet done", 202)
    #             else:
    #                 return ("wrong track type", 400)
    
    
    # return (recttblr, 200)
    return ("ok", 200)
'''


# @app.route("/debug_last_recorded_index/<string:camId>", methods=["GET"])
# def debug_last_recorded_index(camId: str):
#     logger.debug("/debug_last_recorded_index camId " + str(camId))
#     if camId is None:
#         return ("camId not present in url", 400)    
#     if camId == "":
#         return ("nameId is empty in url", 400)
    
#     index = bufferClients.getClientIndex(camId)
#     if index is None:
#         return ("no client with camId: " + camId, 400)

#     lastRecordedIndex = bufferClients.buff[index].bufferImages.lastRecordedIndex
#     logger.debug("/debug_last_recorded_index camId " + str(camId) + " lastRecordedIndex " + str(lastRecordedIndex))
#     return (str(lastRecordedIndex), 200)



# # called by c++ client
# #@app.route("/lastimage_filename/<string:nameId>", methods=["GET"])
# @app.route("/last_image_filename/<string:camId>", methods=["GET"])
# def lastimage_filename(camId: str):
#     logger.debug("/lastimage_filename camId " + str(camId))
#     #print("[DEBUG]/lastimage_filename nameId ", nameId)
#     if camId is None:
#         return ("camId not present in url", 400)    
#     if camId == "":
#         return ("nameId is empty in url", 400)
    
#     index = bufferClients.getClientIndex(camId)
#     if index is None:
#         return ("no client with camId: " + camId, 400)
    
#     lastRecordedIndex = bufferClients.buff[index].bufferImages.lastRecordedIndex
#     logger.debug("/last_image_filename camId " + str(camId) + " lastRecordedIndex " + str(lastRecordedIndex))

#     filenameWithStamp = bufferClients.buff[index].bufferImages.buffer[lastRecordedIndex].filenameWithStamp
#     logger.debug("/last_image_filename camId " + str(camId) + " filenameWithStamp " + str(filenameWithStamp))
#     #pathImage = os.path.join("images", filenameWithStamp) 
    
#     return (filenameWithStamp, 200)

# # called by c++ client
# @app.route("/is_last_image_uploaded/<string:camId>", methods=["GET"])
# def is_last_image_uploaded(camId: str):
#     index = bufferClients.getClientIndex(camId)
#     if index is None:
#         msg = "no client with camId although we found it last image filename: " + camId
#         logger.error(msg)
#         return (msg, 400)
#     lastRecordedIndex = bufferClients.buff[index].bufferImages.lastRecordedIndex
#     logger.debug("/is_last_image_uploaded camId " + str(camId) + " lastRecordedIndex " + str(lastRecordedIndex))

#     uploaded = bufferClients.buff[index].bufferImages.buffer[lastRecordedIndex].uploaded
#     logger.debug("/is_last_image_uploaded camId " + str(camId) + " uploaded " + str(uploaded))
#     return (str(uploaded), 200)

# # called by c++ client
# #@app.route("/lastimage/<string:nameId>", methods=["GET"])
# @app.route("/last_image_content/<string:camId>", methods=["GET"])
# def lastimage_content(camId: str):
#     #print("[DEBUG]/lastimage: nameId: ", nameId)
#     # filename = os.path.join(get_test_dir(get_root_dir()), "data", "small.jpg")
#     # filenameWithStamp = bufferImages.buffer[bufferImages.lastRecordedIndex].filenameWithStamp
#     # pathImage = os.path.join("images", filenameWithStamp)

#     #(filenameWithStamp, succ) = lastimage_filename(camId = camId)
#     #if succ != 200:
#     #    return (filenameWithStamp, 400)

#     index = bufferClients.getClientIndex(camId)
#     if index is None:
#         return ("no client with camId although we found it last image filename: " + camId, 400)

#     lastRecordedIndex = bufferClients.buff[index].bufferImages.lastRecordedIndex
#     logger.debug("/last_image_content camId " + str(camId) + " lastRecordedIndex " + str(lastRecordedIndex))

#     if lastRecordedIndex is None:
#         msg = "lastRecordedIndex None: camId: " + camId
#         logger.error(msg)
#         return (msg, 400)
#     if lastRecordedIndex < 0:
#         msg = "lastRecordedIndex negative: camId: " + camId
#         logger.error(msg)
#         return (msg, 400)

#     filenameWithStamp = bufferClients.buff[index].bufferImages.buffer[lastRecordedIndex].filenameWithStamp
#     logger.debug("/last_image_content camId " + str(camId) + " filenameWithStamp " + str(filenameWithStamp))
    
#     pathImage = os.path.join(bufferClients.buff[index].outputDir, filenameWithStamp)

#     #print("[DEBUG]/lastimage: =======> ", pathImage)
#     if os.path.exists(pathImage) is False:
#         msg = "[ERROR]/getlastimage image does not exists on disk: " + pathImage
#         # dict_out = {
#         #     "information": "KO",
#         #     "details": msg
#         # }
#         logger.error(  msg)
#         return (msg, 400)
#     if os.path.isfile(pathImage) is False:
#         msg = "[ERROR]/getlastimage image exist but is not a valid file: " + pathImage
#         # dict_out = {
#         #     "information": "KO",
#         #     "details": msg
#         # }
#         logger.error(msg)
#         # return (dict_out, 400)
#         return (msg, 400)

#     with open( pathImage, mode="rb" ) as f:
#         imageContent = f.read()
#         bufferClients.buff[index].bufferImages.buffer[lastRecordedIndex].uploaded = True
#         logger.info("uploading image content to client")
#         return (imageContent, 200)
#         # TODO why no more displayed in webrowser


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

# @app.route("/result/<string:camId>", methods=['GET'])
# def getresult(camId: str):
#     return (jsonify(ecovisionResults.recttblr), 200)

# @app.route("/update_rects/<string:camId>", methods=['GET'])
# def update_rects(camId: str):
#     return jsonify(ecovisionResults.recttblr)


# flip image
@app.route("/result_image/<string:camId>", methods=['GET'])
def result_image(camId: str):
    print("/result_image localconfig.flip", localconfig.flip)
    logger.debug("/result_image endpoint: " + str(localconfig.flip))
    # data = {"data": "Hello Camera3"}
    # return jsonify(data)

    if localconfig.flip == 0:
        imgPath = "sample.png"
        localconfig.flip = 1
    else:
        imgPath = "todel.png"
        localconfig.flip = 0

    print("/result_image imgPath", imgPath)

    with open(imgPath, mode="rb") as fsample:
        img_data = fsample.read()
        encoded = b64encode(img_data)
        decoded_img = encoded.decode('utf-8')
        #uri_result = f"data:image/jpeg;base64,{decoded_img}"
        #mime = "image/jpeg"
        #uri_result = "data:%s;base64,%s" % (mime, encoded)
        return (decoded_img, 200)

    return ("YYYYYYYYYYYYYYYYYEEEEEEESS", 200)