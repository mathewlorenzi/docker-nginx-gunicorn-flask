import os
from datetime import datetime

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
    def __init__(self, maxLength: int, directory: str):
        self.directory = directory
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
            pathImage = os.path.join(self.directory, self.buffer[self.oldestRecordedImage].filenameWithStamp)
            if self.buffer[self.oldestRecordedImage].hasData is False:                
                msg = "[INFO]oldest image cannot be deleted as it does not have any data (was not recorded before): " + pathImage
                return (msg, True)    
            if os.path.exists(pathImage) is False:
                msg = "[ERROR]oldest image cannot be deleted as it does not exists on disk: " + pathImage
                return (msg, False)
            if os.path.isfile(pathImage) is False:
                msg = "[ERROR]oldest image cannot be deleted as it is not a file: " + pathImage
                return (msg, False)
            os.remove(pathImage)
            if os.path.exists(pathImage) is True:
                msg = "[ERROR]oldest image was not successfully deleted, it still exist on disk: " + pathImage
                return (msg, False)
            if os.path.isfile(pathImage) is True:
                msg = "[ERROR]oldest image was not successfully deleted, it still is an existing file: " + pathImage
                return (msg, False)
            msg = "[INFO]oldest image was successfully deleted: " + pathImage
            self.buffer[self.oldestRecordedImage].hasData = False
            return (msg, True)
        msg = "[INFO]oldest image not yet recorded: cannot be yet deleted"
        return (msg, True)
        

    def Print(self):
        for i in range(self.maxLength):
            print(i, end=":")
            self.buffer[i].Print()
