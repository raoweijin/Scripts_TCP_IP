import serial,sys


class AT:
    def __init__(self, inport, baudrate, timeout=0.5):
        self.timeout = timeout
        self.s = serial.Serial(port=inport, baudrate=baudrate, timeout=timeout,parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

        #self.s = serial.Serial(port='COM74',baudrate=115200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
        self.s.isOpen()
        print("Port is ",inport)
        
    def close(self):
        self.s.close()
        
    def write(self, cmd, nonStdResponse='OK', timeout=10.0, skipEchoCheck=False, readLine = True):
        # print cmd
        cmd = cmd + '\r\n'
        print("write: ",cmd)
        cmd = cmd.encode()
        self.s.write(cmd)
        if not skipEchoCheck:
            if not self._getEcho(cmd):
                print( 'Error: echo of command %s not received' % (cmd))
                sys.exit()
        print("debug: nonStdResponse is", nonStdResponse)
        if  nonStdResponse != True: 
            if readLine == True:
                response = self._getResponse(timeout=timeout)
            else:
                response = self._getResponseSpecial(timeout=timeout)                
        #response = response.decode()
            print("responsie is ",response)
        if  nonStdResponse == True:       
            print("None check")
        elif  nonStdResponse == 'OK':

            if response.find('OK') < 0:
                print( 'Error: Response from device %s' % (response))
                sys.exit()
        else:

            if response.find(nonStdResponse) < 0:
                print( 'Error: Unexpected Response from device %s' % (response))
                sys.exit()
            
        return True
        
    def writeSpecial(self, cmd, nonStdResponse='OK', timeout=10.0, skipEchoCheck=False):
        # print cmd
        #cmd = cmd + '\r\n'
        print("write: ",cmd)
        cmd = cmd.encode()
        self.s.write(cmd)
        '''
        if not skipEchoCheck:
            if not self._getEcho(cmd):
                print( 'Error: echo of command %s not received' % (cmd))
                sys.exit()
        '''        
        print("debug: nonStdResponse is", nonStdResponse)
        response = self._getResponseSpecial(timeout=timeout)
        #response = response.decode()
        print(response)
        if  nonStdResponse == True:       
            print("None check")
        elif  nonStdResponse == 'OK':

            if response.find('OK') < 0:
                print( 'Error: Response from device %s' % (response))
                sys.exit()
        else:

            if response.find(nonStdResponse) < 0:
                print( 'Error: Unexpected Response from device %s' % (response))
                sys.exit()
            
        return True   
    
    def read(self, cmd, timeout=2.0):
        cmd = cmd+'\r\n'
        print("read: ", cmd)
        self.s.write( cmd.encode())
        if not self._getEcho(cmd.encode()):
            print( 'Error: echo of command %s not received' % (cmd))
            sys.exit()

        reading = self._getReading(timeout=timeout)
        #reading = reading.decode()
        print(reading)
        response = self._getResponse()
        #response = response.decode()
        print(response)
        if response.find('OK') < 0:
            print( 'Error: Response from device %s' % (response))
            #sys.exit()

        return reading
        
    def readMultiLine(self, cmd, timeout=2.0):
        cmd = cmd+'\r\n'
        print("read: ", cmd)
        self.s.write( cmd.encode())
        
        if not self._getEcho(cmd):
            print( 'Error: echo of command %s not received' % (cmd))
            sys.exit()

        op = ''
        line = ''
        while line.find('OK\r\n') != 0:
            line = self._getReading(timeout=timeout)
            #line = line.decode()
            op += line
        return op

    def waitForResponse(self, cmd, timeout=10.0):
        timeoutTarget = int(round(timeout/self.timeout))
        timeoutCnt = 0
        line = ''
        while line.find(cmd) != 0 and timeoutCnt < timeoutTarget:
            timeoutCnt+=1
            line = self._getReading(timeout=timeout)
            #line = line.decode()
            print (timeoutCnt, line)
        
        if timeoutCnt >= timeoutTarget:
            return False, ''
        else:
            return True, line
        
    def _getEcho(self, cmd, timeout=2.0):
        # print [ord(e) for e in cmd]
        timeout= 2
        timeoutTarget = int(round(timeout/self.timeout))
        timeoutCnt = 0
        #print("cmd is ",cmd, "leng is ",len(cmd))
        if type(cmd) != str:
            cmd = cmd.decode()
        length = len(cmd)
        while timeoutCnt < timeoutTarget:
            timeoutCnt+=1
            value = self.s.readline()
            value = value.decode()
            #print ('*: ', value)
            #print ([ord(e) for e in value])
            if value.find(cmd[0:length-2]) >=0:
                # Echo command found
                # print 'Echo Found'
                return True
        return False
    
    def _getReading(self, timeout=2.0):
        timeoutTarget = int(round(timeout/self.timeout))
        timeoutCnt = 0
        
        while timeoutCnt < timeoutTarget:
            timeoutCnt+=1
            value = self.s.readline()
            # print '$: ', value
 

            if value != b'' and value != b'\r\n':
                # Found some response
                # print 'Reading Found'
                value = value.decode()
                return value
        return ''
    
    def _getResponse(self, timeout=2.0):
        #timeout=0.1
        timeoutTarget = int(round(timeout/self.timeout))
        timeoutCnt = 0
        print("start getresponse")
        while timeoutCnt < timeoutTarget:
            timeoutCnt+=1
            value = self.s.readline()
            print("response value is ",value)
            # print '^: ', value
            if value != b'' and value != b'\r\n':
                # Found some response
                # print 'Response Found'
                value = value.decode()
                return value
        return 'Timeout'

    def _getResponseSpecial(self, timeout=2.0):
        #timeout=0.1
        timeoutTarget = int(round(timeout/self.timeout))
        timeoutCnt = 0
        print("start getresponse")
        while timeoutCnt < timeoutTarget:
            timeoutCnt+=1
            value = self.s.read(1)
            print("response value is ",value)
            # print '^: ', value
            if value != b'' and value != b'\r\n':
                # Found some response
                # print 'Response Found'
                value = value.decode()
                return value
        return 'Timeout'
        
if __name__ == '__main__':
    a = AT('COM13', 115200)
    a.write('AT')
    value = a.read('AT+ULSTFILE=0')
    #print (value)
    
    a.write('AT+UDWNFILE="test2.txt",5','>',timeout=1,readLine=False)
    a.writeSpecial("123456",  timeout=5)

    a.write('AT')
    value = a.read('AT+ULSTFILE=0')
    a.close()