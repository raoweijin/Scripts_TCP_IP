#Python 3.x
import os 
import sys 
import serial
import time 

#from serial import serial


ser = serial.Serial(
    port='COM13',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ser.isOpen()


def Inputcommand(command):
    command = command+'\r\n'
    ser.write(command.encode())
    commandOutput = ''
    #time.sleep(0.02)

    while ser.inWaiting() > 0:
        out = ser.read(1)
        commandOutput+=out.decode()
    if commandOutput !='':
        #print ( ">>" + out)
        print ( commandOutput)    

def InputSpecialcommand(command):
    #command = command+'\r\n'
    ser.write(command.encode())
    commandOutput = ''
    #time.sleep(0.02)

    while ser.inWaiting() > 0:
        out = ser.read(1)
        commandOutput+=out.decode()
    if commandOutput !='':
        #print ( ">>" + out)
        print ( commandOutput)   
    
# Create TCP socket
command = 'at+usocr=6'
Inputcommand(command)
time.sleep(2)
# Connect TCP socket
command = 'at+usoco=0,"172.126.88.3",8442'
Inputcommand(command)    

for i in range(30):
    print("iteration ",i)
    # TCP Direct Link
    command = 'AT+USODL=0'
    Inputcommand(command)   
    time.sleep(2)

    # Disconnect TCP Direct Link
    command = '+++'
    InputSpecialcommand(command)    
    time.sleep(0.20)
    # Disconnect TCP Direct Link
    command = 'AT+USOWR=0,12 ,"123456789012"'
    #Inputcommand(command)  
    command = 'at+usowr=0,700,"1234555555555555555555555555555555555555555555555555555555555555555555567890123455555555555555555555555555555555555555555555555555555555555555555556789012345555555555555555555555555555555555555555555555555555555555555555555678901234555555555555555555555555555555555555555555555555555555555555555555567890123455555555555555555555555555555555555555555555555555555555555555555556789012345555555555555555555555555555555555555555555555555555555555555555555678901234555555555555555555555555555555555555555555555555555555555555555555567890123455555555555555555555555555555555555555555555555555555555555555555556789012345555555555555555555555555555555555555555555555555555555555555555555678901234555555555555"'
    Inputcommand(command)
    time.sleep(2)

'''    
for i in range(3):
    print("************************Start case",i,"******************************")
    command = 'at+usowr=0,152,"12345555555555555555555555555555555555555555555555555555555555555555555678901234555555555555555555555555555555555555555555555555555555555555555555567890"'
    Inputcommand(command)

    command = 'at +usord = 0,152'
    Inputcommand(command)
    print("***********************End case******************************")
        
'''
ser.close()
exit()
        
            
                
            