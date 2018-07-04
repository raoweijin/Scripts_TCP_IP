#cafile /home/n7test/wrao/mosquitto_srv/certs/ca.crt
#keyfile /home/n7test/wrao/mosquitto_srv/certs/server.pem
#certfile /home/n7test/wrao/mosquitto_srv/certs/server.crt
#tls_version tlsv1.1
#context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
# weijin no    
import socket, ssl

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
        print("data is ",data)
    # finished with client
    
    
#context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.load_cert_chain(certfile="server.crt", keyfile="server.pem")

bindsocket = socket.socket()
bindsocket.bind(('0.0.0.0', 8443))
bindsocket.listen(5)

while True:
    newsocket, fromaddr = bindsocket.accept()
    connstream = context.wrap_socket(newsocket, server_side=True)
    try:
        deal_with_client(connstream)
    finally:
        connstream.shutdown(socket.SHUT_RDWR)
        connstream.close()
        
