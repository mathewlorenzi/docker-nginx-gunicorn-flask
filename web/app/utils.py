from datetime import datetime

# TODO filewatcher ... or in camera.html launch a second sceript to do this job
# TODO or manager.py to send a clean endpoint to do filewatcher job.
# TODO or look for flask refreshing option

# get username from form
# https://github.com/fossasia/Flask_Simple_Form/blob/master/nagalakshmiv2004/Form.py


def debugPathForDockerIssue():

    print(" .... docker debug: curr dir: ", os.getcwd())

    files = [f for f in os.listdir('.') if os.path.isdir(f)]
    for f in files:
        print(" .... docker debug: ", f)
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        print(" .... docker debug: ", f)

    import os.path as P
    for topdir, subdirs, files in os.walk("./"):
      print("    " * topdir.count(P.sep), P.basename(topdir))
      for f in sorted(files):
        print("    " * (topdir.count(P.sep) + 1), f)

    print(" .... docker debug:", os.path.isdir("/usr/src/app/database_clients_camera"))

    # ENV PYTHONPATH "/usr/src/app"

    # print(".... docker python path:", os.environ.get('PYTHONPATH'))
    # print(".... docker sys path:", sys.path)


import os, sys
def printRootStructure(dirname,indent=0):
    for i in range(indent):
        print("   ", end=",")
    print(os.path.basename(dirname))
    if os.path.basename(dirname) != 'venv' and os.path.basename(dirname) != '.git':
        if os.path.isdir(dirname):
            for files in os.listdir(dirname):
                printRootStructure(os.path.join(dirname,files),indent+1) # changed


# import shutil
# import cv2
# import time
# from datetime import datetime
# def populate_fake_images(OUTPUT_PATH: str, sampleImagePath: str):
#     camIds = ["peter", "paul", "jack", "UNKNOWN"]
#     if os.path.exists(OUTPUT_PATH):
#         shutil.rmtree(OUTPUT_PATH)
#     os.mkdir(OUTPUT_PATH)
#     for dir in camIds:
#         os.mkdir(os.path.join(OUTPUT_PATH, dir))
#     img = cv2.imread(sampleImagePath)
#     for dir in camIds:
#         for nb in range(10):
#             now = datetime.now()
#             date_time = now.strftime("%m-%d-%YT%H:%M:%S.%f")[:-3]
#             print("date_time:", dir, date_time)
#             cv2.imwrite(os.path.join(OUTPUT_PATH, dir, date_time+".jpg"), img)
#             time.sleep(0.5)
#     return camIds
  
# populate_fake_images(OUTPUT_PATH=OUTPUT_PATH, sampleImagePath="sample.png")
# exit(1)


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