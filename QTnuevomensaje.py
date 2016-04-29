# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nuevomensaje.ui'
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

class Ui_DialogNuevoMensaje(object):
    def setupUi(self, DialogNuevoMensaje):
        DialogNuevoMensaje.setObjectName(_fromUtf8("DialogNuevoMensaje"))
        DialogNuevoMensaje.resize(329, 211)
        DialogNuevoMensaje.setMinimumSize(QtCore.QSize(329, 211))
        DialogNuevoMensaje.setMaximumSize(QtCore.QSize(329, 211))
        self.buttonBox = QtGui.QDialogButtonBox(DialogNuevoMensaje)
        self.buttonBox.setGeometry(QtCore.QRect(150, 172, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.plainTextEdit_Mensaje = QtGui.QPlainTextEdit(DialogNuevoMensaje)
        self.plainTextEdit_Mensaje.setGeometry(QtCore.QRect(20, 52, 291, 111))
        self.plainTextEdit_Mensaje.setObjectName(_fromUtf8("plainTextEdit_Mensaje"))
        self.lineEdit_NumeroTelefonico = QtGui.QLineEdit(DialogNuevoMensaje)
        self.lineEdit_NumeroTelefonico.setGeometry(QtCore.QRect(120, 10, 191, 20))
        self.lineEdit_NumeroTelefonico.setObjectName(_fromUtf8("lineEdit_NumeroTelefonico"))
        self.labelTextoNumTelefonico = QtGui.QLabel(DialogNuevoMensaje)
        self.labelTextoNumTelefonico.setGeometry(QtCore.QRect(20, 14, 111, 16))
        self.labelTextoNumTelefonico.setObjectName(_fromUtf8("labelTextoNumTelefonico"))
        self.label_TextoCaracteres = QtGui.QLabel(DialogNuevoMensaje)
        self.label_TextoCaracteres.setGeometry(QtCore.QRect(22, 178, 61, 16))
        self.label_TextoCaracteres.setObjectName(_fromUtf8("label_TextoCaracteres"))
        self.label_Caracteres = QtGui.QLabel(DialogNuevoMensaje)
        self.label_Caracteres.setGeometry(QtCore.QRect(80, 179, 47, 13))
        self.label_Caracteres.setObjectName(_fromUtf8("label_Caracteres"))
        self.label_TextoMensaje = QtGui.QLabel(DialogNuevoMensaje)
        self.label_TextoMensaje.setGeometry(QtCore.QRect(270, 33, 41, 16))
        self.label_TextoMensaje.setObjectName(_fromUtf8("label_TextoMensaje"))

        self.retranslateUi(DialogNuevoMensaje)
        QtCore.QMetaObject.connectSlotsByName(DialogNuevoMensaje)
        DialogNuevoMensaje.setTabOrder(self.lineEdit_NumeroTelefonico, self.plainTextEdit_Mensaje)

    def retranslateUi(self, DialogNuevoMensaje):
        DialogNuevoMensaje.setWindowTitle(_translate("DialogNuevoMensaje", "New SMS", None))
        self.labelTextoNumTelefonico.setText(_translate("DialogNuevoMensaje", "Movil", None))
        self.label_TextoCaracteres.setText(_translate("DialogNuevoMensaje", "Chararter", None))
        self.label_Caracteres.setText(_translate("DialogNuevoMensaje", "Max. Len 160", None))
        self.label_TextoMensaje.setText(_translate("DialogNuevoMensaje", "SMS", None))

