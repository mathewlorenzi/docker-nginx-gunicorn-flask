import os
import base64
import logging
from datetime import datetime

STR_UNKNOWN = "UNKNOWN"

class AppImage:
    def __init__(self):
        dt_obj = str(datetime.now())
        dt_obj = dt_obj.replace(" ", "")
        #print(dt_obj)
        self.filenameWithStamp = dt_obj + ".png"
        self.hasData = False
    def copyFrom(self, src):
        self.filenameWithStamp = src.filenameWithStamp
        self.hasData = src.hasData
    def Print(self):
        print(self.filenameWithStamp, self.hasData)
        
class BufferImages:
    def __init__(self, maxLength: int, clientId:str, directory: str):
        self.directory = directory
        self.clientId = clientId
        self.maxLength = maxLength
        self.buffer = []
        self.lastRecordedIndex = -1
        # self.replacedImageFilename = None
        self.oldestRecordedImage = None
        for i in range(self.maxLength):
            appImage = AppImage();
            self.buffer.append(appImage)
    def insert(self, inputImage: AppImage):
        index_nimage = self.lastRecordedIndex + 1# NextImageNotReadyYetForUploadAsNot
        if index_nimage >= self.maxLength:
            index_nimage = 0
        
        # if self.lastRecordedIndex >= 0:
        #    self.replacedImageFilename = self.buffer[self.lastRecordedIndex].filenameWithStamp;
        
        self.buffer[index_nimage].copyFrom(inputImage)
        #now the image is in the buffer, fully saved, so it is available for the client => update index
        self.lastRecordedIndex = index_nimage;

        self.oldestRecordedImage = self.lastRecordedIndex + 1
        if self.oldestRecordedImage >= self.maxLength:
            self.oldestRecordedImage = 0

    def deleteOldest(self):
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
    def __init__(self, clientId: str, mainUploadDir: str) -> None:
        if clientId == "":
            self.clientId = STR_UNKNOWN
        else:
            self.clientId = clientId
        self.mainUploadDir = mainUploadDir
        self.bufferImages = BufferImages(
            maxLength=5, 
            clientId = self.clientId,
            directory=os.path.join(self.mainUploadDir, self.clientId)
        )
        self.outputDir = os.path.join(self.mainUploadDir, self.clientId)
        if os.path.exists(self.outputDir) is False:
            os.mkdir(self.outputDir)
        if os.path.exists(self.outputDir) is False:
            self.initMsg = "could not create: " + self.outputDir
            print("[ERROR]", self.initMsg)
            self.initSucc = False
        self.initMsg = "Client Camera created: "+self.clientId
        self.initSucc = True
    
    def saveNewImage(self, logger: logging.Logger, imageContent: str):
        appImage = AppImage()
        filename = appImage.filenameWithStamp
        logger.debug("ClientCamera::SaveNewImage " + self.bufferImages.clientId + ", filename:" + filename)
        with open(os.path.join(self.bufferImages.directory, filename), 'wb') as f:
            #f.write(base64.decodestring(imagestr.split(',')[1].encode()))
            f.write(base64.b64decode(imageContent.split(',')[1].encode()))
            appImage.hasData = True
            self.bufferImages.insert(appImage)
            logger.info("ClientCamera::SaveNewImage image ready at {} {} oldest to be del {} {}".format( 
                self.bufferImages.lastRecordedIndex, 
                self.bufferImages.buffer[self.bufferImages.lastRecordedIndex].filenameWithStamp, 
                self.bufferImages.oldestRecordedImage, 
                self.bufferImages.buffer[self.bufferImages.oldestRecordedImage].filenameWithStamp))
            #bufferImages.Print()
            (msg, succ) = self.bufferImages.deleteOldest()
            #print(succ, msg)
            return (msg, succ)
            # if succ is True:
            #     logging.info(msg)
            #     #bufferImages.Print()
            # else:
            #     logging.error(msg)
            #     #app.logger.error(msg)
        return ("failed opening image for writing", False)


class BufferClients():

    def __init__(self, database_main_path_all_clients: str) -> None:
        self.buff = []
        self.database_main_path_all_clients = database_main_path_all_clients

    def getClientIndex(self, nameId: str) -> int:
        #print("BufferClients::getClientIndex: nameId:", nameId)
        indexClient = None
        for index in range(len(self.buff)):
            if self.buff[index].clientId == nameId:
                indexClient = index
                break
        return indexClient

    def insertNewClient(self, nameId: str) -> int:
        newClientCam = ClientCamera(clientId=nameId, mainUploadDir=self.database_main_path_all_clients)

        if newClientCam is None:
            print("[ERROR] creating ClientCamera object is None")
            return None

        if newClientCam.initSucc is not True:
            print("[ERROR] creating ClientCamera", newClientCam.initMsg)
            return None

        self.buff.append(newClientCam)
            
        indexClient = self.getClientIndex(nameId=nameId)
        if indexClient is None:
            print("[ERROR]insertClient failed")
            return None

        print("[INFO]insertClient SUCCESS at ", indexClient)
        return indexClient
