data_file = "data.txt"
def file_Write():
    f= open("guru99.txt","w+")
    for i in range(10):
         f.write("This is line %d\r\n" % (i+1))
    f.close() 

def file_Read():

    f=open(data_file, "r")
    if f.mode == 'r':
        contents =f.read()
        #contents = f.readlines()
        #for ie in range(10):
        #    print(contents[ie])
    return contents
    #f.readlines()
def main():
    res = file_Read()
    print(res)
    print(b'123abc')
    print((b)(res))
    
if __name__== "__main__":
  main()