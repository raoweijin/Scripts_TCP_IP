import serial, sys, json,time
from datetime import datetime, timedelta
from ATParser import AT
from random import randint

def CheckRes(target, result):
        target = target.lower().strip('\r\n')
        result = result.lower().strip('\r\n')
        #print("target and result", target, result,"not find")
        if target == result:
            print("True: That is right. value is ",result)
            return True
        else:
            print("False: That is not correct. Value is ", result)
            return False

def Main():
    a = AT('COM74', 115200)
    Res = a.write('at+usecprf=0,3,"RootCA"')
    Res = a.write('at+usecprf=0,5,"ClientCert"')
    Res = a.write('at+usecprf=0,6,"ClientKey"')
    #value = a.read('at+usecprf=0,6,"ClientKey"')

    Res = a.read('at+usocr=6')
    Res = a.write('AT+USOSEC=0,1,0')    
    Res = a.write('at+usoco=0,"172.126.88.3",8444')

    for i in range(10):    
        Res = a.read('at+usowr=0,3,"123"')        
        #a.write('AT')
        if False == CheckRes("+USOWR: 0,3", Res):
            break;
        time.sleep(0.1)         
        
        Res = a.read('at+usowr=0,76,"7676555555555555555555555555555555555555555555555555555555555555555555567890"')        
        #a.write('AT')

        if False == CheckRes("+USOWR: 0,76", Res):
            break;
        time.sleep(0.1)              

        Res = a.read('at+usowr=0,77,"77775555555555555555555555555555555555555555555555555555555555555555555678901"')        
        #a.write('AT')

        if False == CheckRes("+USOWR: 0,77", Res):
            break;
        time.sleep(0.1)              
            
            
        Res = a.read('at+usowr=0,152,"15245555555555555555555555555555555555555555555555555555555555555555555678901234555555555555555555555555555555555555555555555555555555555555555555567890"')        
        #a.write('AT')

        if False == CheckRes("+USOWR: 0,152", Res):
            break;
        time.sleep(0.1)   
        a.read('at+usord=0,0')
        time.sleep(0.1)       
        ########################################
        #a.read('at+usord=0,3')
        a.read('at+usord=0,1')
        time.sleep(0.1)  
        a.read('at+usord=0,2')
        time.sleep(0.1) 
        #######################################

        
        a.read('at+usord=0,76')
        time.sleep(0.1)  
        a.read('at+usord=0,77')   
        time.sleep(0.1)        
        a.read('at+usord=0,152')          
        time.sleep(0.2)  
        print("Iteration******************************************** ", i)
        time.sleep(0.1)    
    print("*************Stop Writing****************************************")
    Res = a.read('at+usowr=0,4,"stop"')      
    
    #Res = a.write('at+usocl=0')    
    time.sleep(10)
    a.close()
    sys.exit()
    
    
    
if __name__ == '__main__':
    Main()