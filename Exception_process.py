import sys
print("1")
while(1):
    try:
        #sys.exit()
        while (1):
            print("haha")
            #a=10/0
    except:
    #except KeyboardInterrupt:
        print("get key")
        print("except: ",sys.exc_info()[0])
        
    finally:
        print("2")
        continue