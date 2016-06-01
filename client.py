# -*- coding: utf-8 -*-
import socket,select,sys,logging
from PyQt4 import QtCore
import threading
logging.basicConfig(level=logging.DEBUG)

class Client(QtCore.QObject, threading.Thread):
    signal_vlidate = QtCore.pyqtSignal(bool)
    signal_msg_arrive = QtCore.pyqtSignal(str)
    signal_usr_need_refresh = QtCore.pyqtSignal(str)
    signal_group_need_refresh = QtCore.pyqtSignal(str)

    def __init__(self, host, port):
        QtCore.QObject.__init__(self)
        threading.Thread.__init__(self)
        self.logger = logging.getLogger("client")
        self.client_sockect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sockect.settimeout(2)

        self.host = host
        self.port = port
        self.group_port = 1600
        self.is_sign_in = False
        self.is_added_group = False
        self.running = True

        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.udp_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.udp_socket.bind(('0.0.0.0',self.group_port))
        self.udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)


        self.logger.info("Connected to remote host.")
        #self.prompt()

    def _px(self, _data):
        ret = _data.split("@")
        ret = map(lambda x: "@" + x.strip(), ret)
        return ret[1:]

     # I can't understand why!!!!!!!!!!!!!!!!!!!!!
    def _wtf(self, d):
        return filter(lambda x: ord(x) != 0, d)

    def quit(self):
        self.running = False
        self.send("@EX")

    def ehelo(self):
        try:
            self.client_sockect.connect((self.host,self.port))
        except:
            self.logger.error('Connection failed')
            sys.exit()

    def sign_in(self, usr_name, pwd):
        self.client_sockect.send("@sign_in "+ str(usr_name) + " " + str(pwd))
        ret = self.client_sockect.recv(4096).strip()
        print ret
        if ret.strip() == "@success":
            self.is_sign_in = True
        self.signal_vlidate.emit(self.is_sign_in)
    
    def sign_up(self, usr_name, pwd):
        self.client_sockect.send("@sign_up "+ usr_name + " " + pwd)
        ret = self.client_sockect.recv(4096)
        if ret.strip() == "@success":
            self.is_sign_in = True
        self.signal_vlidate.emit(self.is_sign_in)

    def get_current_user(self):
        self.client_sockect.send("@UL")
        
    def update_user_list(self, info):
        self.signal_usr_need_refresh.emit(info.strip())

    def get_current_group(self):
        self.client_sockect.send("@GL")

    def update_group_list(self, info):
        self.signal_group_need_refresh.emit(info.strip())

    def create_group(self, g_name):
        self.client_sockect.send("@GC " + g_name)

    def add_group(self, g_name):
        self.client_sockect.send("@AG " + g_name)
    
    def send(self, msg):
        #print "try to send"
        self.client_sockect.send(msg)
    
    def run(self):
        while self.running:
            rlist = [self.client_sockect,sys.stdin, self.udp_socket]
            read_list, write_list, error_list = select.select(rlist,[],[])
            for sock in read_list:
                if sock == self.client_sockect:
                    _data = '@'
                    try:
                        _data = sock.recv(4096)
                    except:
                        pass
                    _data = self._wtf(_data)
                    reqs = self._px(_data)
                    for data in reqs:
                        print data
                        if not data:
                            self.logger.error("\nDisconnected from chat server")
                            sys.exit()
                        elif data.strip() == "@usrs_need_refresh":
                            self.get_current_user()
                            self.get_current_group()
                        elif data[0:3] == "@UL":
                            info = data[4:]
                            self.update_user_list(info)
                        elif data[0:3] == "@AD":
                            op, mc_ip = data.split(' ', 1)
                            if not self.is_added_group:
                                self.is_added_group = True
                                status = self.udp_socket.setsockopt(socket.IPPROTO_IP,
                                                     socket.IP_ADD_MEMBERSHIP, 
                                                     socket.inet_aton(mc_ip) + socket.inet_aton('0.0.0.0'));
                            else:
                                status = self.udp_socket.setsockopt(socket.IPPROTO_IP,
                                                     socket.IP_DROP_MEMBERSHIP, 
                                                     socket.inet_aton(self.cur_mc_ip) + socket.inet_aton('0.0.0.0'));
                                status = self.udp_socket.setsockopt(socket.IPPROTO_IP,
                                                     socket.IP_ADD_MEMBERSHIP, 
                                                     socket.inet_aton(mc_ip) + socket.inet_aton('0.0.0.0'));
                            self.cur_mc_ip = mc_ip
                        elif data[0:3] == "@GL":
                            info = data[4:]
                            self.update_group_list(info)

                        elif data[0:5] == "@data":
                            print "### " + data
                            self.signal_msg_arrive.emit(data[6:])
                            #sys.stdout.write(data)
                            #self.prompt()
                elif sock == self.udp_socket:
                    data = sock.recv(4096) 
                    self.signal_msg_arrive.emit(data[6:])
                    #sys.stdout.write(data)
                    #self.prompt()
                else:
                    msg = sys.stdin.readline()
                    self.client_sockect.send(msg)
                    #self.prompt()
    
    def prompt(self):
        sys.stdout.write('<You> ')
        sys.stdout.flush()

if __name__ == "__main__":

    host = "127.0.0.1"
    port = 5000
    cl = Client(host, port)
    cl.ehelo()
    cl.sign_in("mengke","123456")
    cl.start()
    


