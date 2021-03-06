 # One echo server with Python scripts
 # The server.crt and server.pem should be copied into the same folder of python script
 #Python 3.x
 #Weijin Rao
import socket, ssl

Server_Certfile = "server.crt"
Server_Keyfile = "server.pem"
Data_file = "data.txt"
tcp_port = 8443
def deal_with_client(connstream):
    #data = connstream.recv(1024)
    #print("data is ",data)
    # empty data means the client is finished with us
    #while data:
        #if not do_something(connstream, data):
            # we'll assume do_something returns False
            # when we're finished with client
        #    break
    print("TCP server will the file ",Data_file)
    data = Read_Data(Data_file)
    connstream.send(data)
    #data = connstream.recv(1024)
    #    print("data is ",data)
    # finished with client
    
def Read_Data(fileName):
    f=open(Data_file, "r")
    data = f.read()
    return data.encode('UTF-8')  # Chang the data into byte format; it is similar to b'xxx'
#context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.load_cert_chain(certfile=Server_Certfile, keyfile=Server_Keyfile)

bindsocket = socket.socket()
bindsocket.bind(('0.0.0.0', tcp_port))
bindsocket.listen(5)

while True:
    newsocket, fromaddr = bindsocket.accept()
    connstream = context.wrap_socket(newsocket, server_side=True)
    try:
        deal_with_client(connstream)
    finally:
        connstream.shutdown(socket.SHUT_RDWR)
        connstream.close()
        
