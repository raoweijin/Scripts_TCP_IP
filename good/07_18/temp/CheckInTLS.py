import serial, sys, json
import serial, sys, json
from datetime import datetime, timedelta
from ATParser import AT
from random import randint
import time
CheckInFilename = 'checkin.txt'
HTTPResponseFilename = 'httpresponse.txt'

fileContents = """X-Parse-Application-Id: bjzD2Lbe1uEnN2HImP60iqp62u2JhibubMUEkOhT {"authToken": "1b189pr9s61zvr7t", "macAddress": "JA:ME:SB:LA:CK:WE", "radioVersion": "24239d69", "bssid": "JA:ME:SB:LA:CK:WE", "sensorId": "dXrACAkOSC", "event": "check in", "firmwareVersion": "M.I.C.e", "devSignature": "01473531373430340045004f", "pattern": "0", "compWakeCount": "2", "batteryLevel": "3100", "channel": "11", "resetReason": "0", "hardwareVersion": "2", "readings": "[[562800303, 14, 50], [562803903, -23, 99], [562807503, -5, 15], [562811103, 20, 75], [562814703, -2, 24], [562818303, 4, 55], [562821903, 21, 7], [562825503, 19, 84], [562829103, -21, 29], [562832703, 1, 11], [562836303, -11, 43], [562839903, 3, 70], [562843503, -28, 1], [562847103, -3, 43], [562850703, 27, 34], [562854303, -18, 16], [562857903, -3, 63], [562861503, -4, 62], [562865103, 33, 21], [562868703, 3, 58], [562872303, 17, 70], [562875903, 4, 68], [562879503, -29, 0], [562883103, -6, 89]]", "opGood": "1", "ssid": "JAMES", "currentTime": 562886693, "sensorLog": "NA", "rssi": "-84", "security": "1", "wifiFirmwareVersion": "A,B.C"}"""

def GenFile():
    global fileContents
    event = 'check in'
    noDays = 1
    epocTime = datetime.strptime('2000-01-01T00:00:00.00Z', '%Y-%m-%dT%H:%M:%S.%fZ') 
    nowTime = int((datetime.utcnow() - epocTime).total_seconds())
    # print "startTime %s " % nowTime
    
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
        fileContents = json.dumps({
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
                    })
        print (fileContents)

def ProcessResponse(input):
    input = input.strip()
    cmd, data = input.split(': ')
    data = data.split(',')
    return cmd, data

