import os
import psutil
import base64
from datetime import datetime
import logging

from buffer_images import BufferClients
from utils import is_port_in_use, check_port

# All ports from 1–65535 support TCP

# this technique create too large number
# import math
# def convertToNumber (s):
#     return int.from_bytes(s.encode(), 'little')
# def convertFromNumber (n):
#     return n.to_bytes(math.ceil(n.bit_length() / 8), 'little').decode()
# x = convertToNumber('foo bar baz')
# convertFromNumber(x)

class PortGenerator:
    def __init__(self):
        self.minPort = 9000 # to avoid the ones in the 5000 and 8000 or 1024 # or 1
        self.maxPort = 65534 # or 65535
        self.currPort = self.minPort
    def getNewPort(self):
        safeCounter=0
        while(True):
            safeCounter+=1
            currPort = self.currPort
            if is_port_in_use(currPort) is False:
            # if check_port(currPort) is False:
                self.currPort += 1
                if self.currPort>=self.maxPort:
                    self.currPort=self.minPort
                print("[INFO] ... found new port: ", self.currPort)
                return currPort
            else:
                self.currPort += 1
            if safeCounter > 65535:
                print("[ERROR]Impossible: all ports are used")
                return -1

portGenerator = PortGenerator()

def record_image_or_result(inputBufferClient: BufferClients, camId: str,
                            imageContentStr: str, 
                            imageContentBytes: bytes, 
                            logger):
    nameId = camId # data["nameId"]

    if imageContentStr is not None:
        if isinstance(imageContentStr, str) is False:
            print("[ERROR]/image: imageContentStr is not a string:", type(imageContentStr))
            return ("KO: imageContentStr is not a string", 400)
    else:
        if imageContentBytes is not None:
            if isinstance(imageContentBytes, bytes) is False:
                print("[ERROR]/image: imageContentBytes is not bytes:", type(imageContentBytes))
                return ("KO: imageContentBytes is not bytes", 400)

    

    if isinstance(nameId, str) is False:
        print("[ERROR]/image: nameId is not a string:" + str(nameId))
        return ("KO: nameId is not a string", nameId, 400)

    # look if existing active camera
    indexClient = inputBufferClient.getClientIndex(nameId=nameId)
    if indexClient is None:
        print("[INFO]/image: nameId:" + nameId + " new client")

        newPort = portGenerator.getNewPort()
        if newPort<0:
            return ("KO: failed to find a free new port for a new ecovision job", nameId, 400)

        (_msg, indexClient) = inputBufferClient.insertNewClient(nameId=nameId, tcpPort=newPort)
        if indexClient is None:
            errMsg = "/image: nameId:" + nameId + " failed inserting new client " + _msg
            # logger.error(errMsg)
            print("[ERROR]", errMsg)
            return (errMsg, nameId, 400)

    # check really necessary ?
    indexClient = inputBufferClient.getClientIndex(nameId=nameId)
    if indexClient is None:
        print("[ERROR]/image: nameId:" + nameId + " failed finding client")
        return ("KO: Failed finding client or inserting new client " + nameId, nameId, 400)
    
    print("[DEBUG]/image: nameId:" + nameId + " indexClient: " + str(indexClient))

    # while(inputBufferClient.buff[indexClient].lockOnUpload is True){
    #     print("[INFO]/image: lock active, wait a bit, for camId" + nameId)
    #     time.sleep(1)
    # }
    # lockOnUpload = False
    # imageToBeUploaded = AppImage()

    (msg, succ) = inputBufferClient.buff[indexClient].insertNewImage(logger=logger, 
                                                                    imageContentStr=imageContentStr,
                                                                    imageContentBytes=imageContentBytes)
    if succ is False:
        print("[ERROR]", msg)
        return ("KO: failed saving new image", nameId, 400)
    else:
        print("[INFO]", msg)

        # camId = nameId
        # print("[DEBUG]/result_image2 endpoint")
        # v1
        # if camId in ecovisionResults.trackResultsImage:
        #     return (ecovisionResults.trackResultsImage[camId], nameId, 200)
        # else:
        #     return ("ok but image result from ecovision not ready yet for " + camId, nameId, 202)
        # v2 return a blank image if not ready
        # indexECO = bufferEcovisionResults.getClientIndex(nameId=nameId)
        # if indexECO is None:
        #     print("[ERROR]/image: nameId:" + nameId + " failed finding client in ecovision results")
        #     return (HERE blank image, nameId, 202)
        # bufferEcovisionResults.buff[indexECO].get last image
    
        # HERE    

        return ("OK", nameId, 200)
    return ("OK", nameId, 200)

