
# python manager.py --url http://127.0.0.1 --port 5000 --ecovisionPath /home/ecorvee/Projects/EcoVision/ecplatform2
# python manager.py --url http://127.0.0.1 --port 5000 --ecovisionPath ./package_ecovision

# in docker but cannot launch my binary ecovision
# python manager.py --url http://web --port 8000 --ecovisionPath ./package_ecovision

# VM
# cd ecoclient
# python manager.py --url http://127.0.0.1 --port 8000 --ecovisionPath ./package_ecovision
# source /home/debian/.bashrc
# python manager.py --url http://127.0.0.1 --port 8000 --ecovisionPath ./package_ecovision
# --debug

# from asyncio import sleep
from asyncio.subprocess import DEVNULL
# from genericpath import isdir
import os
# import sys
#import cv2
import time
import shutil
import subprocess
import threading
import logging
import requests
import json
from datetime import datetime
import argparse



#from crtime import get_crtimes, get_crtimes_in_dir

# echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/absolute_path/' >> ~/.bashrc

# ecovisionlib = '/home/ecorvee/Projects/EcoVision/ecplatform2/build/lib'
# os.environ['LD_LIBRARY_PATH'] = ecovisionlib
# print(os.environ['LD_LIBRARY_PATH'])

#logging.basicConfig(filename='file_watcher.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logging.basicConfig(level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
  
OUTPUT_DIR='output_manager'
  
if os.path.isdir(OUTPUT_DIR) is True:
    shutil.rmtree(OUTPUT_DIR)
  
if os.path.isdir(OUTPUT_DIR) is False:
    os.mkdir(OUTPUT_DIR)
    if os.path.isdir(OUTPUT_DIR) is False:
        print("Failed to create folder: " + OUTPUT_DIR)
        exit(1)
    print("folder successfully created: " + OUTPUT_DIR)

# in setBashRc.py now
# def updateBashRcWithEcovisionLibPath(ecovisionPath: str):
#     if not os.path.isdir(ecovisionPath):
#         print("[ERROR]ecovisionPath does not exist: ", ecovisionPath)
#         exit(1)
#     ecovisionLib = ecovisionPath+'/build/lib'
#     bashRcString = 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:'+ecovisionLib
#     if not os.path.isdir(ecovisionLib):
#         print("[ERROR]updateBashRcWithEcovisionLibPath: this dir does not exist: ", ecovisionLib)
#         exit(1)
#     if 'HOME' not in os.environ:
#         print("[ERROR]updateBashRcWithEcovisionLibPath: environ HOME not present")
#         exit(1)
#     bashrcPath = os.path.join(os.environ['HOME'], ".bashrc")
#     print("[INFO]check bashrc is present: ", bashrcPath)
#     if not os.path.isfile(bashrcPath):
#         print("[WARNING]bashrc not present in home dir ", bashrcPath, "lets create it")
#         with open(bashrcPath, "w") as fbashrc:
#             fbashrc.write(bashRcString)
#             fbashrc.write("\n")
#         if not os.path.isfile(bashrcPath):
#             print("[ERROR]bashrc failed to be created in home dir ", bashrcPath)
#             exit(1)
#     else:
#         ecovisionPathFound = 0

#         targetWords = bashRcString.split(' ')
#         with open(bashrcPath, "r") as fbashrc:
#             for line in fbashrc.readlines():
#                 # print(line)
#                 words = line.split(' ')
#                 # print(" ================= ")
#                 words2 = []
#                 for word in words:
#                     words2.append(word.replace('\n',''))
#                 # print(words2)
#                 localFound = False
#                 if len(words2) == len(targetWords):
#                     localFound = True
#                     for index in range(len(words2)):
#                         if words2[index] != targetWords[index]:
#                             localFound = False
#                 # print(" +++++++++++++++++ ")
#                 # print(targetWords)            
#                 if localFound is True:
#                     ecovisionPathFound += 1
#                 # print(" ----------------- ", localFound, ecovisionPathFound)
#         if ecovisionPathFound == 0:
#             print("[INFO]adding ecovision path lib into bashrc")
#             with open(bashrcPath, "a") as fbashrc:
#                 fbashrc.write(bashRcString)
#                 fbashrc.write("\n")
#         else:
#             print("[INFO]ecovision path lib already present in bashrc")

