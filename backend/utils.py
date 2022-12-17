import os
import psutil
import base64
from datetime import datetime
import logging

IMGEXT='jpg'

from buffer_images import BufferClients

def convertDatetimeToString(input: datetime) -> str:
    return input.strftime("%m-%d-%YT%H:%M:%S.%f")[:-3]

# format input: "%m-%d-%YT%H:%M:%S.%f" WARNING there is T to separate date from time
# eg: now = datetime.now(); date_time = now.strftime("%m-%d-%YT%H:%M:%S.%f")[:-3]
def convertStringTimestampToDatetimeAndMicrosecValue(date_time: str, debug: bool=False):
    if debug is True:
        print("convert: input: date_time:", date_time)
    a1 = date_time.split("T")
    if len(a1) != 2:
        return ("[ERROR]convert string stamp: char T not found beween date and time", False)
    dateStr=a1[0]
    timeStr=a1[1]
    if debug is True:
        print("convert stamp: ", dateStr, timeStr)
    
    a2 = dateStr.split("-")
    if len(a2) != 3:
        return ("[ERROR]convert string stamp: char - not found to split date", False)
    yearStr=a2[2]
    monthStr=a2[0]
    dayStr=a2[1]
    if debug is True:
        print("convert stamp: d m y:", dayStr, monthStr, yearStr)
    
    a2 = timeStr.split(":")
    if len(a2) != 3:
        return ("[ERROR]convert string stamp: char - not found to split time", False)
    hourStr=a2[0]
    minuteStr=a2[1]
    secMilStr=a2[2]
    if debug is True:
        print("convert stamp: h m sm", hourStr, minuteStr, secMilStr)

    a2=secMilStr.split(".")
    if len(a2) != 2:
        return ("[ERROR]convert string stamp: char - not found to split sec to millisec", False)
    secStr=a2[0]
    milliSecStr=a2[1]
    if debug is True:
        print("convert stamp: s m", secStr, milliSecStr)
        print("convert stamp: final: ", dayStr, monthStr, yearStr, hourStr, minuteStr, secStr, milliSecStr)
    convertedStampMicroSec = datetime(year=int(yearStr), month=int(monthStr), day=int(dayStr), hour=int(hourStr), minute=int(minuteStr), second=int(secStr), microsecond=int(milliSecStr)*1000)
    return (convertedStampMicroSec, True)
  
def test_convertStringTimestampToDatetimeAndMicrosecValue():
    now = datetime.now()
    date_time = now.strftime("%m-%d-%YT%H:%M:%S.%f")[:-3]
    (convertedStampMicroSec, succConvert) = convertStringTimestampToDatetimeAndMicrosecValue(date_time = date_time)
    if succConvert is False:
        print(convertedStampMicroSec)
    else:
        print(now)
        print(convertedStampMicroSec)
    # exit(1)

#def get_encoded_img(image_path):
    #img = Image.open(image_path, mode='r')
    #img_byte_arr = io.BytesIO()
    #img.save(img_byte_arr, format='PNG')
    #my_encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
    #return my_encoded_img

def get_encoded_img(image_path):
    with open(image_path, mode="rb" ) as f:
        img_byte_arr = f.read()
        return base64.encodebytes(img_byte_arr).decode('ascii')

def get_cpu_ram_disk():
    per_cpu = psutil.cpu_percent(percpu=True)
    mean_cpu = 0.0
    counter=0
    for idx, usage in enumerate(per_cpu):
        print(f"CORE_{idx+1}: {usage}%")
        mean_cpu += float(usage)
        counter+=1
    if counter > 0:
        mean_cpu /= float(counter)
    cpu=round(mean_cpu)

    mem_usage = psutil.virtual_memory().percent
    print("ram", mem_usage)
    ram=round(mem_usage)

    disk_usage = psutil.disk_usage("./").percent
    print("disk_usage", disk_usage)
    disk=round(disk_usage)

#def get_encoded_img(image_path):
    #img = Image.open(image_path, mode='r')
    #img_byte_arr = io.BytesIO()
    #img.save(img_byte_arr, format='PNG')
    #my_encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
    #return my_encoded_img

def get_encoded_img(image_path):
    with open(image_path, mode="rb" ) as f:
        img_byte_arr = f.read()
        return base64.encodebytes(img_byte_arr).decode('ascii')


