from datetime import datetime

# Envoyé: mercredi 26 octobre 2022 à 17:46
# De: "etienne corvee" <etienne.corvee@caramail.com>
# À: "etienne corvee" <etienne.corvee@caramail.com>
# Objet: TODO convertStringTimestampToDatetimeAndMicrosecValue

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