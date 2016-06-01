# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Login.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName(_fromUtf8("Login"))
        Login.resize(348, 229)
        self.gridLayout = QtGui.QGridLayout(Login)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_usr = QtGui.QLabel(Login)
        self.label_usr.setObjectName(_fromUtf8("label_usr"))
        self.horizontalLayout_3.addWidget(self.label_usr)
        self.edit_usr = QtGui.QLineEdit(Login)
        self.edit_usr.setObjectName(_fromUtf8("edit_usr"))
        self.horizontalLayout_3.addWidget(self.edit_usr)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_pwd = QtGui.QLabel(Login)
        self.label_pwd.setObjectName(_fromUtf8("label_pwd"))
        self.horizontalLayout_2.addWidget(self.label_pwd)
        self.edit_pwd = QtGui.QLineEdit(Login)
        self.edit_pwd.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText)
        self.edit_pwd.setEchoMode(QtGui.QLineEdit.Password)
        self.edit_pwd.setObjectName(_fromUtf8("edit_pwd"))
        self.horizontalLayout_2.addWidget(self.edit_pwd)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btn_signin = QtGui.QPushButton(Login)
        self.btn_signin.setObjectName(_fromUtf8("btn_signin"))
        self.horizontalLayout.addWidget(self.btn_signin)
        spacerItem = QtGui.QSpacerItem(98, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_signup = QtGui.QPushButton(Login)
        self.btn_signup.setObjectName(_fromUtf8("btn_signup"))
        self.horizontalLayout.addWidget(self.btn_signup)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        Login.setWindowTitle(_translate("Login", "Login", None))
        self.label_usr.setText(_translate("Login", "Username", None))
        self.label_pwd.setText(_translate("Login", "Password", None))
        self.btn_signin.setText(_translate("Login", "Sign in", None))
        self.btn_signup.setText(_translate("Login", "Sign up", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Login = QtGui.QDialog()
    ui = Ui_Login()
    ui.setupUi(Login)
    Login.show()
    sys.exit(app.exec_())

