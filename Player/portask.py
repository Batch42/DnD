# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import playerwindow
import sys

mainwin = None

class Dialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setObjectName("Dialog")
        self.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(130, 130, 113, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit1 = QtWidgets.QLineEdit(self)
        self.lineEdit1.setGeometry(QtCore.QRect(130, 40, 113, 22))
        self.lineEdit1.setObjectName("lineEdit1")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(140, 90, 71, 16))
        self.label.setObjectName("label")self.label = QtWidgets.QLabel(self)
        self.label1 = QtWidgets.QLabel(self)
        self.label1.setGeometry(QtCore.QRect(140, 10, 71, 16))
        self.label1.setObjectName("label1")

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)
        
        self.show()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Enter Port:"))
        self.label.setText(_translate("Dialog", "Enter Name:"))

    def reject(self):
        sys.exit()

    def accept(self):
        global mainwin
        try:
            port=int(self.lineEdit.text())
            mainwin = playerwindow.PlayerWindow(name,port)
            self.hide()
        except Exception as ex:
            print(ex)
            return
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    d=Dialog()
    sys.exit(app.exec_())
