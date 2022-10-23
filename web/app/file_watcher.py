from asyncio import sleep
import os
import sys
import time
import time
import threading
import logging
from datetime import datetime
#from crtime import get_crtimes, get_crtimes_in_dir

#logging.basicConfig(filename='file_watcher.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logging.basicConfig(level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

class SessionRunner(threading.Thread):

    def __init__(self, thread_id, mainDir:str, maxNbFiles:int, maxFileAgeMinutes: int, intervalSec=10):
        threading.Thread.__init__(self)
        #self.lock = lock
        self.id = thread_id
        self.mainDir = mainDir
        self.maxNbFiles = maxNbFiles
        self.maxFileAgeMinutes = maxFileAgeMinutes
        self.intervalSec = intervalSec
        #self.status = False
        logging.info("FileWatcher")
        self._stop_event = threading.Event()
    def stop(self):
        self._stop_event.set()
    def stopped(self):
        return self._stop_event.is_set()

    def log(self, msg):
        date = datetime.now()
        date = date.strftime('%Y/%m/%d %H:%M:%S')
        print('{} Thread {:d}: {}'.format(date, self.id, msg))
        logging.info('{} Thread {:d}: {} pid {}'.format(date, self.id, msg, os.getpid()))

    def run(self):
        self.log('starting')
        go_on = True
        while go_on:
            self.log('in loop')
            for dir in os.listdir(self.mainDir):
                print(dir)
                #print(get_crtimes_in_dir(dir))
                localDir = os.path.join(self.mainDir, dir)
                
                files = os.listdir(localDir)
                if len(files) > self.maxNbFiles:
                    self.log("TODO too many files in ".format(localDir))
                    print("TODO")
                    # sort files by creation date
                    # keep only the first maxNbFiles ones

                files = os.listdir(localDir)
                nowTime = ms = time.time()
                for fileEl in files:
                    localFile = os.path.join(localDir, fileEl)
                    creationTime = os.stat(localFile).st_ctime
                    delta = nowTime-creationTime
                    delta_min = delta/60
                    delta_hour = delta_min/60
                    print(creationTime, delta, delta_min, delta_hour)
                    if delta_min > self.maxFileAgeMinutes:
                        try:
                            self.log("removing {}".format(localFile))
                            os.remove(localFile)
                        except FileNotFoundError as e:
                            logging(e)
                            self.log(e)
                            print(e)
                if len(files) == 0:
                    try:
                        self.log("removing dir {}".format(localDir))
                        os.rmdir(localDir)
                    except OSError as x:
                        print("Error occured: %s : %s" % (localDir, x.strerror))
                        self.log("Error occured: %s : %s" % (localDir, x.strerror))

                
            # file_to_process = None
            # self.lock.acquire()
            # if len(self.files) > 0:
            #     self.log('{:d} files remaining ({:.1f} %)'.format(len(self.files),
            #                                                       float(len(self.files))/float(self.nb_files)*100.))
            #     file_to_process = self.files.pop()
            # else:
            #     go_on = False
            # self.lock.release()

            # if file_to_process is not None:
            #     prod = MstarProduction(file_to_process)
            #     if not (self.keep_existing_files and prod.is_mocem_image_computed()):
            #         self.log('processing begins file {}'.format(file_to_process))
            #         prod.run_mocem(False)
            #         self.log('processing ended file {}'.format(file_to_process))
            #     else:
            #         self.log('skipping existing file {}'.format(file_to_process))
            #         prod.run_mocem(True)
            #     self.lock.acquire()
            #     prod.compare_mstar_mocem(self.id+1)
            #     self.lock.release()
            self.log('sleep '+str(self.intervalSec))
            time.sleep(self.intervalSec)

        self.log('end')

# not working
# check if a file exceed a limit, stop and return a status. The run() method will be started and it will run in the background until the application exits.
class FileWatcher(threading.Thread):
    def __init__(self, mainDir:str, maxNbFiles:int, maxFileAgeMinutes: int, intervalSec=10):
        super(FileWatcher, self).__init__()
        self.mainDir = mainDir
        self.maxNbFiles = maxNbFiles
        self.maxFileAgeMinutes = maxFileAgeMinutes
        self.intervalSec = intervalSec
        self.status = False
        logging.info("FileWatcher")
        self._stop_event = threading.Event()
    def stop(self):
        self._stop_event.set()
    def stopped(self):
        return self._stop_event.is_set()                       
    def run(self): # runs forever
        while not self.stopped():
            try:
                for dir in os.listdir(self.mainDir):
                    print(dir)
                # logging.info('Check for {} bigger than {} Bytes'.format(self.filename, self.fileSizeLimitBytes))
                # if os.path.isfile(self.filename):
                #     currentFileSize = os.stat(self.filename).st_size
                #     if currentFileSize > self.fileSizeLimitBytes:
                #         self.status = True
                #         logging.info('FileWatcher detect that {} exceed the limit'.format(self.filename))
                else:
                    logging.warning("FileWatcher: doesn't exist")
            except OSError as e:  ## if failed, report it back to the user ##
                logging.error ("Error: %s - %s." % (e.strerror))   
            self._stop_event.wait(self.intervalSec) # check every N sec
    def GetStatus(self):
        return self.status


def KillThemAll(FileWatcher):
    try:
        if FileWatcher is not None and FileWatcher.isAlive():
            logging.info("stop file size checker")
            FileWatcher.stop()
            FileWatcher.join()
    except Exception as e:
        logging.exception("exception during video max file checker thread killing: " + str(e))
    except:
        logging.exception("unknown exception during video max file checker thread killing")
    
    # # ************ I DID THIS, I use RunTimeError of join:
    # outtime = 0.1
    # if videoCap is not None:
    #     logger.info(" ... stream packer stop, isStopped {} isAlive {}".format(videoCap.isStopped(), videoCap.isAlive()))
    #     videoCap.stop()
    #     while videoCap.isAlive() is True:
    #         try:
    #             logger.info(" ... stream packer join, isStopped {} isAlive {}".format(videoCap.isStopped(), videoCap.isAlive()))
    #             videoCap.join(outtime)
    #         except RuntimeError:
    #             logger.exception(" ... stream packer join, RuntimeError")
    #     logger.info(" ... stream packer stopped and joined, isStopped {} isAlive {}".format(videoCap.isStopped(), videoCap.isAlive()))
        
if __name__ == "__main__":
    logging.debug("start session running")
    threads = []
    #lock = RLock()
    for i in range(1):
        thread = SessionRunner(thread_id=i, mainDir="database_clients_camera", maxNbFiles=10, maxFileAgeMinutes=60, intervalSec=10)
        threads.append(thread)

    logging.debug("start")
    for thread in threads:
        thread.start()

    logging.debug("join")
    for thread in threads:
        thread.join()

    # videoCap = None
    # fileWatcher = None
    # while True :
    #     try:
    #         fileWatcher = FileWatcher(mainDir="database_clients_camera", maxNbFiles=10, maxFileAgeMinutes=60, intervalSec=10)
    #         fileWatcher.start()
    #         while fileWatcher.isAlive() :
    #             fileWatcher.join(1)
    #         KillThemAll(fileWatcher)
    #     except KeyboardInterrupt:
    #             KillThemAll(fileWatcher)    
    #             logging.info("Exit from {} monitoring ! Bye".format(args.channel_desc))
    #             sys.exit(0)
    #     except Exception as e:
    #         logging.exception("exception during live monitoring : " + str(e))        
    #     except:
    #         logging.exception("unknown exception during live monitoring")           
    # logging.info("Exit from monitoring ! Bye")
