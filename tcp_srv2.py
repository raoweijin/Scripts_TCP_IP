import socket

def listen():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(('10.11.250.3', 8442))
    connection.listen(10)
    while True:
        current_connection, address = connection.accept()
        while True:
            data = current_connection.recv(2048)
            print "get data is"
            print "data"
            if data == 'quit\r\n':
                current_connection.shutdown(1)
                current_connection.close()
                break

            elif data == 'stop\r\n':
                current_connection.shutdown(1)
                current_connection.close()
                exit()

            elif data:
                data = b'HTTP/1.1 200 OK\r\nServer: nginx\r\nDate: Mon, 26 Mar 2018 22:36:26 GMT\r\nContent-Type: text/plain;charset=UTF-8\r\nConnection: close\r\nX-Powered-By: PHP/5.6.34\r\nX-Powered-By: PleskLin\r\n\r\nOK - Report'
                current_connection.send(data)
                print data
                current_connection.shutdown(1)
                current_connection.close()


if __name__ == "__main__":
    try:
        listen()
    except KeyboardInterrupt:
        pass