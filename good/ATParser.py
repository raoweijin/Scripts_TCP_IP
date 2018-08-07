import serial,sys


class AT:
    def __init__(self, port, baudrate, timeout=0.5):
        self.timeout = timeout
        self.s = serial.Serial(port=port, baudrate=baudrate, timeout=timeout,parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

        self.s = serial.Serial(
        port='COM13',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )
    
        print("port is ",port)
        
    def close(self):
        self.s.close()
        
    def write(self, cmd, nonStdResponse=None, timeout=10.0, skipEchoCheck=False):
        # print cmd
        self.s.write(cmd.encode()+'\r\n')
        if not skipEchoCheck:
            if not self._getEcho(cmd):
                print( 'Error: echo of command %s not received' % (cmd))
                sys.exit()
        
        if not nonStdResponse:
            response = self._getResponse(timeout=timeout)
            if response.find('OK') < 0:
                print( 'Error: Response from device %s' % (response))
                sys.exit()
        else:
            response = self._getResponse(timeout=timeout)
            if response.find(nonStdResponse) < 0:
                print( 'Error: Unexpected Response from device %s' % (response))
                sys.exit()
            
        return True
    
    
    def read(self, cmd, timeout=2.0):
        cmd = cmd+'\r\n'
        self.s.write( cmd.encode())
        if not self._getEcho(cmd.encode()):
            print( 'Error: echo of command %s not received' % (cmd))
            sys.exit()

        reading = self._getReading(timeout=timeout)
        
        response = self._getResponse()
        if response.find('OK') < 0:
            print( 'Error: Response from device %s' % (response))
            sys.exit()

        return reading
        
    def readMultiLine(self, cmd, timeout=2.0):
        self.s.write(cmd+'\r\n')
        if not self._getEcho(cmd):
            print( 'Error: echo of command %s not received' % (cmd))
            sys.exit()

        op = ''
        line = ''
        while line.find('OK\r\n') != 0:
            line = self._getReading(timeout=timeout)
            op += line
        return op

    def waitForResponse(self, cmd, timeout=10.0):
        timeoutTarget = int(round(timeout/self.timeout))
        timeoutCnt = 0
        line = ''
        while line.find(cmd) != 0 and timeoutCnt < timeoutTarget:
            timeoutCnt+=1
            line = self._getReading(timeout=timeout)
            print (timeoutCnt, line)
        
        if timeoutCnt >= timeoutTarget:
            return False, ''
        else:
            return True, line
        
    def _getEcho(self, cmd, timeout=2.0):
        # print [ord(e) for e in cmd]
        timeoutTarget = int(round(timeout/self.timeout))
        timeoutCnt = 0
        
        while timeoutCnt < timeoutTarget:
            timeoutCnt+=1
            value = self.s.readline()
            # print '*: ', value
            # print [ord(e) for e in value]
            if value.find(cmd) >=0:
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
            if value != '' and value != '\r\n':
                # Found some response
                # print 'Reading Found'
                return value
        return ''
    
    def _getResponse(self, timeout=2.0):
        timeoutTarget = int(round(timeout/self.timeout))
        timeoutCnt = 0
        
        while timeoutCnt < timeoutTarget:
            timeoutCnt+=1
            value = self.s.readline()
            # print '^: ', value
            if value != '' and value != '\r\n':
                # Found some response
                # print 'Response Found'
                return value
        return 'Timeout'

        
if __name__ == '__main__':
    a = AT('COM10', 115200)
    a.write('AT')
    value = a.read('AT+ULSTFILE=0')
    print (value)
    a.close()