# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ChildrenForm.ui'
#
# Created: Tue Apr 16 19:26:53 2019
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ChirldrenForm(object):
    def setupUi(self, ChirldrenForm):
        ChirldrenForm.setObjectName("ChirldrenForm")
        ChirldrenForm.resize(353, 129)
        self.gridLayout = QtWidgets.QGridLayout(ChirldrenForm)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QtWidgets.QTextEdit(ChirldrenForm)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(ChirldrenForm)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(ChirldrenForm)
        self.buttonBox.accepted.connect(ChirldrenForm.accept)
        self.buttonBox.rejected.connect(ChirldrenForm.reject)
        QtCore.QMetaObject.connectSlotsByName(ChirldrenForm)

    def retranslateUi(self, ChirldrenForm):
        _translate = QtCore.QCoreApplication.translate
        ChirldrenForm.setWindowTitle(_translate("ChirldrenForm", "Dialog"))
        self.textEdit.setHtml(_translate("ChirldrenForm", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">魔镜魔镜,谁是世界上最帅的男生?</p></body></html>"))

