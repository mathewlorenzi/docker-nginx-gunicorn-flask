import os
import base64
from base64 import b64encode
import logging
from datetime import datetime
from utils import convertDatetimeToString, convertStringTimestampToDatetimeAndMicrosecValue

STR_UNKNOWN = "UNKNOWN"

NOSAVE = "NOSAVE"
SAVE_WITH_TIMESTAMPS = "SAVE_WITH_TIMESTAMPS"
SAVE_WITH_UNIQUE_FILENAME = "SAVE_WITH_UNIQUE_FILENAME"
LIST_MODE_SAVE_TO_DISK = [NOSAVE, SAVE_WITH_TIMESTAMPS, SAVE_WITH_UNIQUE_FILENAME]

def load_sample(imagePath):
    with open(imagePath, mode="rb") as fsample:
        img_data = fsample.read()
        encoded = b64encode(img_data)
        decoded_img = encoded.decode('utf-8')
        uri_result = f"data:image/jpeg;base64,{decoded_img}"
        #mime = "image/jpeg"
        #uri_result = "data:%s;base64,%s" % (mime, encoded)
        return uri_result

class AppImage:
    def __init__(self):
        now = datetime.now()
        self.dateTime = now
        date_time = convertDatetimeToString(self.dateTime)
        self.filenameWithStamp = date_time + ".png"
        self.hasData = False    # data been saved to disk
        self.uploaded = False
        self.contentBytes = []
        self.contentBytes4Json = []
        (self.convertedStampMicroSec, succConvert) = convertStringTimestampToDatetimeAndMicrosecValue(date_time = date_time)
        if succConvert is False:
            self.initMsg = "[ERROR]AppImage: convertedStampMicroSec: {}".format(self.convertedStampMicroSec)
            self.success = False
        else:
            self.initMsg = "[INFO]AppImage: ", now, "convertedStampMicroSec: {}".format(self.convertedStampMicroSec)
            self.success = True
    def copyFrom(self, src):
        self.dateTime = src.dateTime
        self.filenameWithStamp = src.filenameWithStamp
        self.hasData = src.hasData
        self.success = src.success
        self.convertedStampMicroSec = src.convertedStampMicroSec
        self.uploaded = src.uploaded
        self.contentBytes = src.contentBytes
        self.contentBytes4Json = src.contentBytes4Json
    def Print(self):
        print(self.dateTime, self.convertedStampMicroSec, self.filenameWithStamp, "hasData: ", self.hasData, "uploaded", self.uploaded, "SUCCESS: ", self.success)
    def getAsJsonData(self):
        dict_out = {
            "dateTime": str(self.dateTime),
            "filenameWithStamp": self.filenameWithStamp,
            "hasData": str(self.hasData), # fine to let it bool but C++ json parser needs string
            #"convertedStampMicroSec": self.convertedStampMicroSec,
            "uploaded": str(self.uploaded),
            "contentBytes": self.contentBytes4Json
        }
        return dict_out

class BufferImages:
    def __init__(self, maxLength: int, clientId:str, directory: str=None):
        self.directory = directory
        self.clientId = clientId
        self.maxLength = maxLength
        self.buffer = []
        self.lastRecordedIndex = -1
        # self.replacedImageFilename = None
        self.oldestRecordedImage = None
        self.success = False
        for i in range(self.maxLength):
            appImage = AppImage();
            if appImage.success is False:
                self.success = False
                self.initMsg = "[ERROR]BufferImages init failed: " + appImage.initMsg
                return
            self.buffer.append(appImage)
        self.success = True
        self.initMsg = "[INFO]BufferImages init OK"
    def insert(self, inputImage: AppImage):
        index_nimage = self.lastRecordedIndex + 1# NextImageNotReadyYetForUploadAsNot
        if index_nimage >= self.maxLength:
            index_nimage = 0
            
        self.buffer[index_nimage].copyFrom(inputImage)
        # now the image is in the buffer, fully filled in buffer, so it is available for the client => update index
        self.lastRecordedIndex = index_nimage;

        self.oldestRecordedImage = self.lastRecordedIndex + 1
        if self.oldestRecordedImage >= self.maxLength:
            self.oldestRecordedImage = 0

    def deleteOldest(self):
        if self.directory is None:
            msg = "[WARNING]oldest image cannot be deleted as no directory out provided: check MODE SAVE TO DISK for camId: " + self.clientId
            return (msg, True)
        if self.oldestRecordedImage is not None:
            filename = self.buffer[self.oldestRecordedImage].filenameWithStamp
            pathImage = os.path.join(self.directory, filename)
            if self.buffer[self.oldestRecordedImage].hasData is False:                
                msg = "oldest image cannot be deleted as it does not have any data (was not recorded before): " + self.clientId + ", " + filename
                return (msg, True)    
            if os.path.exists(pathImage) is False:
                msg = "oldest image cannot be deleted as it does not exists on disk: " + self.clientId + ", " + filename
                return (msg, False)
            if os.path.isfile(pathImage) is False:
                msg = "oldest image cannot be deleted as it is not a file: " + self.clientId + ", " + filename
                return (msg, False)
            os.remove(pathImage)
            if os.path.exists(pathImage) is True:
                msg = "oldest image was not successfully deleted, it still exist on disk: " + self.clientId + ", " + filename
                return (msg, False)
            if os.path.isfile(pathImage) is True:
                msg = "oldest image was not successfully deleted, it still is an existing file: " + self.clientId + ", " + filename
                return (msg, False)
            msg = "oldest image was successfully deleted: " + self.clientId + ", " + filename
            self.buffer[self.oldestRecordedImage].hasData = False
            return (msg, True)
        msg = "oldest image not yet recorded: cannot be yet deleted, " + self.clientId
        return (msg, True)
        

    def Print(self):
        for i in range(self.maxLength):
            print(i, end=":")
            self.buffer[i].Print()

