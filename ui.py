# -*- coding:utf8 -*-

import sys, time, os
from PyQt4 import QtGui, QtCore

class chatView(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.parent = parent
        self.initLayout()

    def initLayout(self):

        self.ipLable = QtGui.QLabel(u'IP address')
