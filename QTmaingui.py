# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'maingui.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(1042, 670)
        MainWindow.setMinimumSize(QtCore.QSize(16777215, 16777215))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        MainWindow.setMouseTracking(False)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtGui.QTabWidget.Rounded)
        self.centralwidget = QtGui.QWidget(MainWindow)
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        #Cuadro de Cola de Mensajes
        self.tableWidget_Cola = QtGui.QTableWidget(self.centralwidget)
        SendLeft = 10
        SendTop = 20
        SendWidth = (resolution.width()*30)/100
        SendHeight = (resolution.height()*45)/100
        self.tableWidget_Cola.setGeometry(QtCore.QRect(SendLeft, SendTop, SendWidth, SendHeight))
        self.tableWidget_Cola.setObjectName(_fromUtf8("tableWidget_Cola"))
        self.tableWidget_Cola.setColumnCount(5)
        self.tableWidget_Cola.setRowCount(0)
        self.tableWidget_Cola.setHorizontalHeaderLabels(("Company","Code","Movil","SMS","Date"))
        self.tableWidget_Cola.setColumnWidth(0,0)
        self.tableWidget_Cola.setColumnWidth(1,0)
        self.tableWidget_Cola.setColumnWidth(2,(SendWidth*30)/100)
        self.tableWidget_Cola.setColumnWidth(3,(SendWidth*69)/100)
        self.tableWidget_Cola.setColumnWidth(4,0)
        self.tableWidget_Cola.verticalHeader().setVisible(False)
        self.tableWidget_Cola.setShowGrid(False)
        self.tableWidget_Cola.setAlternatingRowColors(True)
        
        self.label_ColaMensajes = QtGui.QLabel(self.centralwidget)
        self.label_ColaMensajes.setGeometry(QtCore.QRect(SendLeft, SendTop-15, 91, 16))
        self.label_ColaMensajes.setObjectName(_fromUtf8("label_ColaMensajes"))

        
        self.label_Informacion = QtGui.QLabel(self.centralwidget)
        self.label_Informacion.setGeometry(QtCore.QRect(700, 395, 151, 16))
        self.label_Informacion.setObjectName(_fromUtf8("label_Informacion"))
        #Cuadro de Mensajes Enviados
        self.tableWidget_Enviados = QtGui.QTableWidget(self.centralwidget)
        Top = SendTop
        Left = SendWidth+20
        Width = (resolution.width()*68)/100
        
        self.tableWidget_Enviados.setGeometry(QtCore.QRect(Left, Top, Width, SendHeight))
        self.tableWidget_Enviados.setObjectName(_fromUtf8("tableWidget_Enviados"))
        self.tableWidget_Enviados.setColumnCount(5)
        self.tableWidget_Enviados.setRowCount(0)
        self.tableWidget_Enviados.setHorizontalHeaderLabels(("Company","Code","Movil","SMS","Date"))
        self.tableWidget_Enviados.setColumnWidth(0,(Width*10)/100)
        self.tableWidget_Enviados.setColumnWidth(1,(Width*10)/100)
        self.tableWidget_Enviados.setColumnWidth(2,(Width*20)/100)
        self.tableWidget_Enviados.setColumnWidth(3,(Width*40)/100)
        self.tableWidget_Enviados.setColumnWidth(4,(Width*19)/100)
        self.tableWidget_Enviados.verticalHeader().setVisible(False)
        self.tableWidget_Enviados.setShowGrid(False)
        self.tableWidget_Enviados.setAlternatingRowColors(True)

        self.label_MensajesEnviados = QtGui.QLabel(self.centralwidget)
        self.label_MensajesEnviados.setGeometry(QtCore.QRect(Left, Top-15, 101, 16))
        self.label_MensajesEnviados.setObjectName(_fromUtf8("label_MensajesEnviados"))

        
        self.tableWidget_Fallidos = QtGui.QTableWidget(self.centralwidget)

        #geometry = self.desktop().availableGeometry()
        
        FailHeight = (resolution.height()*20)/100
        self.tableWidget_Fallidos.setGeometry(QtCore.QRect(SendLeft, SendHeight+45, SendWidth, FailHeight))        
        self.tableWidget_Fallidos.setObjectName(_fromUtf8("tableWidget_Fallidos"))
        self.tableWidget_Fallidos.setColumnCount(5)
        self.tableWidget_Fallidos.setRowCount(0)
        self.tableWidget_Fallidos.setHorizontalHeaderLabels(("Company","Code","Movil","SMS","Date"))
        self.tableWidget_Fallidos.setColumnWidth(0,0)
        self.tableWidget_Fallidos.setColumnWidth(1,0)
        self.tableWidget_Fallidos.setColumnWidth(2,(SendWidth*25)/100)
        self.tableWidget_Fallidos.setColumnWidth(3,(SendWidth*45)/100)
        self.tableWidget_Fallidos.setColumnWidth(4,(SendWidth*29)/100)
        self.tableWidget_Fallidos.verticalHeader().setVisible(False)
        self.tableWidget_Fallidos.setShowGrid(False)
        self.tableWidget_Fallidos.setAlternatingRowColors(True)

        self.label_MensajesFallidos = QtGui.QLabel(self.centralwidget)
        self.label_MensajesFallidos.setGeometry(QtCore.QRect(SendLeft, SendHeight+30, 151, 16))
        self.label_MensajesFallidos.setObjectName(_fromUtf8("label_MensajesFallidos"))

                
        self.label_TextoTotalEnviados = QtGui.QLabel(self.centralwidget)
        self.label_TextoTotalEnviados.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.label_TextoTotalEnviados.setObjectName(_fromUtf8("label_TextoTotalEnviados"))
        self.label_TextoTotalCola = QtGui.QLabel(self.centralwidget)
        self.label_TextoTotalCola.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.label_TextoTotalCola.setObjectName(_fromUtf8("label_TextoTotalCola"))
        self.label_TotalCola = QtGui.QLabel(self.centralwidget)
        self.label_TotalCola.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.label_TotalCola.setObjectName(_fromUtf8("label_TotalCola"))
        self.label_TotalEnviados = QtGui.QLabel(self.centralwidget)
        self.label_TotalEnviados.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.label_TotalEnviados.setObjectName(_fromUtf8("label_TotalEnviados"))
        
        self.tableWidget_Recibidos = QtGui.QTableWidget(self.centralwidget)
        SendWidth = (resolution.width()*68)/100       
        self.tableWidget_Recibidos.setGeometry(QtCore.QRect(Left, SendHeight+45, SendWidth, FailHeight))
        self.tableWidget_Recibidos.setObjectName(_fromUtf8("tableWidget_Recibidos"))
        self.tableWidget_Recibidos.setColumnCount(3)
        self.tableWidget_Recibidos.setRowCount(0)
        self.tableWidget_Recibidos.setHorizontalHeaderLabels(("Movil","SMS","Date"))
        self.tableWidget_Recibidos.setColumnWidth(0,(SendWidth*18)/100)
        self.tableWidget_Recibidos.setColumnWidth(1,(SendWidth*60)/100)
        self.tableWidget_Recibidos.setColumnWidth(2,(SendWidth*21)/100)
        
        self.tableWidget_Recibidos.verticalHeader().setVisible(False)
        self.tableWidget_Recibidos.setShowGrid(False)
        self.tableWidget_Recibidos.setAlternatingRowColors(True)
        
        self.label_MensajesRecibidos = QtGui.QLabel(self.centralwidget)
        self.label_MensajesRecibidos.setGeometry(QtCore.QRect(Left, SendHeight+30, 151, 16))
        self.label_MensajesRecibidos.setObjectName(_fromUtf8("label_MensajesRecibidos"))

        Diferencia = 230
        

        Diferencia = Diferencia + 25

        self.progressBar_Bateria = QtGui.QProgressBar(self.centralwidget)
        self.progressBar_Bateria.setGeometry(QtCore.QRect(Left+SendWidth+100, SendHeight+Diferencia, 0, 23))
        self.progressBar_Bateria.setProperty("value", 0)
        self.progressBar_Bateria.setObjectName(_fromUtf8("progressBar_Bateria"))
        self.label_TextoBateria = QtGui.QLabel(self.centralwidget)
        self.label_TextoBateria.setGeometry(QtCore.QRect(Left+SendWidth+20, SendHeight+Diferencia+3, 0, 16))
        self.label_TextoBateria.setObjectName(_fromUtf8("label_TextoBateria"))
        
        Diferencia = Diferencia + 25
        self.label_TextoOperadora = QtGui.QLabel(self.centralwidget)
        self.label_TextoOperadora.setGeometry(QtCore.QRect(Left+SendWidth+20, SendHeight+Diferencia, 0, 16))
        self.label_TextoOperadora.setObjectName(_fromUtf8("label_TextoOperadora"))
        self.label_Operadora = QtGui.QLabel(self.centralwidget)
        self.label_Operadora.setGeometry(QtCore.QRect(Left+SendWidth+100, SendHeight+Diferencia, 0, 16))
        self.label_Operadora.setObjectName(_fromUtf8("label_Operadora"))

        Diferencia = Diferencia + 25        
        self.label_TextoModo = QtGui.QLabel(self.centralwidget)
        self.label_TextoModo.setGeometry(QtCore.QRect(Left+SendWidth+20, SendHeight+Diferencia, 0, 16))
        self.label_TextoModo.setObjectName(_fromUtf8("label_TextoModo"))
        self.label_Modo = QtGui.QLabel(self.centralwidget)
        self.label_Modo.setGeometry(QtCore.QRect(Left+SendWidth+100, SendHeight+Diferencia, 0, 16))
        self.label_Modo.setObjectName(_fromUtf8("label_Modo"))
        
        Diferencia = Diferencia + 25    
        self.label_TextoEstado = QtGui.QLabel(self.centralwidget)
        self.label_TextoEstado.setGeometry(QtCore.QRect(Left+SendWidth+20, SendHeight+Diferencia, 0, 16))
        self.label_TextoEstado.setObjectName(_fromUtf8("label_TextoEstado"))
        self.label_Estado = QtGui.QLabel(self.centralwidget)
        self.label_Estado.setGeometry(QtCore.QRect(Left+SendWidth+100, SendHeight+Diferencia, 0, 16))
        self.label_Estado.setObjectName(_fromUtf8("label_Estado"))

        Diferencia = Diferencia + 25 
        self.label_TextoApertura = QtGui.QLabel(self.centralwidget)
        self.label_TextoApertura.setGeometry(QtCore.QRect(Left+SendWidth+20, SendHeight+Diferencia, 0, 16))
        self.label_TextoApertura.setObjectName(_fromUtf8("label_TextoApertura"))        
        self.label_FechaApertura = QtGui.QLabel(self.centralwidget)
        self.label_FechaApertura.setGeometry(QtCore.QRect(Left+SendWidth+100, SendHeight+Diferencia, 0, 16))
        self.label_FechaApertura.setObjectName(_fromUtf8("label_FechaApertura"))

        
        self.label_Consola = QtGui.QLabel(self.centralwidget)
        self.label_Consola.setGeometry(QtCore.QRect(0, 0, 0, 0)) #No lo muestro es el titulo de la consola....
        self.label_Consola.setObjectName(_fromUtf8("label_Consola"))
        #Consola de Log Jhonattan Ramirez
        SendWidth2 = (resolution.width()*99)/100
        CmdHeight = (resolution.width()*7)/100
        self.plainTextEdit_Consola = QtGui.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_Consola.setGeometry(QtCore.QRect(SendLeft, SendHeight+230, SendWidth2, CmdHeight))
        self.plainTextEdit_Consola.setReadOnly(True)
        self.plainTextEdit_Consola.setObjectName(_fromUtf8("plainTextEdit_Consola"))
        self.plainTextEdit_Consola.setMaximumBlockCount(100)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1042, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuOpciones = QtGui.QMenu(self.menubar)
        self.menuOpciones.setObjectName(_fromUtf8("menuOpciones"))
        self.menuA_adir = QtGui.QMenu(self.menubar)
        self.menuA_adir.setObjectName(_fromUtf8("menuA_adir"))
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        
        Top2 = 2 #(resolution.height()*5)/100
        self.progressBar_Senal = QtGui.QProgressBar(self.centralwidget)
        self.progressBar_Senal.setGeometry(QtCore.QRect(Left+SendWidth-((SendWidth*20)/100), Top2, (SendWidth*20)/100, 17))
        self.progressBar_Senal.setMaximum(31)
        self.progressBar_Senal.setProperty("value", 0)
        self.progressBar_Senal.setObjectName(_fromUtf8("progressBar_Senal"))
        
        self.label_TextoSenal = QtGui.QLabel(self.centralwidget)
        self.label_TextoSenal.setGeometry(QtCore.QRect(Left+SendWidth+20, SendHeight+Diferencia+3, 0, 16))
        self.label_TextoSenal.setObjectName(_fromUtf8("label_TextoSenal"))
        
        
        self.actionConfiguracion = QtGui.QAction(MainWindow)
        self.actionConfiguracion.setObjectName(_fromUtf8("actionConfiguracion"))
        self.actionNuevo_Mensaje = QtGui.QAction(MainWindow)
        self.actionNuevo_Mensaje.setObjectName(_fromUtf8("actionNuevo_Mensaje"))
        self.actionNueva_Cola_de_Mensajes = QtGui.QAction(MainWindow)
        self.actionNueva_Cola_de_Mensajes.setObjectName(_fromUtf8("actionNueva_Cola_de_Mensajes"))
        self.menuOpciones.addSeparator()
        self.menuOpciones.addAction(self.actionConfiguracion)
        self.menuA_adir.addAction(self.actionNuevo_Mensaje)
        self.menuA_adir.addAction(self.actionNueva_Cola_de_Mensajes)
        self.menubar.addAction(self.menuA_adir.menuAction())
        self.menubar.addAction(self.menuOpciones.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Soluciones SMS (www.soluciones-sms.com)", None))
        self.label_MensajesFallidos.setText(_translate("MainWindow", "SMS Fail", None))
        self.label_Informacion.setText(_translate("MainWindow", "Information", None))
        self.label_MensajesEnviados.setText(_translate("MainWindow", "Send Messages", None))
        self.label_TextoSenal.setText(_translate("MainWindow", "Signal", None))
        self.label_TextoBateria.setText(_translate("MainWindow", "Batery", None))
        self.label_TextoOperadora.setText(_translate("MainWindow", "", None))
        self.label_Operadora.setText(_translate("MainWindow", "---------------", None))
        self.label_TextoModo.setText(_translate("MainWindow", "Modo", None))
        self.label_Modo.setText(_translate("MainWindow", "---------------", None))
        self.label_TextoEstado.setText(_translate("MainWindow", "State", None))
        self.label_TextoApertura.setText(_translate("MainWindow", "Abierto desde", None))
        self.label_Estado.setText(_translate("MainWindow", "---------------", None))
        self.label_FechaApertura.setText(_translate("MainWindow", "---------------", None))
        self.label_ColaMensajes.setText(_translate("MainWindow", "SMS Sending", None))
        self.label_TextoTotalEnviados.setText(_translate("MainWindow", "", None))
        self.label_TextoTotalCola.setText(_translate("MainWindow", "", None))
        self.label_TotalCola.setText(_translate("MainWindow", "0", None))
        self.label_TotalEnviados.setText(_translate("MainWindow", "0", None))
        self.label_MensajesRecibidos.setText(_translate("MainWindow", "Incoming Messages", None))
        self.label_Consola.setText(_translate("MainWindow", "Consola", None))
        self.menuOpciones.setTitle(_translate("MainWindow", "Options", None))
        self.menuA_adir.setTitle(_translate("MainWindow", "Add", None))
        self.actionConfiguracion.setText(_translate("MainWindow", "Configuracion", None))
        self.actionNuevo_Mensaje.setText(_translate("MainWindow", "New SMS", None))
        self.actionNueva_Cola_de_Mensajes.setText(_translate("MainWindow", "Exit", None))

