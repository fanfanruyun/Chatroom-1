import socket, select, logging
import cPickle as pickle
logging.basicConfig(level=logging.DEBUG)

class server:
    def __init__(self):
        self._connect_list = []
        self.logger = logging.getLogger("server")

        self.RECV_BUFFER = 4096
        self.PORT = 5000
        self.HOST = "0.0.0.0"

        try:
            self.users = pickle.load(open("usrs.dat", "rb"))
        except:
            self.users = []
        self.hash_tb = {}

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.HOST,self.PORT))
        self.server_socket.listen(10)

        self._connect_list.append(self.server_socket)

    def __del__(self):
        pickle.dump(self.users, open("usrs.data", "wb"), True)


    def sign_up(self, user_id, user_pwd):
        for x,y in self.users:
            if x == user_id:
                return False, "conflict"
        
        self.users.append((user_id, user_pwd))
        return True, "success"

    def sign_in(self, user_id, user_pwd):
        for x,y in self.users:
            if x == user_id and y == user_pwd:
                return True, "success"
        return False, "no match"

    def launch(self):
        self.logger.info("Server launched on port" + str(self.PORT))

        while 1:
            read_sockets,write_sockets,error_sockets = select.select(self._connect_list,[],[])

            for sock in read_sockets:

                if sock == self.server_socket:
                    sockfd, addr = sock.accept()
                    self._connect_list.append(sockfd)
                    self.logger.info("Client (%s,%s) connected"% addr)
                    sockfd.send("Login please.\n")
                    #self.broadcast(sockfd, "[%s,%s] entered room\n" %addr)

                else:
                    try:
                        name = sock.getpeername()
                        data = sock.recv(self.RECV_BUFFER)

                        if name not in self.hash_tb:
                            if data[0:7] != "sign_in" and data[0:7] != "sign_up":
                                sock.send("Login please!")
                            elif data[0:7] == "sign_in":
                                op, user_id, user_pwd = data.split()
                                jud = self.sign_in(user_id, user_pwd)
                                if jud[0]:
                                    self.hash_tb[name] = user_id
                                    self.logger.info("%s signed in\n" %user_id)
                                    sock.send("success\n")
                                    self.broadcast(sock, "%s entered room\n" %user_id)
                                else:
                                    sock.send(jud[1])
                            elif data[0:7] == "sign_up":
                                op, user_id, user_pwd = data.split()
                                jud = self.sign_up(user_id, user_pwd)
                                if jud[0]:
                                    self.hash_tb[name] = user_id
                                    self.logger.info("%s signed up\n" %user_id)
                                    sock.send("success\n")
                                    self.broadcast(sock, "%s entered room\n" %user_id)
                                else:
                                    sock.send(jud[1])
                        else:
                            user_id = self.hash_tb[name]
                            if data:
                                self.broadcast(sock, "\r"+'<'+str(user_id) + '>' + data)
                    except:
                        name = sock.getpeername()
                        if name in self.hash_tb:
                            self.broadcast(sock, "Client %s is offline" % self.hash_tb[name])
                            self.logger.info("Client %s is offline" % self.hash_tb[name])
                            del self.hash_tb[name]
                        sock.close()
                        self._connect_list.remove(sock)
                        continue
        self.server_socket.close()

    def broadcast(self, sock, msg):
        for socket in self._connect_list:
            if socket != self.server_socket and socket != sock:
                try:
                    name = socket.getpeername()
                    if name in self.hash_tb:
                        socket.send(msg)
                except:
                    socket.close()
                    self._connect_list.remove(socket)



if __name__ == '__main__':
    sv = server()
    sv.launch()
