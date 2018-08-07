#@08/06 Add exception process and close the sockets
#cafile /home/n7test/wrao/mosquitto_srv/certs/ca.crt
#keyfile /home/n7test/wrao/mosquitto_srv/certs/server.pem
#certfile /home/n7test/wrao/mosquitto_srv/certs/server.crt
#tls_version tlsv1.1
#context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
# weijin no    
import socket, ssl,sys

Server_Certfile = "server.crt"
Server_Keyfile = "server.pem"
tcp_port = 8444
def deal_with_client(connstream):
    data = connstream.recv(1024)
    print("data is ",data)
    # empty data means the client is finished with us
    while data:
        #if not do_something(connstream, data):
            # we'll assume do_something returns False
            # when we're finished with client
        #    break
        connstream.send(data)
        data = connstream.recv(1024)
        if data=='quit\r\n' or data=='stop':
            print("data is stop and will close socket ",data)
            connstream.shutdown(1)
            # connstream.close()
            # socket.shutdown(1)
            break
        print("data is ",data)
    # finished with client
    
    
#context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.load_cert_chain(certfile=Server_Certfile, keyfile=Server_Keyfile)

bindsocket = socket.socket()
bindsocket.bind(('0.0.0.0', tcp_port))
bindsocket.listen(5)
try:
    while True:
        newsocket, fromaddr = bindsocket.accept()
        print("New connection is established", newsocket,fromaddr)
        connstream = context.wrap_socket(newsocket, server_side=True)
        try:
            deal_with_client(connstream)
        #finally:
        except KeyboardInterrupt:
            print("This is KeyboardInterrupt")
            connstream.shutdown(socket.SHUT_RDWR)
            bindsocket.shutdown(1)
            #connstream.close()
except:
    print("\nExcept: ",sys.exc_info()[1])
    bindsocket.shutdown(1)
    print("close socket")
        
