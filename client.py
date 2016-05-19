import socket,select,sys,logging
logging.basicConfig(level=logging.DEBUG)

class client:
    def __init__(self, host, port):
        self.logger = logging.getLogger("client")
        self.client_sockect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sockect.settimeout(2)

        try:
            self.client_sockect.connect((host,port))
        except:
            self.logger.error('Connection failed')
            sys.exit()

        self.logger.info("Connected to remote host.")
        self.prompt()

    
    def launch(self):

        while 1:
            rlist = [sys.stdin, self.client_sockect]
            read_list, write_list, error_list = select.select(rlist,[],[])

            for sock in read_list:
                if sock == self.client_sockect:
                    data = sock.recv(4096)
                    if not data:
                        self.logger.error("\nDisconnected from chat server")
                        sys.exit()
                    else:
                        sys.stdout.write(data)
                        self.prompt()

                else:
                    msg = sys.stdin.readline()
                    self.client_sockect.send(msg)
                    self.prompt()
    
    def prompt(self):
        sys.stdout.write('<You> ')
        sys.stdout.flush()

if __name__ == "__main__":

    host = sys.argv[1]
    port = int(sys.argv[2])

    cl = client(host, port)
    cl.launch()


