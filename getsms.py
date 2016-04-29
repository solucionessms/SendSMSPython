import time
from bd import BasedeDatos
from PyQt4 import QtCore
from formato import Validar
import globalvars
from guardarlog import GuardarTXTObjeto
import traceback

class GetSMSBD(QtCore.QThread):  
	def __init__(self,master):  
		QtCore.QThread.__init__(self)
		self.master = master
	def ConectarBD(self):
		self.BD1 = BasedeDatos()
		self.BD1.Conectar() 
	def BuscarMensajes(self):
		self.BD1.Seleccionar("SELECT id_salida, movil, sms, fecha_creada, status FROM t365_BsalidaSpeed WHERE status = 0")
		for SMS in self.BD1.resultado:
			ValidacionNum = Validar.Validar(str(SMS.movil))
			if ValidacionNum == 'Ok':
				self.BD1.Actualizar("UPDATE t365_BsalidaSpeed SET status = 5 WHERE id_salida = ?", int(SMS.id_salida))
				self.Mensaje = str(SMS.movil)+"|"+str(SMS.sms)+"|"+str(SMS.id_salida)
				globalvars.ColaGeneral.append(self.Mensaje)

			elif ValidacionNum == None:
				#Si el formato del numero no es valido
				self.BD1.Actualizar("UPDATE t365_BsalidaSpeed SET status = 3 WHERE id_salida = ?", int(SMS.id_salida))

	def ActualizarEnviados(self):
		#Lista donde se almacenan los PK que ya se colocaron como enviados, para luego borrarlos de la lista
		pkaborrar = []
		for PKMensaje in globalvars.ColaEnviados:
			self.BD1.Actualizar("UPDATE t365_BsalidaSpeed SET status = 1 WHERE id_salida = ?", int(PKMensaje))
			pkaborrar.append(PKMensaje)
		#Borrando de la lista los PK ya actualizados
		cantidad = len(pkaborrar)
		for i in range(cantidad):
			globalvars.ColaEnviados.remove(pkaborrar[i])


	def ActualizarFallidos(self):
		#Lista donde se almacenan los PK que ya se colocaron como enviados, para luego borrarlos de la lista
		pkaborrar = []
		for PKMensaje in globalvars.ColaFallidos:
			self.BD1.Actualizar("UPDATE t365_BsalidaSpeed SET status = 2 WHERE id_salida = ?", int(PKMensaje))
			pkaborrar.append(PKMensaje)
		#Borrando de la lista los PK ya actualizados
		cantidad = len(pkaborrar)
		for i in range(cantidad):
			globalvars.ColaFallidos.remove(pkaborrar[i])
	def InsertarRecibidos(self):
		cantidadrecibidos = len(globalvars.ColaRecibidos)
		for PKMensaje in range(cantidadrecibidos):
			self.BD1.Insertar("INSERT INTO t365_Bentrada(id_cliente,id_user,movil,sms,fecha,status,modem)values(?,?,?,?,?,?,?); """, globalvars.ColaRecibidos.pop(0))
	def Iniciar(self):
		#Esta funcion iniciar la creo porque no se puede llamar a run directamente.
		self.ConectarBD()
		while True:
			try:
				#Solo si es Master busca mensajes en la Base de datos
				if self.master == True:
					self.BuscarMensajes()
				else:
					pass
				#Pero igualmente al ser Slave Actualiza sus propios Mensajes en BD
				self.ActualizarEnviados()
				self.ActualizarFallidos()
				self.InsertarRecibidos()
				time.sleep(1)
			except Exception as exc:
				GuardarTXTObjeto.GuardarErrorLog('GETSMS Error...',str(traceback.format_exc()))
				print 'NO DATA BASE CONECTION...'
				time.sleep(10)
				self.Iniciar()

	def run(self):
		self.Iniciar()



