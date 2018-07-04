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

print ('Enter your commands below. \r\n Insert "exit" to leave the application.')

input = 1

while 1:

    input = 'ati' #raw_input(">>")
    #command = "ati"

    if input == 'exit':
        ser.close()
        exit()
    else:
        command = input+'\r\n'
        ser.write(command.encode())
        commandOutput = ''
        time.sleep(1)
        try:

            while ser.inWaiting() > 0:
                out = ser.read(1)

                commandOutput+=out.decode()
            if commandOutput !='':
                #print ( ">>" + out)
                print ( commandOutput)
                
        except:
            print ("There is an issue while reading data Please try again")
            time.sleep(1)
    ser.close()
    exit()
            
            
                
            
            
