import SocketServer
import time
import globalvars
from PyQt4 import QtCore


class ServidorSMS(SocketServer.BaseRequestHandler):
	def handle(self):
		try:	
			self.data = 'vacia'
			Salida = "Modem Conectado", self.client_address
			globalvars.ModemsConectados.append(str(self.client_address[1]))
			while len(self.data):
				#print globalvars.ModemsConectados
				self.data = ''
				self.MensajesParaCliente = ''
				self.data = self.request.recv(1024).rstrip()
				Salida = 'Recibido ' + self.data + ' del Cliente ' + str(self.client_address)
				if self.data == 'HelloServer':
					self.request.send('HelloClient')
					Salida = 'Enviando HelloClient al Cliente'
				elif self.data == 'Ready':
					if len(globalvars.ColaGeneral) > 0: 
						if len(globalvars.ColaGeneral) >= 6:
							for i in range(5):
								if self.MensajesParaCliente == '':
									self.MensajesParaCliente = str(globalvars.ColaGeneral.pop(0))
								else:
									self.MensajeparaAcoplar = str(globalvars.ColaGeneral.pop(0))
									self.MensajesParaCliente = self.MensajesParaCliente + '^' +self.MensajeparaAcoplar
						elif len(globalvars.ColaGeneral) >= 4:
							for i in range(3):
								if self.MensajesParaCliente == '':
									self.MensajesParaCliente = str(globalvars.ColaGeneral.pop(0))
								else:
									self.MensajeparaAcoplar = str(globalvars.ColaGeneral.pop(0))
									self.MensajesParaCliente = self.MensajesParaCliente + '^' +self.MensajeparaAcoplar
						elif len(globalvars.ColaGeneral) >= 1:
							self.MensajesParaCliente = str(globalvars.ColaGeneral.pop(0))
						else:
							pass
						if self.MensajesParaCliente != "":
							Salida = 'Enviando Mensajes al cliente = '+self.MensajesParaCliente
							self.request.send(self.MensajesParaCliente)
					else:
						self.request.send('NotBuffer')
						Salida = 'Enviando NotBuffer al Cliente'
				elif self.data == 'Bye':
					pass
				else:
					self.request.send('IDontUnderstand')
					Salida = 'Enviando IDontUnderstand al Cliente'

				time.sleep(1)
			Salida = "Cliente Desconectado", self.client_address[1]
			globalvars.ModemsConectados.remove(str(self.client_address[1]))
			self.request.close()
		except:
			Salida = "Cliente Desconectado", self.client_address[1]
			globalvars.ModemsConectados.remove(str(self.client_address[1]))
			self.request.close()



class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass

class HiloServer(QtCore.QThread):  
	def __init__(self):  
		QtCore.QThread.__init__(self) 
	def run(self):
		try:
			Salida = 'Consultor DB'
			self.puerto = 6562
			self.server = ThreadedTCPServer(('',self.puerto), ServidorSMS)
			Salida = 'Listing... ' + str(self.puerto) 
			#Cambiando el Modem a Master para que sepa que es Servidor
			master = True
			self.emit(QtCore.SIGNAL("signalMasterTrue"))
			#Solo si estamos en globalvars.Modo Base de Datos
			if globalvars.Modo == "1":
				self.emit(QtCore.SIGNAL("signalMastertoBD"),master)
			self.server.serve_forever()

		except:
			Salida = 'Puerto en Uso, Creando Cliente'
			#Mandamos a correr el hilo de Cliente
			self.emit(QtCore.SIGNAL("signalCrearCliente"))
			master = False
			#Solo si estamos en globalvars.Modo Base de Datos
			if globalvars.Modo == "1":
				self.emit(QtCore.SIGNAL("signalMastertoBD"),master)