class ClientCamera():
    """
    buffer of N images: bufferImages
    clientId = camId
    directory where are saved the images if MODE_SAVE_TO_DISK is not set to no save
    """
    def __init__(self, clientId: str, MODE_SAVE_TO_DISK: str, mainUploadDir: str=None) -> None:

        self.MODE_SAVE_TO_DISK = MODE_SAVE_TO_DISK 
        if self.MODE_SAVE_TO_DISK not in LIST_MODE_SAVE_TO_DISK:
            self.initMsg = "ClientCamera: MODE_SAVE_TO_DISK " + MODE_SAVE_TO_DISK + " not in allowed list " + str(LIST_MODE_SAVE_TO_DISK)
            print("[ERROR]", self.initMsg)
            self.initSucc = False
            return 

        self.clientId = clientId
        if clientId == "":
            self.clientId = STR_UNKNOWN

        if self.MODE_SAVE_TO_DISK == NOSAVE:
            self.mainUploadDir = None
            self.outputDir = None
        else:
            self.mainUploadDir = mainUploadDir
            self.outputDir = os.path.join(self.mainUploadDir, self.clientId)
            if os.path.exists(self.outputDir) is False:
                os.mkdir(self.outputDir)
            if os.path.exists(self.outputDir) is False:
                self.initMsg = "could not create: " + self.outputDir
                #print("[ERROR]", self.initMsg)
                self.initSucc = False
                return
        
        self.bufferImages = BufferImages(
            maxLength=5, 
            clientId = self.clientId,
            directory = self.outputDir
        )
        if self.bufferImages is False:
            self.initMsg = "ClientCamera: buffer images creation failed: "
            self.initSucc = False
            return

        if self.bufferImages.success is False:
            self.initSucc = False
            self.initMsg = "[ERROR]ClientCamera: buffer images creation failed: " + self.bufferImages.initMsg
            return

        self.initMsg = "Client Camera created: "+self.clientId
        self.initSucc = True
    
    def insertNewImage(self, logger: logging.Logger, imageContent: str):
        appImage = AppImage()
        if appImage.success is False:
            return ("[ERROR]ClientCamera::insertNewImage: failed creating new image", False)
        filename = appImage.filenameWithStamp
        logger.debug("ClientCamera::insertNewImage " + self.bufferImages.clientId + ", filename: " + filename)

        # OK but KO with simul_clients => f.write(base64.b64decode(imageContent.split(',')[1].encode()))


        
        if len(imageContent.split(',')) > 1:
            content = imageContent.split(',')[1]
        elif len(imageContent.split(',')) == 1:
            content = imageContent
        else:
            return ("[ERROR]ClientCamera::insertNewImage: image content seems empty", False)

        # type(content)) # str
        appImage.contentBytes = base64.b64decode(content.encode())
        # type(appImage.contentBytes)) # bytes
        appImage.contentBytes4Json = content
        # type(appImage.contentBytes4Json)) # bytes
        appImage.hasData = True

        self.bufferImages.insert(appImage)
                
        # logger.info(msg)
        
        if self.MODE_SAVE_TO_DISK == NOSAVE:
            msg = "ClientCamera::insertNewImage image ready at {}: {} ".format( 
                self.bufferImages.lastRecordedIndex, 
                self.bufferImages.buffer[self.bufferImages.lastRecordedIndex].filenameWithStamp)
            return (msg, True)
        else:
            if self.MODE_SAVE_TO_DISK == SAVE_WITH_TIMESTAMPS:
                msg = "ClientCamera::insertNewImage image ready at {} {} oldest to be del {} {}".format( 
                    self.bufferImages.lastRecordedIndex, 
                    self.bufferImages.buffer[self.bufferImages.lastRecordedIndex].filenameWithStamp, 
                    self.bufferImages.oldestRecordedImage, 
                    self.bufferImages.buffer[self.bufferImages.oldestRecordedImage].filenameWithStamp)
                pathout = os.path.join(self.bufferImages.directory, filename)
            elif self.MODE_SAVE_TO_DISK == SAVE_WITH_UNIQUE_FILENAME:
                msg = "ClientCamera::insertNewImage image ready at {}: {} ".format( 
                    self.bufferImages.lastRecordedIndex, 
                    self.bufferImages.buffer[self.bufferImages.lastRecordedIndex].filenameWithStamp)
                pathout = os.path.join(self.bufferImages.directory, "image.png")
            with open(pathout, 'wb') as f:
                f.write(appImage.contentBytes)
            #bufferImages.Print()

            if self.MODE_SAVE_TO_DISK == SAVE_WITH_TIMESTAMPS:
                (_msg, succ) = self.bufferImages.deleteOldest()
                return (msg+_msg, succ)
            
            return (msg, True)

