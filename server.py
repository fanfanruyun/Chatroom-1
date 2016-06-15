# -*- coding: utf-8 -*-
import socket, select, logging, sys
import cPickle as pickle
import random
import potocol
logging.basicConfig(level=logging.DEBUG)

class server:
    def __init__(self):
        self._connect_list = []
        self.logger = logging.getLogger("server")
        self.pt = potocol.Potocol()

        self.RECV_BUFFER = 4096
        self.PORT = 5000
        self.HOST = "0.0.0.0"
        self.UDP_PORT = 1501
        self.group_port = 1600

        try:
            self.users = pickle.load(open("usrs.dat", "rb"))
        except:
            self.users = []
        self.sock_2_name = {}
        self.running = True

        self.group_tb = {}
        self.group_mems_tb = {}
        self.group_belong_tb = {}
        self.mc_ip_in_use = []

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.HOST,self.PORT))
        self.server_socket.listen(10)

        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) 
        self.udp_socket.bind((self.HOST, self.UDP_PORT)) 
        self.udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255) 

        self._connect_list.append(self.server_socket)
        self._connect_list.append(sys.stdin)
        self._func_list = [self.error_msg, self.sign_in, self.sign_up, self.pensonal_chat, self.list_users, self.client_quit,
                self.create_group, self.add_group, self.muticast_msg, self.list_group]
        #self._connect_list.append(self.udp_socket)

    def __del__(self):
        pickle.dump(self.users, open("usrs.dat", "wb"), True)


    def _px(self, _data):
        ret = _data.split("@")
        ret = map(lambda x: "@" + x.strip(), ret)
        return ret[1:]
    
    # I can't understand why!!!!!!!!!!!!!!!!!!!!!
    def _wtf(self, d):
        return filter(lambda x: ord(x) != 0, d)

    # potocol 0
    def error_msg(self, args, who):
        #print "error msg type."
        #self.logger.error("unreadable potocol type")
        pass
    
    # potocol 1
    def sign_in(self, args, who):
        def func(usr_id, usr_pwd):
            for x,y in self.users:
                if x == usr_id and y == usr_pwd:
                    return True, "@success"
            return False, "@no match"
        usr_id, usr_pwd = args
        jud = func(usr_id, usr_pwd)
        if jud[0]:
            self.sock_2_name[who] = usr_id
            self.logger.info("%s signed in\n" %usr_id)
            who.send("@success\n")
            self.broadcast(who, "@usrs_need_refresh\n")
        else:
            who.send(jud[1])

    # potocol 2
    def sign_up(self, args, who):
        def func(usr_id, usr_pwd):
            for x,y in self.users:
                if x == usr_id:
                    return False, "@conflict"
            self.users.append((usr_id, usr_pwd))
            return True, "@success"
        usr_id, usr_pwd = args
        jud = func(usr_id, usr_pwd)
        if jud[0]:
            self.sock_2_name[who] = usr_id
            self.logger.info("%s signed up\n" %usr_id)
            who.send("@success\n")
            self.broadcast(who, "@usrs_need_refresh\n")
        else:
            who.send(jud[1])

    # potocal 3
    def pensonal_chat(self, args, who):
        to, msg = args
        print to, msg
        if msg:
            self.forward(to, '@data <'+str(self.sock_2_name[who])+':> ' + msg+ "\n")

    # potpcol 4
    def list_users(self, args, who):
        ret = self.cmd_list_users()
        self.forward(self.sock_2_name[who], "@UL "+" ".join(ret) + "\n")
    
    # potocol 5
    def client_quit(self, args, who):
        self.broadcast(who, "@usrs_need_refresh\n")
        self.logger.info("Client %s is offline" % self.sock_2_name[who])
        who.close()
        self._connect_list.remove(who)
        del self.sock_2_name[who]

    # potocol 6
    def create_group(self, args, who):
        g_name = args
        usr_id = self.sock_2_name[who]
        mc_ip = self.generate_ip()
        self.group_tb[g_name] = mc_ip
        self.group_mems_tb[g_name] = [usr_id]
        self.group_belong_tb[usr_id] = g_name
        self.forward(usr_id, "@AD " + mc_ip + "\n")
        self.broadcast(who, "@usrs_need_refresh\n")
        self.forward(usr_id, "@usrs_need_refresh\n")

    #Potocol 7
    def add_group(self, args, who):
        g_name = args
        usr_id = self.sock_2_name[who]
        # if have ?
        mc_ip = self.group_tb[g_name]
        if usr_id in self.group_belong_tb:
            if g_name == self.group_belong_tb[usr_id]:
                return
            old_g_name = self.group_belong_tb[usr_id]
            tmp = self.group_mems_tb[old_g_name]
            tmp.remove(usr_id)
            if tmp:
                self.group_mems_tb[old_g_name] = tmp
            else:
                del self.group_mems_tb[old_g_name]
                self.mc_ip_in_use.remove(self.group_tb[old_g_name])
                del self.group_tb[old_g_name]
            self.group_belong_tb[usr_id] = g_name
            self.group_mems_tb[g_name].append(usr_id)
            self.forward(usr_id, "@AD " + mc_ip + "\n")
        

    #potocol 8
    def muticast_msg(self, args, who):
        g_name, msg = args
        mc_ip = self.group_tb[g_name]
        if (msg):
            self.udp_socket.sendto('@data <'+str(self.sock_2_name[who])+r'/'+g_name+':> ' + msg, (mc_ip,self.group_port))

    #potocol 9
    def list_group(self, args, who):
        ret = self.cmd_list_group()
        self.forward(self.sock_2_name[who], "@GL "+" ".join(ret) + "\n")

    def cmd_list_users(self):
        ret = []
        for key, value in self.sock_2_name.items():
            ret.append(value)
        return ret

    def cmd_list_group(self):
        ret = []
        for g_name, mc_ip in self.group_tb.items():
            ret.append(g_name)
        return ret

    def cmd_op(self, op):
        if op == "users":
            user_list = self.cmd_list_users()
            for item in user_list:
                print "[%s]"% item
        elif op == "quit":
            self.running = False
        elif op == "group":
            group_list = self.cmd_list_group()
            for item in group_list:
                print "[%s]" % item

                

    def generate_ip(self):
        a = random.randint(225,238)
        b = random.randint(0,255)
        c = random.randint(0,255)
        d = random.randint(0,255)
        x = str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d)
        if x in self.mc_ip_in_use:
            self.generate_ip()
        else:
            self.mc_ip_in_use.append(x)
            return x

    def launch(self):
        self.logger.info("Server launched on port" + str(self.PORT))

        while self.running:
            read_sockets,write_sockets,error_sockets = select.select(self._connect_list,[],[])

            for sock in read_sockets:
                if sock == sys.stdin:
                    op = sys.stdin.readline().strip()
                    self.cmd_op(op)
                    
                elif sock == self.server_socket:
                    sockfd, addr = sock.accept()
                    self._connect_list.append(sockfd)
                    self.logger.info("Client (%s,%s) connected"% addr)
                    #sockfd.send("Login please.\n")
                    #self.broadcast(sockfd, "[%s,%s] entered room\n" %addr)

                else:
                    try:
                        _data = sock.recv(self.RECV_BUFFER)
                        _data = self._wtf(_data)
                        reqs = self._px(_data)
                        for data in reqs:
                            print data
                            index, args = self.pt.resolve(data)
                            if sock not in self.sock_2_name and index not in [1, 2]:
                                #sock.send("Login please!\n")
                                pass
                            else:
                                self._func_list[index](args, sock)
                    except socket.error, e:
                        print e
                        if sock in self.sock_2_name:
                            sock.close()
                            self._connect_list.remove(sock)
                            self.broadcast(sock, "@usrs_need_refresh\n")
                            self.logger.info("Client %s is offline" % self.sock_2_name[sock])
                            del self.sock_2_name[sock]
                        continue
        self.server_socket.close()

    def broadcast(self, sock, msg):
        for socket in self._connect_list:
            if socket != self.server_socket and socket != sock and socket != sys.stdin and socket != self.udp_socket:
                try:
                    #name = socket.getpeername()
                    if socket in self.sock_2_name:
                        socket.send(msg)
                except:
                    print "should not be here"
                    socket.close()
                    self._connect_list.remove(socket)

    def forward (self, to, msg):
        tmp = ""
        for key, value in self.sock_2_name.items():
            if to == value:
                tmp = key
                break
        for socket in self._connect_list:
            if socket != self.server_socket and socket != self.udp_socket and socket != sys.stdin:
                if socket == tmp:
                    try:
                        socket.send(msg)
                    except:
                        print "should not be here 3"
                        socket.close()
                        self._connect_list.remove(socket)
                    break

if __name__ == '__main__':
    sv = server()
    sv.launch()