def Main():
    a = AT('COM13', 115200)
    
    # Wait until registered on the network
    print ('Waiting for network registration')
    v = a.read('AT+CGATT?')
    c,d = ProcessResponse(v)
    while d[0] != '1':
        print ('Waiting for network registration')
        v = a.read('AT+CGATT?')
        c,d = ProcessResponse(v)
        print (d)
    
    
    # Connect to Network
    print ('Connecting to Network')
    a.write('AT+COPS=0') 
    v = a.read('AT+CEREG?')
    c,d = ProcessResponse(v)
    if d[0] != '0' or d[1] != '1':
        print ('Error: Did not connect to network!')
        sys.exit()
    v = a.read('AT+COPS?')
    c,d = ProcessResponse(v)
    print ('Connected to %s' % (d[2]))
    
    # Set-up TLS
    print ('Setting up TLS')
    a.write('AT+USECMNG=1,0,"DigiCA","test.cer"','+USECMNG: 1,0,"DigiCA","D474DE575C39B2D39C8583C5C065498A"') #Import certificate
    a.write('AT+USECPRF=2,0,1')
    a.write('AT+USECPRF=2,3,"DigiCA"')
    
    # Set-up HTTP Details
    print ('Setting up the HTTP details')
    # AT+UHTTP=<profile_id>,<op_code>,<param_val>[,<param_val1>]
    a.write('AT+UHTTP=0,1,"roost-parse-dev.herokuapp.com"') # Set Server Name
    a.write('AT+UHTTP=0,9,"0:X-parse-Application-Id:bjzD2Lbe1uEnN2HImP60iqp62u2JhibubMUEkOhT"') #Set custom header
    a.write('AT+UHTTP=0,5,443') #Set port
    a.write('AT+UHTTP=0,6,1,2') #Enable the SSL/TLS for the UHTTP profile #0 and
                                #specify the SSL/TLS security profile 2.
    a.write('AT+UHTTP=0,4,0') # Disable Authentication
    #a.write('AT+UHTTP=0,6,0') # Disable TLS - Module FW does not currently support TLS
    
    # Update File to Send
    # - See if CheckIn File exists and delete
    print ('Checking for Old Files')
    v = a.read('AT+ULSTFILE=0')
    c,d = ProcessResponse(v)
    if '"'+CheckInFilename+'"' in d:
        print ('Found old CheckIn File - deleting')
        #a.write('AT+UDELFILE="%s"' % (CheckInFilename))
    
    # - See if Response File exists and delete
    v = a.read('AT+ULSTFILE=0')
    c,d = ProcessResponse(v)
    '''
    if '"'+HTTPResponseFilename+'"' in d:
        print ('Found old Response File - deleting')
        a.write('AT+UDELFILE="%s"' % (HTTPResponseFilename))
    '''
    # - Download CheckIn File
    print ('Download CheckIn File')
    #GenFile()
    #a.write('AT+UDWNFILE="%s",%s' % (CheckInFilename, len(fileContents)-1), nonStdResponse='>')
    #a.writeSpeical(fileContents, skipEchoCheck=True, nonStdResponse=True, timeout=10.0)

    # Send Post
    #AT+UHTTPC=<profile_id>,<http_command>,<path>,<filename>[,<param1>[,<param2>[,<param3>]]]
    print ('Checking In!')
    a.write('AT+UHTTPC=0,4,"/1/functions/updateSensor","%s","%s",4' % (HTTPResponseFilename, CheckInFilename), timeout = 10.)
    # a.write('AT+UHTTPC=0,4,"/1/functions/updateSensor","%s","%s",6, "X-Parse-Application-Id: bjzD2Lbe1uEnN2HImP60iqp62u2JhibubMUEkOhT"' % (HTTPResponseFilename, CheckInFilename), timeout = 10.)
    # a.write('AT+UHTTPC=0,4,"/1/functions/updateSensor","%s","%s",6, "X-Parse-Application-Id: bjzD2Lbe1uEnN2HImP60iqp62u2JhibubMUEkOhT Content-Type: application/json"' % (HTTPResponseFilename, CheckInFilename), timeout = 10.)
    
    # Wait for response
    r, v = a.waitForResponse('+UUHTTPCR:')
    if not r:
        print ('Error: Expected Response (%s) not received. Received: %s' % ('+UUHTTPCR:', v))
        sys.exit()
    
    # - See if Response File exists 
    print ('Checking for Response File')
    v = a.read('AT+ULSTFILE=0')
    c,d = ProcessResponse(v)
    if '"'+HTTPResponseFilename+'"' in d:
        print ('Found new Response File')

    # - Check file size
    v = a.read('AT+ULSTFILE=2,"%s"' % (HTTPResponseFilename))
    c,d = ProcessResponse(v)

    # - Read response file
    print ('Reading Response File')
    v = a.readMultiLine('AT+URDFILE="%s"' % (HTTPResponseFilename), timeout=10.)
    print (v)
    i = v.find('{"result":')
    if i > 0:
        s = v[i:].find('\n')    # Find end of line
        # Fix JSON Object
        data = v[i:i+s-2].replace("'", '"') 
        data = data.replace('"{', '{')
        data = data.replace('}"', '}')
        
        data = json.loads(data)
        if data['result']['result'] == 'success':
            print ('Checked In')
        else:
            print ('Error: Failed to Check In')
            sys.exit()
    else:
        print ('Error: Could not find results')
        sys.exit()
    
    
    
if __name__ == '__main__':
    for i in range(30):
        print("**********************************iteration ",i," ***************************************************")
        Main()
        time.sleep(2)