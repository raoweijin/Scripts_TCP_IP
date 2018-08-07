import serial, sys, json
import serial, sys, json
from datetime import datetime, timedelta
from random import randint
data_file = "data.txt"
def GenFile():
    global fileContents
    event = 'check in'
    noDays = 1
    epocTime = datetime.strptime('2000-01-01T00:00:00.00Z', '%Y-%m-%dT%H:%M:%S.%fZ') 
    nowTime = int((datetime.utcnow() - epocTime).total_seconds())
    # print "startTime %s " % nowTime
    f= open("test.txt","w+")
    for i in range (0, noDays):
        climate = []
        daysAgo = (noDays - i) * 24 * 3600
        periodStart = nowTime - daysAgo
        periodEnd = periodStart + (24 * 3600)
        
        tmpPeriodStart = datetime.strptime('2000-01-01T0:0:0', '%Y-%m-%dT%H:%M:%S') + timedelta(seconds=periodStart)
        tmpperiodEnd = datetime.strptime('2000-01-01T0:0:0', '%Y-%m-%dT%H:%M:%S') + timedelta(seconds=periodEnd)

        for j in range (0, 24):
        #for j in range (0, 2):
            readTime = periodStart + (j * 3600)
            climate.append([readTime, randint(0,40) - randint(0,40), randint(0,100)])
        fileContents = json.dump({
        # fileContents = 'Content-Type: application/json ' + json.dumps({
        # fileContents = json.dumps({
                    "sensorId":"dXrACAkOSC",
                    "event":event,
                    "macAddress":"JA:ME:SB:LA:CK",
                    "firmwareVersion":"M.I.C.e",
                    "bssid":"JA:ME:SB:LA:CK",
                    "wifiFirmwareVersion":"A,B.C",
                    "authToken":"1b189pr9s61zvr7t",
                    "batteryLevel":"3100",
                    "opGood":"1",
                    "compWakeCount":"2",
                    "sensorLog":"NA",
                    "rssi":"-84",
                    "hardwareVersion":"2",
                    "devSignature":"01473531373430340045004f",
                    "radioVersion":"24239d69",
                    "channel":"11",
                    "security":"1",
                    "resetReason":"0",
                    "currentTime": periodEnd - 10,
                    "readings": json.dumps(climate),
                    "ssid":"JAMES",
                    "pattern" : "0"
                    },f)
        print (fileContents)
        f.close()
def file_Write():
    f= open("guru99.txt","w+")
    
    
    
    for i in range(10):
         f.write("This is line %d\r\n" % (i+1))
    f.close() 

def file_Read():

    f=open(data_file, "r")
    if f.mode == 'r':
        contents =f.read()
        #contents = f.readlines()
        #for ie in range(10):
        #    print(contents[ie])
    return contents
    #f.readlines()
def main():
    GenFile()
    '''
    res = file_Read()
    print(res)
    print(b'123abc')
    print((b)(res))
    '''
    
if __name__== "__main__":
  main()