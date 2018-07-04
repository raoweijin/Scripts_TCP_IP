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
    time.sleep(1)

    while ser.inWaiting() > 0:
        out = ser.read(1)
        commandOutput+=out.decode()
    if commandOutput !='':
        #print ( ">>" + out)
        print ( commandOutput)    



print("************************Start case******************************")
command = 'at+cnmi=2,1'
Inputcommand(command)

command = 'at+cmee=2'
Inputcommand(command)

command = 'at+cmgf=1'
Inputcommand(command)


command = 'at+csmp=17,167,0,0'
Inputcommand(command)



command = 'at+cpms="ME","ME","ME"'
Inputcommand(command)

command = 'at+cmgs=\"9496778552\"'
Inputcommand(command)


command = 'abc\x1a'
Inputcommand(command)

command = 'AT+COPS= 2'
Inputcommand(command)

command = 'AT+CPWROFF '
Inputcommand(command)
print("***********************End case******************************")
        
ser.close()
exit()
        
            
                
            