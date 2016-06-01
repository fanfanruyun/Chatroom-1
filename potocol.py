# -*- coding: utf-8 -*-
class Potocol:
    def resolve(self, data):
        if data[0:8] == "@sign_in":
            op, usr_id, usr_pwd = data.split(' ', 2)
            return 1, (usr_id, usr_pwd)
        elif data[0:8] == "@sign_up":
            op, usr_id, usr_pwd = data.split(' ', 2)
            return 2, (usr_id, usr_pwd)
        elif data[0:3] == "@PM":
            op, to, msg = data.split(' ', 2)
            return 3, (to, msg)
        elif data[0:3] == "@UL":
            return 4, ()
        elif data[0:3] == "@EX":
            return 5, ()
        elif data[0:3] == "@GC":
            op, g_name = data.split(' ', 1)
            print "g_name" + g_name
            return 6, (g_name)
        elif data[0:3] == "@AG":
            op, g_name = data.split(' ', 1)
            return 7, (g_name)
        elif data[0:3] == "@MC":
            op, g_name, msg = data.split(' ', 2)
            return 8, (g_name, msg)
        elif data[0:3] == "@GL":
            return 9, ()
        else:
            return 0, ()
       #elif data[0:3] == "@GC":
          #op, g_name = data.strip().split(' ', 1)
          #mc_ip = self.generate_ip()
          #self.group_tb[g_name] = mc_ip
          #print self.group_tb[g_name]
          #self.group_mems_tb[g_name] = [user_id]
          #self.group_belong_tb[user_id] = g_name
          #self.forward(user_id, "@AD "+mc_ip)
      #elif data[0:3] == "@AG":
          #op, g_name = data.strip().split(' ', 1)
          #mc_ip = self.group_tb[g_name]
          #self.group_mems_tb[g_name].append(user_id)
          #self.group_belong_tb[user_id] = g_name
          #self.forward(user_id, "@AD "+mc_ip)
      #elif data[0:3] == "@MC":
          #op, g_name, msg = data.strip().split(' ', 2)
          #mc_ip = self.group_tb[g_name]
          #print mc_ip, g_name
          #if (msg):
              #self.udp_socket.sendto(msg,(mc_ip,self.group_port))
