import os 
import sys 
import serial
import time 


ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ser.isOpen()

print ('Enter your commands below. \r\n Insert "exit" to leave the application.')

input = 1

while 1:
    input = 'ati' #raw_input(">>")
    #command = "ati"

    if input == 'exit':
        ser.close()
        exit()
    else:
        ser.write(input + '\r\n')
        out = ''
        time.sleep(1)
        try:

            while ser.inWaiting() > 0:
                out +=ser.read(1)
            if out !='':
                print ( ">>" + out)
                
        except:
            print ("There is an issue while reading data Please try again")
            time.sleep(1)
	ser.close()
	exit()
            
            
                
            
            
