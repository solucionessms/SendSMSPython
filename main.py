#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import openpyxl
os.system("color 1f")
os.system("title Consola Modem                           ##NO CERRAR##")
from PyQt4 import QtGui, QtCore
from QTmaingui import Ui_MainWindow
from QTnuevomensaje import Ui_DialogNuevoMensaje
from check import LicCheck
from openinfo import AvisodeApertura
from bd import BasedeDatos
from Device import Modem_EnforaSerial, Modem_HuaweiUSB
import serial, time, sys
from date import LaFecha
from Servidor import HiloServer
from Cliente import HiloCliente
from getsms import GetSMSBD
import globalvars
from formato import Validar
from numadmins import NumAdminsObjeto
import traceback
from guardarlog import GuardarTXTObjeto

#Arranque de las variables globales.
globalvars.initvars()

class NuevoMensaje(QtGui.QDialog):
	def __init__(self,parent):
		QtGui.QDialog.__init__(self, parent)
		self.QNuevoMensaje = Ui_DialogNuevoMensaje()
		self.QNuevoMensaje.setupUi(self)

		self.connect(self.QNuevoMensaje.buttonBox, QtCore.SIGNAL("rejected()"),self.CerrarVentana)
		self.connect(self.QNuevoMensaje.buttonBox, QtCore.SIGNAL("accepted()"),self.EnviarSMS)																			#Le paso QString que es lo que retorna.
		self.connect(self.QNuevoMensaje.lineEdit_NumeroTelefonico, QtCore.SIGNAL("textChanged(QString)"),self.MascaraNumero)

	def MascaraNumero(self,texto):
		#Para que una letra sea un numero en el simulador.
		for k,v in NumAdminsObjeto.dictnums.items():
			if str(texto) == str(k):
				self.QNuevoMensaje.lineEdit_NumeroTelefonico.setText("04142788259")
				break

		
	def EnviarSMS(self):
		numero = self.QNuevoMensaje.lineEdit_NumeroTelefonico.text()
		mensaje = self.QNuevoMensaje.plainTextEdit_Mensaje.toPlainText()
		validacion = Validar.Validar(numero)
		# if validacion == "Ok":
		if True:
			mensajecompleto = str(numero)+"|"+str(mensaje)+"|"+"15156"
			globalvars.ColaparaEnviar.append(mensajecompleto)
			self.hide()
		else:
			QtGui.QMessageBox.information(self, "Information", """El numero no cumple con el formato establecido""",QtGui.QMessageBox.Ok)

	def CerrarVentana(self):
		self.hide()