def lastsample(camId: str, inputBufferClient: BufferClients, logger, take_care_of_already_uploaded: bool=True):
    # called by httpclient or ecovision :
    # prog_v2.h
    #   httpRequestUtils getRequester;
    #   httpRequestUtils postRequester; 
    # prog_exe_v2.cpp
    #   getRequester.getRequestImage(...)
    #   postRequester.postRequestJsonMessage(...)
    # curl_request.h
    #   httpRequestUtils::getRequestImage(...)          ==>  url /lastimage/camId ... getCurler
    #   httpRequestUtils::postRequestJsonMessage(...)   ==>  url /result/camId ... postCurler
    #   /result/

    # 405 error (that shoukd be handled by flask)
    # 404 programming error
    # 400 client/camId not present in list of current clients
    # 204 ok but already uploaded last image
    # 200 ok, last image returned

    print("[DEBUG]lastsample camId " + str(camId) + "/" + inputBufferClient.TYPE)
    if camId is None:
        msg = "camId in None in url" + " /" + inputBufferClient.TYPE
        # logger.error(msg)
        print("[ERROR]", msg)
        return (msg, 405)    
    if camId == "":
        msg = "nameId is empty in url" + " /" + inputBufferClient.TYPE
        # logger.error(msg)
        print("[ERROR]", msg)
        return (msg, 405)
    
    index = inputBufferClient.getClientIndex(camId)
    if index is None:
        msg = "client/camId not present in list of current clients: " + camId + " /" + inputBufferClient.TYPE
        # logger.debug(msg)
        print("[DEBUG]", msg)
        return (msg, 400)

    lastRecordedIndex = inputBufferClient.buff[index].bufferImages.lastRecordedIndex
    print("[INFO]lastsample camId " + str(camId) + " lastRecordedIndex " + str(lastRecordedIndex) + " /" + inputBufferClient.TYPE)

    if lastRecordedIndex is None:
        msg = "lastRecordedIndex None: camId: " + camId + " /" + inputBufferClient.TYPE
        # logger.error(msg)
        print("[ERROR]", msg)
        return (msg, 404)
    if lastRecordedIndex < 0:
        msg = "lastRecordedIndex negative: camId: " + camId + " /" + inputBufferClient.TYPE
        # logger.error(msg)
        print("[ERROR]", msg)
        return (msg, 404)


    already_uploaded = inputBufferClient.buff[index].bufferImages.buffer[lastRecordedIndex].uploaded
    filename = inputBufferClient.buff[index].bufferImages.buffer[lastRecordedIndex].filenameWithStamp

    if take_care_of_already_uploaded is True:
        if already_uploaded is True:
            print("[WARNING]lastsample camId " + str(camId) + " lastRecordedIndex " + str(lastRecordedIndex) + ", already uploaded" + " /" + inputBufferClient.TYPE)
            return ("already_uploaded", 204)
            
    dict_out = inputBufferClient.buff[index].bufferImages.buffer[lastRecordedIndex].getAsJsonData()

    if take_care_of_already_uploaded is True:
        inputBufferClient.buff[index].bufferImages.buffer[lastRecordedIndex].uploaded = True

    # OK
    # with open( "todel.png", mode="wb" ) as f:
    #     f.write(base64.b64decode(dict_out["contentBytes"].encode()))
        

    # return (jsonify(dict_out), 200)
    return (dict_out, 200)
