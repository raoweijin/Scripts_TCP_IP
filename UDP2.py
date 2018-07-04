import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('195.34.89.241', 7)
#server_address = ('10.11.250.3', 8443)
server_address = ('172.126.88.3', 8443)
message = b'This is the message.  It will be repeated.'

message = b'hello'

try:

    # Send data
    #print >>sys.stderr, 'sending "%s"' % message
    sent = sock.sendto(message, server_address)

    # Receive response
    #print >>sys.stderr, 'waiting to receive'
    data, server = sock.recvfrom(50)
    print("data is ", str(data))
    #print >>sys.stderr, 'received "%s"' % data

finally:
    #print >>sys.stderr, 'closing socket'
    sock.close()