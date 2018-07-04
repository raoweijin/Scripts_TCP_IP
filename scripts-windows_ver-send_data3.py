import os 
import sys 
import serial
import time 

#from serial import serial


ser = serial.Serial(
    port='COM25',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ser.isOpen()




def Inputcommand(command):
    command = command+'\r\n'
    print("Run command ",command)
    ser.write(command.encode())
    commandOutput = ''
    time.sleep(1)


    while ser.inWaiting() > 0:
        out = ser.read(1)
        commandOutput+=out.decode()
    if commandOutput !='':
        #print ( ">>" + out)
        print ( commandOutput)    
        
        
        
command = 'ati'
Inputcommand(command)
print("************************Start case******************************")




for i in range(50):
    command =  'at+usocr=6'    
    Inputcommand(command)
    time.sleep(1)
    
    command = 'at+usoco=0,"echo.u-blox.com",7'
    Inputcommand(command)
    time.sleep(1)
    
    command = 'at+usocl=0'
    Inputcommand(command)
    time.sleep(5)
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
    print("iteration************************************ ",i)
print("************************End case******************************")
    

        
ser.close()
exit()
        
            
                
            