class BufferClients():

    def __init__(self, MODE_SAVE_TO_DISK: str, database_main_path_all_clients: str=None, debugapp: bool=False) -> None:
        self.MODE_SAVE_TO_DISK = MODE_SAVE_TO_DISK 
        if self.MODE_SAVE_TO_DISK not in LIST_MODE_SAVE_TO_DISK:
            self.initMsg = "BufferClients: MODE_SAVE_TO_DISK " + MODE_SAVE_TO_DISK + " not in allowed list " + str(LIST_MODE_SAVE_TO_DISK)
            print("[ERROR]", self.initMsg)
            self.initSucc = False 

        self.buff = []
        self.database_main_path_all_clients = database_main_path_all_clients
        self.debugapp = debugapp
        self.initMsg = "OK"
        self.initSucc = True

    def getClientIndex(self, nameId: str) -> int:
        #print("BufferClients::getClientIndex: nameId:", nameId)
        indexClient = None
        if self.debugapp is True:
            print(" ... debugapp: BufferClients::getClientIndex ", nameId, "in", len(self.buff), "buffer")
        for index in range(len(self.buff)):
            if self.debugapp is True:
                print(" ... debugapp: BufferClients::getClientIndex ", nameId, "vs", self.buff[index].clientId)
            if self.buff[index].clientId == nameId:
                indexClient = index
                break
        return indexClient

    def insertNewClient(self, nameId: str) -> int:

        newClientCam = ClientCamera(clientId=nameId, MODE_SAVE_TO_DISK=self.MODE_SAVE_TO_DISK, mainUploadDir=self.database_main_path_all_clients)

        if newClientCam is None:
            return ("[ERROR] creating ClientCamera object is None", None)

        if newClientCam.initSucc is False:
            return ("[ERROR] creating ClientCamera" + newClientCam.initMsg, None)

        self.buff.append(newClientCam)
            
        indexClient = self.getClientIndex(nameId=nameId)
        if indexClient is None:
            return ("[ERROR]insertClient failed getClientIndex failed for nameId: " + nameId, None)

        return ("[INFO]insertClient SUCCESS at " + str(indexClient), indexClient)

    def deleteOneTooOldConnectedClient(self, maxDeltaAge: int, debug: bool=False) -> bool:
        now = datetime.now()
        index = 0
        for client in self.buff:
            index += 1
            mostRecentInd = client.bufferImages.lastRecordedIndex
            if mostRecentInd>=0:
                mostRecentImg = client.bufferImages.buffer[client.bufferImages.lastRecordedIndex]
                # print("....", mostRecentImg.convertedStampMicroSec)
                delta = now.timestamp() - mostRecentImg.convertedStampMicroSec.timestamp()
                outdated = False
                if delta >  maxDeltaAge:
                    outdated = True
                # print("[INFO]BufferClients: too old connected client deleteing it from active clients: ", client.clientId, mostRecentInd, delta, outdated)
                if outdated is True:
                    print("[INFO]BufferClients: too old connected client deleteing it from active clients: ", client.clientId, mostRecentInd, delta, outdated)
                    self.buff.pop(index - 1)
                    return True

        '''if debug is True:
            for client in self.buff:
                print()
                for im in client.bufferImages.buffer:
                    outdated = False
                    if now.timestamp() - im.convertedStampMicroSec.timestamp() >  5:
                        outdated = True
                    print(client.clientId, client.bufferImages.lastRecordedIndex, im.convertedStampMicroSec, now-im.convertedStampMicroSec, outdated)
        '''
        return False

    def getListClients(self):
        listClients = []
        for client in self.buff:
            listClients.append(client.clientId)
        return listClients