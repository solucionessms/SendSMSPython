import time
import socket
from PyQt4 import QtCore
import globalvars

class ClienteSMS(object):
	def __init__(self):
		# Creando un socket TCP/IP
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.toStop = False
	def Conectar(self):
		try:
			#print 'Buscando Server'
			server_address = ('localhost', 6562)
			self.sock.connect(server_address)
			#print 'Conectando a Server' + str(server_address)
			self.Comunicarse()
		except:
			Salida = "No Conect to Server"
			Salida = "Waiting..."
			time.sleep(5)
			self.Conectar()
	def Comunicarse(self):
		try:
			while self.toStop == False:
				#Solo si no tiene Mensajes en cola, va y pide
				if len(globalvars.ColaparaEnviar) == 0 and len(globalvars.ColaGeneral) == 0:
					self.sock.sendall('HelloServer')
					Salida = 'Enviando HelloServer al Server'
					if self.toStop == True:
						break
					else:
						data = self.sock.recv(1024).rstrip()
						Salida = 'RECIVER: ' + data
						if data == 'HelloClient':
							self.sock.sendall('Ready')
							Salida = 'OK...'
							if self.toStop == True:
								break
							else:
								data = self.sock.recv(1024).rstrip()
								if data != 'NotBuffer':
									Salida = "SMS Incoming...."
									self.mensajes = data.split('^')
									Salida = "Mensajes Recibidos (" + str(self.mensajes) + ")"
									for msg in self.mensajes:
										globalvars.ColaGeneral.append(str(msg))
									Salida = globalvars.ColaGeneral
								elif data == 'NotBuffer':
									Salida = "No Cache Reciver..."
								elif data == 'IDontUnderstand':
									pass
									time.sleep(1)
				else:
					time.sleep(1.5)
					pass

		except:
			Salida = 'Server Disconect...'
			self.sock.close()
			self.Conectar()

class HiloCliente(QtCore.QThread):  
	def __init__(self):  
		QtCore.QThread.__init__(self) 
	def run(self):
		self.cliente = ClienteSMS()
		self.emit(QtCore.SIGNAL("signalSlaveTrue"))
		self.cliente.Conectar()