#         if ecovisionPathFound > 1:
#             print("[WARNING]ecovision path lib was fou nd more than once: ", ecovisionPathFound)

#     # bash = subprocess.run('bash')
#     # bash.execute('source '+os.environ['HOME']+'/.bashrc')
#     # subprocess.call(['source', os.environ['HOME']+'/.bashrc'])
        
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
  
# now = datetime.now()
# date_time = now.strftime("%m-%d-%YT%H:%M:%S.%f")[:-3]
# (convertedStampMicroSec, succConvert) = convertStringTimestampToDatetimeAndMicrosecValue(date_time = date_time)
# if succConvert is False:
#     print(convertedStampMicroSec)
# else:
#     print(now)
#     print(convertedStampMicroSec)
# exit(1)
  
class SessionRunner(threading.Thread):
  
    def __init__(self, url: str, port: int, thread_id: int, nameId:str, ecovisionPath: str, debug: bool):
        threading.Thread.__init__(self)
        self.url = url
        self.port = port
        #self.lock = lock
        self.thread_id = thread_id
        self.nameId = nameId
        self.capture_process = None
        #self.status = False
        #self.output_pipe = None
        self.output_pipe = None
        self.ecovisionPath = ecovisionPath
        self.debug = debug
        logging.info("SessionRunner")
        self._stop_event = threading.Event()
    def stop(self):
        self._stop_event.set()
    def stopped(self):
        return self._stop_event.is_set()
  
    def log(self, msg):
        #date = datetime.now()
        #date = date.strftime('%Y/%m/%d %H:%M:%S')
        #print('{} Thread {:d}: {}'.format(date, self.id, msg))
        #logging.info('{} Thread {:d}: {} pid {}'.format(date, self.id, msg, os.getpid()))
        logging.info('{}'.format(msg))
  
    def run(self):
        self.log('starting')
        
        # OLD
        # cmdline = ["./simul_ecovision", "--url", url+":"+ str(port)+"/image", "--method", "GET", "--output", "simul_ecovision_output.png"]

        # OK
        # cmdline = ["./simul_ecovision", "--url", self.url+":"+ str(args.port), "--camId", self.nameId]

        # OK
        #cmdline = ["./simul_ecovision", "--url", self.url, "--camId", self.nameId]
        # LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/ecorvee/Projects/EcoVision/ecplatform2/build/lib && export LD_LIBRARY_PATH && /home/ecorvee/Projects/EcoVision/ecplatform2/build/bin/platformecpp -subsize 0 -control /home/ecorvee/Projects/EcoVision/ecplatform2/programs/programecpp/platformecpp/control2d.txt  -http_client_to_flask_server -camidname paulo9 -host http://127.0.0.1 -port 5000 -motionwindow 2 -context2dec LOCAL -fantagaugedim 70
        # cmdline = ["LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/ecorvee/Projects/EcoVision/ecplatform2/build/lib",
        #     "&&", "export LD_LIBRARY_PATH",
        #     "&&", "/home/ecorvee/Projects/EcoVision/ecplatform2/build/bin/platformecpp",
        #     "-subsize", "0",
        #     "-control", "/home/ecorvee/Projects/EcoVision/ecplatform2/programs/programecpp/platformecpp/control2d.txt",
        #     "-http_client_to_flask_server", "-camidname", self.nameId,
        #     "-host", self.url, "-port", str(self.port),
        #     "-motionwindow", "2", "-context2dec", "LOCAL", "-fantagaugedim", "70"]

        # echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/absolute_path/' >> ~/.bashrc


        cmdline = [self.ecovisionPath+"/build/bin/platformecpp",
            "-subsize", "0",
            "-control", self.ecovisionPath+"/programs/programecpp/platformecpp/control2d.txt",
            "-create_tcp_server", "-camidname", self.nameId,
            "-host", self.url, "-port", str(self.port),
            "-motionwindow", "2", "-context2dec", "LOCAL", "-fantagaugedim", "70", 
            "-httpPostGet_waitIntervalBeforeRetrying", "10"]


