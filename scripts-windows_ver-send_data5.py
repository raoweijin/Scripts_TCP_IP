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
    time.sleep(0.5)

    while ser.inWaiting() > 0:
        out = ser.read(1)
        commandOutput+=out.decode()
    if commandOutput !='':
        #print ( ">>" + out)
        print ( commandOutput)    


for i in range(3):
    print("************************Start case",i,"******************************")
    command = 'at+usowr=0,152,"12345555555555555555555555555555555555555555555555555555555555555555555678901234555555555555555555555555555555555555555555555555555555555555555555567890"'
    Inputcommand(command)

    command = 'at +usord = 0,152'
    Inputcommand(command)
    print("***********************End case******************************")
        
ser.close()
exit()
        
            
                
            