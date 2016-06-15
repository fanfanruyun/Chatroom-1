# -*- coding: utf-8 -*-
import client
from PyQt4 import QtCore, QtGui, Qt
import ui_login, ui_mainwin
import sys


class Login(QtGui.QDialog, ui_login.Ui_Login):
    signal_sign_in = QtCore.pyqtSignal(str, str)
    signal_sign_up = QtCore.pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        #self.ui = Ui_Login()
        self.setupUi(self)
        self.btn_signin.clicked.connect(self.handle_sign_in)
        self.btn_signup.clicked.connect(self.handle_sign_up)

    def handle_sign_in(self):
        usr_name = self.edit_usr.text()
        pwd = self.edit_pwd.text()
        print usr_name,pwd
        self.signal_sign_in.emit(usr_name, pwd)

    def handle_sign_ret(self, flag):
        if flag:
            self.accept()
        else:
            self.errorAlert("Bad Username or Password.")

    def handle_sign_up(self):
        usr_name = self.edit_usr.text()
        pwd = self.edit_pwd.text()
        print usr_name, pwd
        self.signal_sign_up.emit(usr_name, pwd)


    def errorAlert(self, s):
        QtGui.QMessageBox.critical(self, u'error', s)
     

class ChatRoom(QtGui.QMainWindow, ui_mainwin.Ui_MainWindow):
    signal_chat = QtCore.pyqtSignal(str)
    signal_create_group = QtCore.pyqtSignal(str)
    signal_add_group = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(ChatRoom, self).__init__(parent)
        #self.ui = Ui_ChatRoom()
        self.setupUi(self)
        self.btn_send.clicked.connect(self.handle_send)
        self.btn_add.clicked.connect(self.handle_add)
        self.chat_target = None
        self.listWidget_2.itemClicked.connect(self.handle_item_act)
        self.listWidget.itemClicked.connect(self.handle_item_act2)
        self.is_pm = True

    def handle_item_act(self, item):
        self.label.setText("Talking to: " + item.text() + " [PM mode]")
        self.chat_target = str(item.text())
        self.is_pm = True

    def handle_item_act2(self, item):
        self.label.setText("Talking to: " + item.text() + " [Muticast mode]")
        self.chat_target = str(item.text())
        self.is_pm = False
        self.signal_add_group.emit(item.text())

    def handle_add(self):
        g_name = self.lineEdit.text()
        if g_name:
            self.signal_create_group.emit(g_name)


    def handle_send(self):
        if self.chat_target:
            txt = str(self.textEdit.toPlainText())
            if txt:
                self.textBrowser.setText(self.textBrowser.toPlainText() + "<Me:> " + txt + "\n")
                self.textEdit.setText("")
                if self.is_pm:
                    data = "@PM %s %s" %(self.chat_target, txt)
                    self.signal_chat.emit(data)
                else:
                    data = "@MC %s %s" %(self.chat_target, txt)
                    self.signal_chat.emit(data)
        else:
            self.errorAlert("No chat target")

    def handle_refresh_usrs(self, cur_usrs):
        self.listWidget_2.clear()
        usr_list = str(cur_usrs).strip().split()
        for usr in usr_list:
            self.listWidget_2.addItem(QtGui.QListWidgetItem(usr))
        self.label.setText("Talking to: None")
        self.chat_target = None

    def handle_msg_arrive(self, msg):
        self.textBrowser.setText(self.textBrowser.toPlainText() + msg + '\n')

    def handle_refresh_groups(self, cur_group):
        self.listWidget.clear()
        group_list = str(cur_group).strip().split()
        for g in group_list:
            self.listWidget.addItem(QtGui.QListWidgetItem(g))
        self.label.setText("Talking to: None")
        self.chat_target = None


    def errorAlert(self, s):
        QtGui.QMessageBox.critical(self, u'error', s)
# ------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    cln = client.Client("127.0.0.1", 5000)
    cln.ehelo()
    login = Login()
    chatroom = ChatRoom()
    login.signal_sign_in.connect(cln.sign_in)
    login.signal_sign_up.connect(cln.sign_up)
    cln.signal_vlidate.connect(login.handle_sign_ret)
    cln.signal_usr_need_refresh.connect(chatroom.handle_refresh_usrs)
    cln.signal_msg_arrive.connect(chatroom.handle_msg_arrive)
    cln.signal_group_need_refresh.connect(chatroom.handle_refresh_groups)
    chatroom.signal_chat.connect(cln.send)
    chatroom.signal_create_group.connect(cln.create_group)
    chatroom.signal_add_group.connect(cln.add_group)
    app.aboutToQuit.connect(cln.quit)
    if login.exec_() == QtGui.QDialog.Accepted:
        cln.start()
        cln.get_current_user()
        cln.get_current_group()
        chatroom.show()
        sys.exit(app.exec_())