# error: FileNotFoundError: [Errno 2] No such file or directory: './package_ecovision/build/bin/platformecpp'
# but file exist
# see if i can copy ffmpeg and run it, 
# and simply run pwd
        # cmdline = ["pwd"] => /usr/src/app


        self.log("[INFO]cmdline:" + str(cmdline))
        
        # ssend = str(int(1200 / (self.thread_id+1)))
        # intput_video = "Tears_of_Steel_1080p.webm"
        # out_video = os.path.join(OUTPUT_DIR, "outvideo" + self.nameId + ".webm")
        capture_log_stderr = os.path.join(OUTPUT_DIR, "stderr" + self.nameId + ".log")
        capture_log_stdout = os.path.join(OUTPUT_DIR, "stdout" + self.nameId + ".log")
        # #cmdline = ["ffmpeg", "-i", intput_video, "-r", "1", 
        # #           "-ss", "0", "-t", ssend, "-c", "copy", out_video, "-y"]
        # # cmdline = ["ffmpeg", "-i", intput_video, "-r", "1", 
        # #            "-c", "copy", out_video, "-y"]
        # # if self.thread_id == 1:
        # #     cmdline = ["ls", "-l"]  
        # # print(cmdline)
        # cmdline = ["ls", "-l"]
        # logging.info("launch " + cmdline[0] + " ... ")
        # #delta = 3*(self.thread_id + 1)
        # delta = 10*(self.thread_id + 1)
        # #print("sleep: ", delta)
        # time.sleep(delta)
        # # cmdline = [ECOVISION_PROG, '-subsize', '0', '-control', ECOVISION_CTRL2D, 
        # # '-lcsmainfolder', '-directory', '/home/ecorvee/data/LCS-videos/database1/', 
        # # '-lcsvideoindex', '33', '-startat', '1', '-incrementvideoindex', '1',
        # # '-motionwindow', '2', '-context2dec', 'LOCAL', '-fantagaugedim 70']
        # # TODO + datetime
  
        # *************** TODO logrotate ********************

        if self.debug is True:
            with open(capture_log_stderr, "w") as fileStdErr:
                with open(capture_log_stdout, "w") as fileStdOut:
                    self.capture_process = subprocess.Popen(
                            cmdline,
                            stdin=subprocess.PIPE,
                            #stdout=subprocess.PIPE if self.output_pipe is None else self.output_pipe, # ************ keep PIPE here as we do not feed our stdout to another process
                            stdout=fileStdOut,
                            stderr=fileStdErr) # ************** PIPE too ?, see notes above                        
                    self.capture_process.wait()
                    fileStdErr.flush()
                    fileStdOut.flush()
        else:
            self.capture_process = subprocess.Popen(
                cmdline,
                stdin=subprocess.PIPE,
                stdout=DEVNULL,
                stderr=DEVNULL,
                shell=False)
            self.capture_process.wait()
            
        # self.log('sleep '+str(self.intervalSec))
        # time.sleep(self.intervalSec)
        
        self.log('end')
  
# def KillThemAll(FileWatcher):
#     try:
#         if FileWatcher is not None and FileWatcher.isAlive():
#         logging.info("stop file size checker")
#         FileWatcher.stop()
#         FileWatcher.join()
#     except Exception as e:
#         logging.exception("exception during video max file checker thread killing: " + str(e))
#     except:
#         logging.exception("unknown exception during video max file checker thread killing")
  
# def deamonWork():
#     logging.debug('Starting')
#     time.sleep(2)
#     logging.debug('Exiting')
  