def record_image_or_result(inputBufferClient: BufferClients, imageContentStr: str, camId: str, logger):
    nameId = camId # data["nameId"]
    if isinstance(imageContentStr, str) is False or isinstance(nameId, str) is False:
        logger.error("/image: nameId is not a string:" + str(nameId))
        return ("KO: nameId is not a string", nameId, 400)
    else:
        # look if existing active camera
        indexClient = inputBufferClient.getClientIndex(nameId=nameId)
        if indexClient is None:
            logger.info("/image: nameId:" + nameId + " new client")
            (_msg, indexClient) = inputBufferClient.insertNewClient(nameId=nameId)
            if indexClient is None:
                errMsg = "/image: nameId:" + nameId + " failed inserting new client " + _msg
                logger.error(errMsg)
                return (errMsg, nameId, 400)

        # check really necessary ?
        indexClient = inputBufferClient.getClientIndex(nameId=nameId)
        if indexClient is None:
            logger.error("/image: nameId:" + nameId + " failed finding client")
            return ("KO: Failed finding client or inserting new client " + nameId, nameId, 400)
        
        logger.debug("/image: nameId:" + nameId + " indexClient: " + str(indexClient))

        # while(inputBufferClient.buff[indexClient].lockOnUpload is True){
        #     logger.info("/image: lock active, wait a bit, for camId" + nameId)
        #     time.sleep(1)
        # }
        # lockOnUpload = False
        # imageToBeUploaded = AppImage()

        (msg, succ) = inputBufferClient.buff[indexClient].insertNewImage(logger=logger, imageContent=imageContentStr)
        if succ is False:
            logger.error(msg)
            return ("KO: failed saving new image", nameId, 400)
        else:
            logger.info(msg)

            # camId = nameId
            # logger.debug("/result_image2 endpoint")
            # v1
            # if camId in ecovisionResults.trackResultsImage:
            #     return (ecovisionResults.trackResultsImage[camId], nameId, 200)
            # else:
            #     return ("ok but image result from ecovision not ready yet for " + camId, nameId, 202)
            # v2 return a blank image if not ready
            # indexECO = bufferEcovisionResults.getClientIndex(nameId=nameId)
            # if indexECO is None:
            #     logger.error("/image: nameId:" + nameId + " failed finding client in ecovision results")
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

    logger.debug("lastsample camId " + str(camId) + "/" + inputBufferClient.TYPE)
    if camId is None:
        msg = "camId in None in url" + " /" + inputBufferClient.TYPE
        logger.error(msg)
        return (msg, 405)    
    if camId == "":
        msg = "nameId is empty in url" + " /" + inputBufferClient.TYPE
        logger.error(msg)
        return (msg, 405)
    
    index = inputBufferClient.getClientIndex(camId)
    if index is None:
        msg = "client/camId not present in list of current clients: " + camId + " /" + inputBufferClient.TYPE
        logger.debug(msg)
        return (msg, 400)

    lastRecordedIndex = inputBufferClient.buff[index].bufferImages.lastRecordedIndex
    logger.info("lastsample camId " + str(camId) + " lastRecordedIndex " + str(lastRecordedIndex) + " /" + inputBufferClient.TYPE)

    if lastRecordedIndex is None:
        msg = "lastRecordedIndex None: camId: " + camId + " /" + inputBufferClient.TYPE
        logger.error(msg)
        return (msg, 404)
    if lastRecordedIndex < 0:
        msg = "lastRecordedIndex negative: camId: " + camId + " /" + inputBufferClient.TYPE
        logger.error(msg)
        return (msg, 404)


    already_uploaded = inputBufferClient.buff[index].bufferImages.buffer[lastRecordedIndex].uploaded
    filename = inputBufferClient.buff[index].bufferImages.buffer[lastRecordedIndex].filenameWithStamp

    if take_care_of_already_uploaded is True:
        if already_uploaded is True:
            logger.warning("lastsample camId " + str(camId) + " lastRecordedIndex " + str(lastRecordedIndex) + ", already uploaded" + " /" + inputBufferClient.TYPE)
            return ("already_uploaded", 204)
            
    dict_out = inputBufferClient.buff[index].bufferImages.buffer[lastRecordedIndex].getAsJsonData()

    if take_care_of_already_uploaded is True:
        inputBufferClient.buff[index].bufferImages.buffer[lastRecordedIndex].uploaded = True

    # OK
    # with open( "todel.png", mode="wb" ) as f:
    #     f.write(base64.b64decode(dict_out["contentBytes"].encode()))
        

    # return (jsonify(dict_out), 200)
    return (dict_out, 200)
