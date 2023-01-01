import os
import psutil
import base64
from datetime import datetime
import logging
import socket, errno

IMGEXT='jpg'

# populate_fake_images()
# exit(1)
# uri_result = load_sample("todel.png")

def isascii(s):
    """Check if the characters in string s are in ASCII, U+0-U+7F."""
    return len(s) == len(s.encode())

def isBase64(sb):
    try:
            if isinstance(sb, str):
                    # If there's any unicode here, an exception will be thrown and the function will return false
                    sb_bytes = bytes(sb, 'ascii')
            elif isinstance(sb, bytes):
                    sb_bytes = sb
            else:
                    raise ValueError("Argument must be string or bytes")
            return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
    except Exception:
            return False

def is_port_in_use(port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def check_port(i):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print("... port", i)
        s.bind(("127.0.0.1", i))
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            print("Port is already in use", i)
        else:
            print("Port available", i)
            print(e)
            return False   
    s.close()
    return True

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
       
# TEST in main:
#       # if args.setBashrc is True:
    #     print("[INFO]updateBashRcWithEcovisionLibPath")
    #     updateBashRcWithEcovisionLibPath(args.ecovisionPath)
    #     print("[INFO]exit, export /user/.bashrc and restart manager")
    #     exit(0)



#def get_encoded_img(image_path):
    #img = Image.open(image_path, mode='r')
    #img_byte_arr = io.BytesIO()
    #img.save(img_byte_arr, format='PNG')
    #my_encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
    #return my_encoded_img

def get_encoded_img(image_path):
    with open(image_path, mode="rb" ) as f:
        img_byte_arr = f.read()                 # bytes
        a = base64.encodebytes(img_byte_arr)    # bytes (base64 encoded)
        b = a.decode('ascii')                   # str
        # print("[DEBUG]get_encoded_img ", image_path, "step0 fread rb           : ", type(img_byte_arr))
        # print("[DEBUG]get_encoded_img ", image_path, "step1 encode base64 bytes: ", type(a))
        # print("[DEBUG]get_encoded_img ", image_path, "step2 decode ascii       : ", type(b))
        # # return base64.encodebytes(img_byte_arr).decode('ascii')
        return b

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

# def get_encoded_img(image_path):
#     with open(image_path, mode="rb" ) as f:
#         img_byte_arr = f.read()
#         return base64.encodebytes(img_byte_arr).decode('ascii')


def split_images(input):
    '''new_ids = []
    function = lambda x, y: [x, y]
    for i in range(0, len(input), 1024):
        try:
            new_ids.append(function(input[i], input[i + 1023]))
        except IndexError:
            new_ids.append(input[i])
    return new_ids'''

    output = []
    start = 0
    end = len(input)
    step = 2048
    for i in range(start, end, step):
        x = i
        output.append(input[x:x+step])
    return output