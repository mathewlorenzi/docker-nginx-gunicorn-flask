
# python manager.py --host http://127.0.0.1 --port 5000 --ecovisionPath /home/ecorvee/Projects/EcoVision/ecplatform2
# python manager.py --host http://127.0.0.1 --port 5000 --ecovisionPath ./package_ecovision

# in docker but cannot launch my binary ecovision
# python manager.py --host http://web --port 8000 --ecovisionPath ./package_ecovision

# VM
# cd ecoclient
# python manager.py --host http://127.0.0.1 --port 8000 --ecovisionPath ./package_ecovision
# source /home/debian/.bashrc
# python manager.py --host http://127.0.0.1 --port 8000 --ecovisionPath ./package_ecovision
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

class EcoVisionRunner(threading.Thread):
  
    def __init__(self, port: int, thread_id: int, nameId:str, ecovisionPath: str, debug: bool):
        threading.Thread.__init__(self)
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
        logging.info("EcoVisionRunner")
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
        # OK
        # cmdline = ["./simul_ecovision", "--host", self.host+":"+ str(args.port), "--camId", self.nameId]
        # echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/absolute_path/' >> ~/.bashrc
        cmdline = [self.ecovisionPath+"/build/bin/platformecpp",
            "-subsize", "0",
            "-control", self.ecovisionPath+"/programs/programecpp/platformecpp/control2d.txt",
            "-create_tcp_server", "-camidname", self.nameId,
            "-port", str(self.port),
            "-motionwindow", "2", "-context2dec", "LOCAL",
            ]

        self.log("[INFO]cmdline:" + str(cmdline))
        
        capture_log_stderr = os.path.join(OUTPUT_DIR, "stderr" + self.nameId + ".log")
        capture_log_stdout = os.path.join(OUTPUT_DIR, "stdout" + self.nameId + ".log")
  
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
    

class ManagerEcovisionS(threading.Thread):
    def __init__(self, host: str, port: int, ecovisionPath: str, debug: bool=False):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.ecovisionPath = ecovisionPath
        self.debug = debug
        logging.info("ManagerEcovisionS")
        self._stop_event = threading.Event()
    def stop(self):
        self._stop_event.set()
    def stopped(self):
        return self._stop_event.is_set()  
    def run(self):
        print('starting ManagerEcovisionS')
        threads = []
        while True:
            try:
                url = "http://"+self.host+":"+ str(self.port) +"/active_client_cam"
                if self.debug is True:
                    print("[DEBUG]asking for active clients on ", url)
                active_client_cam = requests.get(url)
                if self.debug is True:
                    print("[DEBUG]active_client_cam ", active_client_cam)
                json_data_res = json.loads(active_client_cam.content.decode("utf-8"))
                if self.debug is True:
                    print("[DEBUG]json_data_res ", json_data_res)
                
                json_data = json_data_res.get("data")
                print("[INFO]checking current active client cam: ", json_data)
                for el in json_data:
                    camId = el
                    
                    dirout = os.path.join(OUTPUT_DIR, camId)
                    if os.path.isdir(dirout) is False:
                        os.mkdir(dirout)
                    
                    DEBUG = False
                    if DEBUG is True:
                        #url_get_image = self.url+"/uploaded_image/"+camId+"/"+filename
                        url_get_image_filename = self.host+":"+ str(self.port)+"/last_image_filename/"+camId
                        url_get_image_content = self.host+":"+ str(self.port)+"/last_image_content/"+camId

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
                        thread = EcoVisionRunner(thread_id=len(threads), host=self.host, port=self.port, 
                            nameId=camId, ecovisionPath=self.ecovisionPath, debug=self.debug)
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
                            thread = EcoVisionRunner(thread_id=index, host=self.host, port=self.port, 
                                nameId=camId, ecovisionPath=self.ecovisionPath, debug=self.debug)
                            thread.start()
                            threads.append(thread)
            except requests.exceptions.RequestException as e:
                print("[WARNING]not reachable")

            time.sleep(10)
        
        print("end managing ecovisions")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='ecovision threads manager')
    parser.add_argument('--host', metavar='host', required=True,
                        help='the server host that grabs client web cam images')
    parser.add_argument('--port', metavar='port', required=True,
                        help='the corr. server port')
    parser.add_argument('--ecovisionPath', metavar='ecovisionPath', required=True,
                        help='the ecovisionPath') # "/home/ecorvee/Projects/EcoVision/ecplatform2"
    parser.add_argument('--debug', action='store_true', default=False)
    args = parser.parse_args()

    manager = ManagerEcovisionS(host=args.host, port=args.port, ecovisionPath=args.ecovisionPath, debug=args.debug)
