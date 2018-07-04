import os 
import sys 
import serial
import time 

#from serial import serial


ser = serial.Serial(
    port='COM13',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ser.isOpen()


def Inputcommand(command):
    command = command+'\r\n'
    ser.write(command.encode())
    commandOutput = ''
    #time.sleep(1)

    '''
    while ser.inWaiting() > 0:
        out = ser.read(1)
        commandOutput+=out.decode()
    if commandOutput !='':
        #print ( ">>" + out)
        print ( commandOutput)    
    '''

for i in range(5):
    '''
    input = 'ati' #raw_input(">>")
    #command = "ati"
    from datetime import datetime, date, time
    datetime.now() 
    import time
    ts = time.time()

    import datetime
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print (st)
    '''
    command = 'ati'
    Inputcommand(command)
    #time.sleep(3)
    print("ddddd-------------i",i)
    
time.sleep(3)
commandOutput = ''
while ser.inWaiting() > 0:
    out = ser.read(1)
    commandOutput+=out.decode()
if commandOutput !='':
    #print ( ">>" + out)
    print ( commandOutput) 
        
ser.close()
exit()
        
            
                
            