import os 
import sys 
import serial
import time 

#from serial import serial


ser = serial.Serial(
    port='COM25',
    #baudrate=9600,
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ser.isOpen()




def Inputcommand(command):
    command = command+'\r\n'
    #print("Run command ",command)
    ser.write(command.encode())
    commandOutput = ''
    #time.sleep(1)


    while ser.inWaiting() > 0:
        out = ser.read(1)
        commandOutput+=out.decode()
    if commandOutput !='':
        #print ( ">>" + out)
        print ( commandOutput)    
        
        
        
command = 'ati'
Inputcommand(command)
print("************************Start case******************************")
data = "\"12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdefgh12334567890abcdef\""
length = len(data)
print("length is ",length)
#data="\"1234\""
command = 'AT+USOCR=6'
Inputcommand(command)
time.sleep(1)

command = 'AT+USOCO=0,\"87.92.104.45\",12345'
#command = 'AT+USOCO=0,\"172.126.88.3\",8442'
Inputcommand(command)
time.sleep(3)


import datetime;



for i in range(500):
    ts = datetime.datetime.now().timestamp()
    print(ts)
    command = 'AT+USOWR=0,1024,'+data
    #print("write data", command)
    Inputcommand(command)
    time.sleep(1)
  
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

    #time.sleep(3)
    print("iteration ",i)
print("************************End case******************************")
    
command = 'AT+USOCl=0'
Inputcommand(command)
time.sleep(3)
        
ser.close()
exit()
        
            
                
            