if __name__ == "__main__":

    # logging.debug("create deamon")
    # deamon = threading.Thread(name=' ......... Daemon Main Manager .......... ', target=deamonWork)
    # deamon.setDaemon(True)
    # logging.debug("start deamon")
    # deamon.start()
    # # logging.debug("join deamon")
    # # deamon.join()

    parser = argparse.ArgumentParser(description='ecovision threads manager')
    parser.add_argument('--url', metavar='url', required=True,
                        help='the server url that grabs client web cam images')
    parser.add_argument('--port', metavar='port', required=True,
                        help='the corr. server port')
    parser.add_argument('--ecovisionPath', metavar='port', required=True,
                        help='the ecovisionPath') # "/home/ecorvee/Projects/EcoVision/ecplatform2"
    parser.add_argument('--debug', action='store_true', default=False)
    #parser.add_argument('--setBashrc', action='store_true', default=False)
    args = parser.parse_args()

    # if args.setBashrc is True:
    #     print("[INFO]updateBashRcWithEcovisionLibPath")
    #     updateBashRcWithEcovisionLibPath(args.ecovisionPath)
    #     print("[INFO]exit, export /user/.bashrc and restart manager")
    #     exit(0)

    logging.debug("start session running")
    threads = []
    while True:
        try:
            active_client_cam = requests.get(args.url+":"+ str(args.port) +"/active_client_cam")
            json_data_res = json.loads(active_client_cam.content.decode("utf-8"))
            json_data = json_data_res.get("data")
            print("[INFO]checking current active client cam: ", json_data)
            for el in json_data:
                camId = el
                
                dirout = os.path.join(OUTPUT_DIR, camId)
                if os.path.isdir(dirout) is False:
                    os.mkdir(dirout)
                
                DEBUG = False
                if DEBUG is True:
                    #url_get_image = args.url+"/uploaded_image/"+camId+"/"+filename
                    url_get_image_filename = args.url+":"+ str(args.port)+"/last_image_filename/"+camId
                    url_get_image_content = args.url+":"+ str(args.port)+"/last_image_content/"+camId

                    getimage_filename = str(requests.get(url_get_image_filename).content.decode("utf-8"))
                    print("filename:", getimage_filename)
                    getimage_content = requests.get(url_get_image_content)
                    
                    filenameWithStamp = os.path.splitext(getimage_filename)[0]
                    filenameExt = os.path.splitext(getimage_filename)[1]
                    current_image_path = os.path.join(dirout, "currentimage"+filenameExt)
                    print("current_image_path:", current_image_path)
                    
                    # OK, just for debug, saving current image at same location always
                    print(current_image_path)
                    with open(current_image_path, mode="wb") as fout:
                        fout.write(getimage_content.content)
                    
                
                #here
                # # decode filenameWithStamp into int
                # # check if already been treated by the correspoinding thread
                # # so go through all threads, check if inactive or treating the correct camId
                # # ecovision: serveru mode: waiting for input ....
                
            
                FOUND_INDEX = None
                for index in range(len(threads)):
                    nameId = threads[index].nameId
                    if nameId == camId:
                        FOUND_INDEX = index
                    
                if FOUND_INDEX is None:
                    print("[INFO]camId", camId, "CREATE NEW THREAD: index:", len(threads))
                    thread = SessionRunner(thread_id=len(threads), url=args.url, port=args.port, 
                        nameId=camId, ecovisionPath=args.ecovisionPath, debug=args.debug)
                    thread.start()
                    threads.append(thread)
                else:
                    print("[INFO]camId", camId, "still alive at thread buffer index: ", FOUND_INDEX)
                    index = FOUND_INDEX
                    thread_id = threads[index].thread_id
                    isAlive = threads[index].is_alive()
                    if isAlive is False:
                        # TODO restart it
                        print("[INFO]camId", camId, "NO MORE ALIVE : restart it ... TODO if timestamp last image not too old or not already treated")
                        threads.pop(index)
                        thread = SessionRunner(thread_id=index, url=args.url, port=args.port, 
                            nameId=camId, ecovisionPath=args.ecovisionPath, debug=args.debug)
                        thread.start()
                        threads.append(thread)
        except requests.exceptions.RequestException as e:
            print("[WARNING]not reachable")

        time.sleep(10)
    
    logging.debug("end")