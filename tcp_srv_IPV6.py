import socket

Tcp_port = 8442 
def fetch_local_ipv6_address(port=10008):
    # try to detect whether IPv6 is supported at the present system and
    # fetch the IPv6 address of localhost.
    if not socket.has_ipv6:
        raise Exception("the local machine has no IPv6 support enabled")

    addrs = socket.getaddrinfo("localhost", port, socket.AF_INET6, 0, socket.SOL_TCP)
    # example output: [(23, 0, 6, '', ('::1', 10008, 0, 0))]

    if len(addrs) == 0:
        raise Exception("there is no IPv6 address configured for localhost")

    entry0 = addrs[0]
    sockaddr = entry0[-1]
    return sockaddr


def listen():
    connection = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    localAddr = fetch_local_ipv6_address(Tcp_port)
    connection.bind(localAddr)
    connection.listen(10)
    while True:
        current_connection, address = connection.accept()
        while True:
            data = current_connection.recv(2048)

            if data == 'quit\r\n':
                current_connection.shutdown(1)
                current_connection.close()
                break

            elif data == 'stop\r\n':
                current_connection.shutdown(1)
                current_connection.close()
                exit()

            elif data:
                current_connection.send(data)
                print(data)


if __name__ == "__main__":
    try:
        listen()
    except KeyboardInterrupt:
        pass
