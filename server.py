import socket, select, logging
logging.basicConfig(level=logging.DEBUG)

class server:
    def __init__(self):
        self._connect_list = []
        self.logger = logging.getLogger("server")

        self.RECV_BUFFER = 4096
        self.PORT = 5000
        self.HOST = "0.0.0.0"

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.HOST,self.PORT))
        self.server_socket.listen(10)

        self._connect_list.append(self.server_socket)

    def launch(self):
        self.logger.info("Server launched on port" + str(self.PORT))

        while 1:
            read_sockets,write_sockets,error_sockets = select.select(self._connect_list,[],[])

            for sock in read_sockets:

                if sock == self.server_socket:
                    sockfd, addr = sock.accept()
                    self._connect_list.append(sockfd)
                    self.logger.info("Client (%s,%s) connected"% addr)

                    self.broadcast(sockfd, "[%s,%s] entered room\n" %addr)

                else:
                    try:
                        data = sock.recv(self.RECV_BUFFER)
                        if data:
                            self.broadcast(sock, "\r"+'<'+str(sock.getpeername()) + '>' + data)
                    except:
                        self.broadcast(sock, "Client (%s, %s) is offline" % addr)
                        self.logger.info("Client (%s, %s) is offline" % addr)
                        sock.close()
                        self._connect_list.remove(sock)
                        continue
        self.server_socket.close()

    def broadcast(self, sock, msg):
        for socket in self._connect_list:
            if socket != self.server_socket and socket != sock:
                try:
                    socket.send(msg)
                except:
                    socket.close()
                    self._connect_list.remove(socket)


if __name__ == '__main__':
    sv = server()
    sv.launch()