class MainClass(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QWidget.__init__(self)
		self.MainWindow = Ui_MainWindow()
		self.MainWindow.setupUi(self)
		#Consola Negra
		pal = QtGui.QPalette()
		bgc = QtGui.QColor(0, 0, 0)
		pal.setColor(QtGui.QPalette.Base, bgc)
		textc = QtGui.QColor(255, 255, 255)
		pal.setColor(QtGui.QPalette.Text, textc)
		self.MainWindow.plainTextEdit_Consola.setPalette(pal)
				
		self.setWindowIcon(QtGui.QIcon("icons/SystemTrey.png"))
		self.setWindowTitle('Soluciones SMS  (www.soluciones-sms.com)')

		#Colocando Fecha de Apertura
		self.MainWindow.label_FechaApertura.setText(str(LaFecha.damefecha()))
		#Creando QActions
		self.accionSalir = QtGui.QAction('Exit', self)
		self.accionSalir.setStatusTip('Exit App - Ctl+E')
		self.accionSalir.setShortcut('Ctl+E')
		self.accionSalir.setIcon(QtGui.QIcon('icons/Exit.png'))
		
		self.accionIniciar = QtGui.QAction('Excel', self)
		self.accionIniciar.setStatusTip('Load Excel File - Ctl+L')
		self.accionIniciar.setShortcut('Ctl+L')
		self.accionIniciar.setIcon(QtGui.QIcon('icons/excel.png'))
		
		self.accionDetener = QtGui.QAction('Simulator', self) #Simular SMS Automatic
		self.accionDetener.setStatusTip('Simulator - Ctl+S')
		self.accionDetener.setShortcut('Ctl+S')
		self.accionDetener.setIcon(QtGui.QIcon('icons/sms.png'))
		
		self.accionLimpiar = QtGui.QAction('Reset', self)
		self.accionLimpiar.setStatusTip('Reset Device - Ctl+R')
		self.accionLimpiar.setShortcut('Ctl+R')
		self.accionLimpiar.setIcon(QtGui.QIcon('icons/ResetModem.png'))
		
		#Creando ToolBar
		self.toolbar = QtGui.QToolBar(self)
		#Indicandole donde arrancara por defecto
		self.addToolBar(QtCore.Qt.TopToolBarArea,self.toolbar)
		#Agregandole a la ToolBar los QtGui.QActions
		self.toolbar.addAction(self.accionIniciar)
		self.toolbar.addAction(self.accionDetener)
		self.toolbar.addSeparator()
		self.toolbar.addAction(self.accionLimpiar)
		self.toolbar.addSeparator()
		self.toolbar.addAction(self.accionSalir)
		
		self.setWindowState(QtCore.Qt.WindowMaximized)
		if self.Iniciar():
			self.connect(self.modemseleccionado, QtCore.SIGNAL("signalEscribirConsola"),self.EscribirConsola)
			self.connect(self.modemseleccionado, QtCore.SIGNAL("signalModificarSenal"),self.ModificarSenal)
			self.connect(self.modemseleccionado, QtCore.SIGNAL("signalModificarOperadora"),self.ModificarOperadora)
			self.connect(self.modemseleccionado, QtCore.SIGNAL("signalModificarStatusBar"),self.ModificarStatusBar)
			self.connect(self.modemseleccionado, QtCore.SIGNAL("signalModificarStatusBar2"),self.ModificarStatusBar2)
			self.connect(self.modemseleccionado, QtCore.SIGNAL("signalModificarBateria"),self.ModificarBateria)
			self.connect(self.modemseleccionado, QtCore.SIGNAL("signalDetenerCliente"),self.DetenerCliente)
			self.connect(self.modemseleccionado, QtCore.SIGNAL("signalAddTabMensajeEnviado"),self.AddMensajeEnviado)
			self.connect(self.modemseleccionado, QtCore.SIGNAL("signalAddTabMensajeFallido"),self.AddMensajeFallido)
			self.connect(self.modemseleccionado, QtCore.SIGNAL("signalAddTabMensajeRecibido"),self.AddMensajeRecibido)
			self.connect(self.modemseleccionado, QtCore.SIGNAL("signalAddTabMensajeCola"),self.AddMensajeCola)
			self.connect(self.modemseleccionado, QtCore.SIGNAL("signalStatusToLabel"),self.StatusToLabel)

			self.connect(self.accionIniciar, QtCore.SIGNAL("triggered()"), self.IniciarModem)
			self.connect(self.accionDetener, QtCore.SIGNAL("triggered()"), self.DetenerModem)
			self.connect(self.accionSalir, QtCore.SIGNAL("triggered()"), self.exitEvent)


			#Para abrir la ventana del Nuevo Mensaje Simulador
			self.connect(self.MainWindow.actionNuevo_Mensaje, QtCore.SIGNAL("triggered()"), self.AbrirNuevoMensaje)
			#Para Salir del Sistema
			self.connect(self.MainWindow.actionNueva_Cola_de_Mensajes, QtCore.SIGNAL("triggered()"), self.exitEvent)

			


			self.connect(self.cliente, QtCore.SIGNAL("signalSlaveTrue"),self.SlaveToLabel)

			self.connect(self.server, QtCore.SIGNAL("signalMasterTrue"),self.MasterToLabel)
			self.connect(self.server, QtCore.SIGNAL("signalMastertoBD"),self.ArrancarBD)
			self.connect(self.server, QtCore.SIGNAL("signalCrearCliente"),self.CrearCliente)
			self.connect(self.modemseleccionado, QtCore.SIGNAL("signalCrearServer"),self.CrearServer)

			##################FUNCIONES PARA EL SYSTEM TRAY ICON#######################
			self.exitOnClose = False
			exit = QtGui.QAction(QtGui.QIcon("icons/SystemTrey.png"), "Close Modem ("+str(self.puerto)+")", self)
			self.connect(exit, QtCore.SIGNAL("triggered()"), self.exitEvent)
			self.trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon("icons/SystemTrey.png"), self)
			menu = QtGui.QMenu(self)
			menu.addAction(exit)
			self.trayIcon.setContextMenu(menu)
			self.connect(self.trayIcon, \
					QtCore.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), \
					self.trayIconActivated)
			self.trayIcon.show()
			self.trayIcon.showMessage("Soluciones SMS!", "Boton izquierdo para Open\nBoton derecho para Close" )
			self.trayIcon.setToolTip("Soluciones SMS COM"+str(self.puerto))

	def trayIconActivated(self, reason):
		if reason == QtGui.QSystemTrayIcon.Context:
			self.trayIcon.contextMenu().show()
		elif reason == QtGui.QSystemTrayIcon.Trigger:
			self.show()
			self.raise_()

	def closeEvent(self, event):
		if self.exitOnClose:
			self.trayIcon.hide()
			del self.trayIcon
			#event.accept()
		else:
			self.hide()
			event.setAccepted(True)
			event.ignore()

	def exitEvent(self):                
		self.exitOnClose = True
		self.PuertoCOM.close()
		self.close()

		################################################################################

	def AbrirNuevoMensaje(self):
		QNuevoMensaje = NuevoMensaje(self)
		QNuevoMensaje.show()


	def StatusToLabel(self,status):
		self.MainWindow.label_Estado.setText(status)
	def MasterToLabel(self):
		self.MainWindow.label_Modo.setText("M1")
	def SlaveToLabel(self):
		self.MainWindow.label_Modo.setText("S2")
	def AddMensajeEnviado(self,telefono,mensaje,pk,smsenviados):
		try:
			#Variables para Insertar
			datos = ["1",str(pk),str(telefono),str(mensaje),str(LaFecha.damefechaJerm())]
			fila = 0
			columna = 0
			self.MainWindow.tableWidget_Enviados.insertRow(0)
			for item in datos:
				texto = QtGui.QTableWidgetItem(item)
				self.MainWindow.tableWidget_Enviados.setItem(fila,columna,texto)
				columna = columna + 1
			#Eliminamor el primero de la cola
			self.MainWindow.tableWidget_Cola.removeRow(0)
			#Contamos la cantidad de columnas en la tabla
			if self.MainWindow.tableWidget_Enviados.rowCount() > 100:
				self.MainWindow.tableWidget_Enviados.removeRow(101)
			#Sumo el numero al Label Contador
			self.MainWindow.label_TotalEnviados.setText(str(smsenviados))

			#Actualizar el Label de la Cola
			self.AddMensajeCola()
		except Exception as exc:
			GuardarTXTObjeto.GuardarErrorLog(0,str(traceback.format_exc()))

	def AddMensajeFallido(self,telefono,mensaje,pk,smsfallidos):
		try:
			#Variables para Insertar
			datos = ["1",str(pk),str(telefono),str(mensaje),str(LaFecha.damefechaJerm())]
			fila = 0
			columna = 0
			self.MainWindow.tableWidget_Fallidos.insertRow(0)
			for item in datos:
				texto = QtGui.QTableWidgetItem(item)
				self.MainWindow.tableWidget_Fallidos.setItem(fila,columna,texto)
				columna = columna + 1
			#Eliminamor el primero de la cola
			self.MainWindow.tableWidget_Cola.removeRow(0)
			#Contamos la cantidad de columnas en la tabla
			if self.MainWindow.tableWidget_Fallidos.rowCount() > 100:
				self.MainWindow.tableWidget_Fallidos.removeRow(101)
			#Sumo el numero al Label Contador
			self.MainWindow.label_MensajesFallidos.setText("SMS Fail ("+str(smsfallidos)+")")

			#Actualizar el Label de la Cola
			self.AddMensajeCola()
		except Exception as exc:
			GuardarTXTObjeto.GuardarErrorLog(0,str(traceback.format_exc()))

	def AddMensajeCola(self,telefono=None,mensaje=None,pk=None):
		try:
			#Variables para Insertar
			if telefono != None:
				datos = ["1",str(pk),str(telefono),str(mensaje),str(LaFecha.damefechaJerm())]
				fila = 0
				columna = 0
				self.MainWindow.tableWidget_Cola.insertRow(0)
				for item in datos:
					texto = QtGui.QTableWidgetItem(item)
					self.MainWindow.tableWidget_Cola.setItem(fila,columna,texto)
					columna = columna + 1
					#Contamos la cantidad de columnas en la tabla
					if self.MainWindow.tableWidget_Cola.rowCount() > 100:
						self.MainWindow.tableWidget_Cola.removeRow(101)
			#Cambiamos el label de Contador
			filas = self.MainWindow.tableWidget_Cola.rowCount()
			self.MainWindow.label_TotalCola.setText(str(filas))
		except Exception as exc:
			GuardarTXTObjeto.GuardarErrorLog(0,str(traceback.format_exc()))
	def AddMensajeRecibido(self,telefono,mensaje,smsrecibidos):
		try:
			datos = [str(telefono),str(mensaje),str(LaFecha.damefechaJerm())]
			fila = 0
			columna = 0
			self.MainWindow.tableWidget_Recibidos.insertRow(0)
			for item in datos:
				texto = QtGui.QTableWidgetItem(item)
				self.MainWindow.tableWidget_Recibidos.setItem(fila,columna,texto)
				columna = columna + 1
				#Contamos la cantidad de columnas en la tabla
				if self.MainWindow.tableWidget_Recibidos.rowCount() > 100:
					self.MainWindow.tableWidget_Recibidos.removeRow(101)
			#Cambiamos el label de Contador
			self.MainWindow.label_MensajesRecibidos.setText("SMS Incoming ("+str(smsrecibidos)+")")
		except Exception as exc:
			GuardarTXTObjeto.GuardarErrorLog(0,str(traceback.format_exc()))		

	def EscribirConsola(self,text):                
		self.MainWindow.plainTextEdit_Consola.appendPlainText(time.strftime('%H:%M:%S') + " >> " + text)
	def ModificarSenal(self,senal):
		self.MainWindow.progressBar_Senal.setValue(int(senal))
	def ModificarBateria(self,bateria):
		self.MainWindow.progressBar_Bateria.setValue(int(bateria))
	def ModificarOperadora(self,operadora):
		self.MainWindow.label_Operadora.setText(str(operadora))
	def ModificarStatusBar2(self,marca,modelo,version,operadora,imei):
		self.MainWindow.statusbar.insertPermanentWidget(0,QtGui.QLabel("Version 8.1"),1)
		self.MainWindow.statusbar.insertPermanentWidget(1,QtGui.QLabel("COM ("+str(self.puerto)+")"),1)
		self.MainWindow.statusbar.insertPermanentWidget(2,QtGui.QLabel(str(marca)),1)
		self.MainWindow.statusbar.insertPermanentWidget(3,QtGui.QLabel(str(modelo)),1)
		self.MainWindow.statusbar.insertPermanentWidget(4,QtGui.QLabel(str(version)),1)
		self.MainWindow.statusbar.insertPermanentWidget(5,QtGui.QLabel(str(operadora)),1)
		self.MainWindow.statusbar.insertPermanentWidget(6,QtGui.QLabel(str(imei)),1)
		self.MainWindow.statusbar.insertPermanentWidget(7,QtGui.QLabel(str(self.MainWindow.label_Modo.text())),1)
		self.MainWindow.statusbar.insertPermanentWidget(8,QtGui.QLabel(str(time.strftime('%d/%m/%y' + ' %H:%M:%S'))),1)
                
	def ModificarStatusBar(self,marca,modelo,version,operadora,imei):		
		self.ModificarStatusBar2(marca,modelo,version,operadora,imei)
		self.MainWindow.statusbar.insertPermanentWidget(9,QtGui.QLabel(str("                                                                                                                                                                                                                                                                                                          ")),1)


	def IniciarModem(self):
		#self.Iniciar()
		file_name = QtGui.QFileDialog.getOpenFileName(self, "Open Data File", "", "Excel data files (*.xlsx)")
		wb = openpyxl.load_workbook(file_name)
		sheet = wb.get_active_sheet()


	def DetenerModem(self):                
		#self.PuertoCOM.close()
		numero = "04142788259"
		mensaje = "Prueba SMS Modem ("+str(self.puerto)+") "+str(time.strftime('%d/%m/%y' + ' %H:%M:%S'))
		mensajecompleto = str(numero)+"|"+str(mensaje)+"|"+"151589"
		globalvars.ColaparaEnviar.append(mensajecompleto)
		#self.accionIniciar.setEnabled(True)
		#self.accionDetener.setEnabled(False)
	def CrearServer(self):
		self.server.start()
	def CrearCliente(self):
		#Le cambiamos el Status a Falso al Modem en Master, para
		#que si esta pegado, se desconecte del server.
		self.modemseleccionado.Master = False
		self.cliente.start()
	def DetenerCliente(self):
		self.cliente.cliente.toStop = True
		print self.cliente.cliente.toStop
	def ArrancarBD(self,master):
		self.getsms = GetSMSBD(master)
		self.getsms.start()		
	def Iniciar(self):
		print globalvars.Modo
		try:
			if globalvars.Modo == '1':
				self.puertomodem = 23 #sys.argv[1] Es el parametro que llega de afuerta al correo el sistema
				self.BasedeDatos = BasedeDatos()
				self.BasedeDatos.Conectar()
				self.BasedeDatos.SeleccionarUno("""SELECT id_modem,tipo,config FROM t365_Modem WHERE id_modem = ?""", self.puertomodem)
				self.configpuerto = str(self.BasedeDatos.resultado.config).split(',')
				#460800,8,N,1
				self.configmodem = ['23',460800,'8','N','1','1']

			elif globalvars.Modo == '2':
				archivoconfiguracion = open('conf/config.txt','r')
				self.lineaconfig = archivoconfiguracion.readline()
				self.configmodem = self.lineaconfig.split(",")
			
			elif globalvars.Modo == None:
				self.configmodem = 23 #sys.argv[1] Es el parametro que llega de afuerta al correo el sistema
				#Pasando los argumentos a los objetos de PySerial
			self.puerto = 22 #self.configmodem[0]
			self.baudrate = 921600 #self.configmodem[1]
			self.bitesize = 8 #globalvars.nombresPySerial['BiteSize'][self.configmodem[2]]
			self.parity = 'N' #globalvars.nombresPySerial["Parity"][self.configmodem[3]]
			self.stopbits = 1 #globalvars.nombresPySerial["StopBits"][self.configmodem[4]]
			self.modem = 1 #self.configmodem[5].rstrip('\n')

			#Le cambiamos el nombre a la ventana y le colocamos el COM antes del Titulo
			self.setWindowTitle("("+str(self.puerto)+")"+"   .: www.soluciones-sms.com :.")
                        #serial.Serial(int(self.puerto)-1,self.baudrate,eval(self.bitesize),eval(self.parity),eval(self.stopbits))
			self.PuertoCOM = serial.Serial(port='COM22', baudrate=921600, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False, inter_byte_timeout=None)
			#23,460800,8,serial.PARITY_NONE,1)
                             
			print "Modem:"
			print self.modem
			self.modem = '2'
			if self.modem == '1':                                 
				self.modemseleccionado = Modem_EnforaSerial(self.PuertoCOM,self.puerto)
				
				self.modemseleccionado.start()
				self.accionIniciar.setEnabled(True)
				self.accionDetener.setEnabled(True)
				#Creamos el hilo del Server, pero no lo arrancamos si no con una senal desde el mismo Modem cuando compruebe que inicio bien
				self.server = HiloServer()
				#Creamos el hilo del Cliente, pero no lo arrancamos al menos que ya halla server. 
				self.cliente = HiloCliente()
			elif self.modem == '2':
				self.modemseleccionado = Modem_HuaweiUSB(self.PuertoCOM,self.puerto)
				
				self.modemseleccionado.start()
				self.accionIniciar.setEnabled(True)
				self.accionDetener.setEnabled(True)
				#Creamos el hilo del Server, pero no lo arrancamos si no con una senal desde el mismo Modem cuando compruebe que inicio bien
				self.server = HiloServer()
				#Creamos el hilo del Cliente, pero no lo arrancamos al menos que ya halla server. 
				self.cliente = HiloCliente()
			return True

		except Exception as exc:
			GuardarTXTObjeto.GuardarErrorLog(0,str(traceback.format_exc()))
			self.EscribirConsola("Port "+str(self.puerto)+" in use...")
			self.EscribirConsola(str(traceback.format_exc()))
			return False
			


if __name__ == "__main__":
	lic = LicCheck()
	AvisodeApertura(lic)
	if lic == True:
		app = QtGui.QApplication(sys.argv)
		app.setStyle(QtGui.QStyleFactory.create("plastique"))
		window = MainClass()
		window.show()
		app.exec_()
	else:
		pass
