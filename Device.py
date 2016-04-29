#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, datetime 
from PyQt4 import QtCore
import re
import globalvars
from guardarlog import GuardarTXTObjeto
import traceback


class Modem_EnforaSerial(QtCore.QThread):
	def __init__(self,puerto,numpuerto):
		QtCore.QThread.__init__(self)
		self.MODEM = puerto #Es el objeto del Puerto
		self.NumPuerto = numpuerto
		self.FallidosSeguidos = 0
		self.Status = "ERROR"
		self.Master = True
		self.TotalSMSEnviados = 0
		self.TotalSMSFallidos = 0
		self.TotalSMSCola = 0
		self.TotalSMSRecibidos = 0
	def run(self):
		
		self.proceso()
 ####################################################################
 ###################### COMANDOS DE INTERFAZ ########################
 ####################################################################

	def Imprimir(self,*args):
		self.emit(QtCore.SIGNAL("signalEscribirConsola"),*args)
	def AddInfoStatusBar(self,marca,modelo,version,imei):
		self.emit(QtCore.SIGNAL("signalModificarStatusBar"),marca,modelo,version,imei,)
	def AddTabMensajeRecibido(self,telefono,mensaje):
		#Ojo Tambien suma el numero en el Label
		self.TotalSMSRecibidos = self.TotalSMSRecibidos + 1
		self.emit(QtCore.SIGNAL("signalAddTabMensajeRecibido"),telefono,mensaje,self.TotalSMSRecibidos)
	def AddTabMensajeFallido(self,telefono,mensaje,pk):
		#Ojo Tambien suma el numero en el Label
		self.TotalSMSFallidos = self.TotalSMSFallidos + 1
		self.emit(QtCore.SIGNAL("signalAddTabMensajeFallido"),telefono,mensaje,pk,self.TotalSMSFallidos)
	def AddTabMensajeEnviado(self,telefono,mensaje,pk):
		#Ojo Tambien suma el numero en el Label
		self.TotalSMSEnviados = self.TotalSMSEnviados + 1
		self.emit(QtCore.SIGNAL("signalAddTabMensajeEnviado"),telefono,mensaje,pk,self.TotalSMSEnviados)
	def AddTabMensajeCola(self):
		for i in reversed(globalvars.ColaparaEnviar):
			sms = i.split("|")
			pk = sms[2]
			telefono = sms[0]
			mensaje = sms[1]
			self.emit(QtCore.SIGNAL("signalAddTabMensajeCola"),telefono,mensaje,pk)
	def StatusToLabel(self,status):
		self.emit(QtCore.SIGNAL("signalStatusToLabel"),status)


 ####################################################################
 #################### COMANDOS DE INFORMACION #######################
 ####################################################################

	def DameMarca(self):
		self.Imprimir('Reading...1')
		self.MODEM.write("AT+CGMI\r\n")
		respuesta = self.LeerBuffer()
		self.Marca = respuesta[0]
		self.Imprimir(str(respuesta))
	def DameModelo(self):
		self.Imprimir('Reading...2')
		self.MODEM.write("AT+CGMM\r\n")
		respuesta = self.LeerBuffer()
		self.Modelo = respuesta[0]
		self.Imprimir(str(respuesta))
	def DameVersion(self):
		self.Imprimir('Reading...3')
		self.MODEM.write("AT+CGMR\r\n")
		respuesta = self.LeerBuffer()
		self.Version = respuesta[0]
		self.Imprimir(str(respuesta))
	def DameIMEI(self):
		self.Imprimir('Reading...4')
		self.MODEM.write("AT+CGSN\r\n")
		respuesta = self.LeerBuffer()
		self.IMEI = respuesta[0]
		self.Imprimir(str(respuesta))
	def DameEstadoSIM(self):
		self.Imprimir('Reading...5')
		self.MODEM.write("AT+CPIN?\r\n")
		respuesta = self.LeerBuffer()
		self.Imprimir(str(respuesta))
		#Si responde que esta READY
		for i in respuesta:
			if re.match("\+CPIN: READY",i):
				return "OK"
			else:
				return "ERROR"
	def DameOperadora(self):
		self.Imprimir('Reading...6')
		self.MODEM.write("AT+COPS?\r\n")
		respuesta = self.LeerBuffer()
		self.Imprimir(str(respuesta))
		for i in respuesta:
			if re.match("\+COPS",i):
				operadoraactual = i.split(",")
				if len(operadoraactual) > 1:
					operadoraactual = operadoraactual[2]
				self.emit(QtCore.SIGNAL("signalModificarOperadora"),operadoraactual)
				self.OPERADORA = operadoraactual
				return "OK"
			else:
				return "ERROR"
	def EstasRegistrado(self):
		self.Imprimir('Reading...7')
		self.MODEM.write("AT+CREG?\r\n")
		respuesta = self.LeerBuffer()
		self.Imprimir(str(respuesta))
		for i in respuesta:
			if re.match("\+CREG:",i):
				estadooperadora = i.split(",")
				estadooperadora = estadooperadora[1]
				if estadooperadora == "1" or "5":
					return "OK"
				else:
					return "ERROR"
			else:
				return "ERROR"
	def DameSenal(self):
		#self.Imprimir('Reading...8')
		self.MODEM.write("AT+CSQ\r\n")
		respuesta = self.LeerBuffer()
		#self.Imprimir(str(respuesta))
		for i in respuesta:
			if re.match("\+CSQ",i):
				senal = i.split(",")
				senal = senal[0].replace("+CSQ:","")
				if senal == "99":
					senal = "0"
					self.emit(QtCore.SIGNAL("signalModificarSenal"),senal)
					return "ERROR"
				else:
					self.emit(QtCore.SIGNAL("signalModificarSenal"),senal)
					return "OK"
	def DameBateria(self):
		#Como no usa Bateria
		bateria = 100
		self.emit(QtCore.SIGNAL("signalModificarBateria"),bateria)

 ####################################################################
 ################### COMANDOS DE FUNCIONAMIENTO #####################
 ####################################################################

	#Para leer el Buffer de los Mensajes debe ser mas lento
	#Y creo una nueva funcion para no afectar al resto de los
	#Comandos
	def LeerBufferSMS(self):
		time.sleep(0.2)
		todalarespuesta = []
		while self.MODEM.inWaiting() >= 1:
			respuesta = self.MODEM.readline()
			if respuesta == "\r\n":
				pass
			elif re.match("\+CMTI",respuesta):
				pass
			elif re.match("\%",respuesta):
				GuardarTXTObjeto.GuardarErrorLog(self.NumPuerto,respuesta)
			elif re.match("RING",respuesta):
				GuardarTXTObjeto.GuardarErrorLog(self.NumPuerto,respuesta)
			else:
				respuesta = respuesta.replace("\r","")
				respuesta = respuesta.replace("\n","")
				todalarespuesta.append(respuesta)
			time.sleep(0.5)
		return todalarespuesta

	def LeerBuffer(self):
		time.sleep(0.2)
		todalarespuesta = []
		while self.MODEM.inWaiting() >= 1:
			respuesta = self.MODEM.readline()
			if respuesta == "\r\n":
				pass
			elif re.match("\+CMTI",respuesta):
				pass
			elif re.match("\^",respuesta):
				pass
			elif re.match("\%",respuesta):
				GuardarTXTObjeto.GuardarErrorLog(self.NumPuerto,respuesta)
			elif re.match("RING",respuesta):
				GuardarTXTObjeto.GuardarErrorLog(self.NumPuerto,respuesta)
			else:
				respuesta = respuesta.replace("\r","")
				respuesta = respuesta.replace("\n","")
				todalarespuesta.append(respuesta)
		return todalarespuesta

 ####################################################################
 ################### COMANDOS DE CONFIGURACION ######################
 ####################################################################
	def DesactivarAutoRetransmisionSMS(self):
		self.Imprimir('Reading...9')
		self.MODEM.write("AT%CMGRS=0\r\n")
		respuesta = self.LeerBuffer()
		self.Imprimir(str(respuesta))
		if "OK" in respuesta:
			return "OK"
		else:
			return "ERROR"
		


	def DesactivarLecturaAutomaticaSMS(self):
		self.Imprimir('Reading...10')
		self.MODEM.write("AT+CNMI=1,1,0,0,0\r\n")
		respuesta = self.LeerBuffer()
		self.Imprimir(str(respuesta))
		if "OK" in respuesta:
			return "OK"
		else:
			return "ERROR"
		

	def ActivarSMSTexto(self):
		self.Imprimir('Reading...11')
		self.MODEM.write("AT+CMGF=1\r\n")
		respuesta = self.LeerBuffer()
		self.Imprimir(str(respuesta))
		if "OK" in respuesta:
			return "OK"
		else:
			return "ERROR"
	def ActivarTextoErrores(self):
		self.Imprimir('Reading...12')
		self.MODEM.write("AT+CMEE=2\r\n")
		respuesta = self.LeerBuffer()
		#Identificamos la Respuesta
		self.Imprimir(str(respuesta))
		if "OK" in respuesta:
			return "OK"
		else:
			return "ERROR"
	def QuitarEcho(self):
		self.Imprimir('Reading...13')
		self.MODEM.write("ATE0\r\n")
		respuesta = self.LeerBuffer()
		#Identificamos la Respuesta
		self.Imprimir(str(respuesta))
		if "OK" in respuesta:
			return "OK"
		else:
			return "ERROR"

 ####################################################################
 ######################## COMANDOS DE SMS ###########################
 ####################################################################
	def LeerSMS(self):		
		self.MODEM.write('AT+CMGL="REC UNREAD"\r\n')
		time.sleep(1.0)
		respuesta = self.LeerBufferSMS()
		#Identificamos la Respuesta
		self.Imprimir('Reading Incoming Messages...'+str(respuesta))
		#Tomamos el Largo de la respuesta
		largorespuesta = len(respuesta)
		p1 = False
		mensajesarreglados = []
		#Acomodamos los Mensajes
		for i in range(largorespuesta):
			if re.match("\+CMGL",(respuesta[i-1])):
				parte1 = respuesta[i-1]
				p1 = True
			elif p1 == True:
				completo =  parte1 + "," + respuesta[i-1]
				mensajesarreglados.append(completo)
				p1 = False
			else:
				pass
		#Tomamos lo que nos interesa y lo insertamos en la interfaz y BD o Texto
		#Depende del Modo [Consultar globalvars]
		#Creamos lista index en blanco.
		listaindex = []
		for i in mensajesarreglados:
			todosms = i.split(",")
			index = int(todosms[0].replace("+CMGL:",""))
			telefono = str(todosms[2].replace('"',''))
			fecha = str(todosms[4].replace('"',''))
			hora = str(todosms[5].replace('"',''))
			mensaje = str(todosms[6])
			self.AddTabMensajeRecibido(telefono,mensaje)
			#Lista de Index para despues borrarlas
			listaindex.append(str(index))
			#Si estamos trabajando con Base de Datos:
			if globalvars.Modo == "1":
				now = datetime.datetime.now()
				mensajeparabd = ['0','0',telefono,mensaje,now,'0',str(self.NumPuerto)]
				globalvars.ColaRecibidos.append(mensajeparabd)
			#Si esta en Modo 2 o 3, [Consultar Globalvars]
			else:
				pass
		#Solo si hay mensajes los borro
		if len(listaindex) >= 1:
			#Ahora Mandamos a borrar todos los mensajes que recibimos
			self.VaciarMemoriaSMS(listaindex)
		else:
			pass



	
	def EnviarCTRLZ(self):
		self.MODEM.write(chr(26)+"\r\n")
		time.sleep()
	def VaciarMemoriaSMS(self,listaindex):
		#self.Imprimir('Delete Incoming Messages...')
		for i in listaindex:
			self.Imprimir("Delete Incoming Messages (" +str(i)+")" )
			self.MODEM.write("AT+CMGD=%s\r\n"%i)
			time.sleep(1.2)
			respuesta = self.LeerBuffer()
			self.Imprimir(str(respuesta))
			#if "OK" in respuesta:
			#	return "OK"
			#elif "ERROR" in respuesta:
			#	return "OK"
	def EnviarSMS(self):
		mensajeytelefono = globalvars.ColaparaEnviar.pop(0)
		self.Imprimir("SENDING SMS: "+ str(mensajeytelefono))
		mensajeytelefono = mensajeytelefono.split("|")
		telefono = mensajeytelefono[0]
		mensaje = mensajeytelefono[1]
		pk = mensajeytelefono[2]
		intento = 1
		while intento <= 3:
			self.MODEM.write('AT+CMGS="%s"\r\n' %str(telefono))
			time.sleep(1)
			self.MODEM.readline()
			completo = ""
			while True:
				caracter = self.MODEM.read()
				completo = completo + caracter
				if caracter == "\x20":
					break
			self.Imprimir(completo)
			self.MODEM.write(str(mensaje)+chr(26)+"\r\n")
			while self.MODEM.inWaiting() == 0:
				pass
			respuesta = self.LeerBuffer()
			self.Imprimir(str(respuesta))
			for i in respuesta:
				if re.match("\+CMS ERROR",i):

					enviado = False
					intento = intento + 1
					GuardarTXTObjeto.GuardarErrorLog(self.NumPuerto,str(respuesta)+" Error # "+str(intento),telefono+"-"+mensaje)

					#Si van 3 intentos fallidos, se suma a fallidosseguidos
					if intento == 4:
						self.FallidosSeguidos = self.FallidosSeguidos + 1
						#Verificamos si van 10 Fallidos Seguidos para cambiar Status Modem
						if self.FallidosSeguidos == 10:
							#Enviamos el Status al Label
							self.StatusToLabel("ERROR")
							#Cambiamos el Status para Detener
							self.Status = "ERROR"
						break

					self.Imprimir("Error "+str(intento)+"Send SMS")
					self.Imprimir("Waiting...")
					time.sleep(3)

				elif re.match("\+CMGS",i):
					enviado =  True
					intento = 4
					#En caso de enviar un SMS, se coloca en 0 fallidosseguidos
					self.FallidosSeguidos = 0
					break
				else:
					#Enviar al Log de Error Respuesta Inesperada
					GuardarTXTObjeto.GuardarErrorLog(self.NumPuerto,respuesta,mensaje)
					#En caso de que no responda algo esperado
					enviado = False
					intento = intento + 1
					#Si van 3 intentos fallidos, se suma a fallidosseguidos
					if intento == 4:
						self.FallidosSeguidos = self.FallidosSeguidos + 1
						#Verificamos si van 10 Fallidos Seguidos para cambiar Status Modem
						if self.FallidosSeguidos == 10:
							#Enviamos el Status al Label
							self.StatusToLabel("ERROR")
							#Cambiamos el Status para Detener
							self.Status = "ERROR"
						break
		#Si el PK es simulado es un mensaje simulado que no se guarda. Solo se envia
		if enviado == True and pk != "Simulado":
			self.AddTabMensajeEnviado(telefono,mensaje,pk)
			globalvars.ColaEnviados.append(str(mensajeytelefono[2]))
		elif enviado == False and pk != "Simulado":
			self.AddTabMensajeFallido(telefono,mensaje,pk)
			globalvars.ColaFallidos.append(str(mensajeytelefono[2]))
	def proceso(self):
		try:
			#Enviamos CTRLZ por quedo enviando SMS, Manual con un TimeSleep para Esperar una respuesta mas tiempo
			self.MODEM.write(chr(26)+"\r\n")
			time.sleep(5)
			#Si hay algo en el Buffer, lo leemos
			if self.MODEM.inWaiting() >= 1:
				self.LeerBuffer()
			else:
				pass
			#Verificamos que quitamos el ECHO
			if self.QuitarEcho() == "OK":
				#Colocamos los Errores Completos
				self.ActivarTextoErrores()
				#Verificamos el Estado de la SIM en el Equipo
				if self.DameEstadoSIM() == "OK":
					#Verificamos si estamos Conectados a la Operadora
					if self.EstasRegistrado() == "OK":
						#Verificamos a que Operador estamos registrados
						self.DameOperadora()
						#Verificamos el nivel de señal del equipo
						if self.DameSenal() == "OK":
							#Activamos el Modo Texto
							if self.ActivarSMSTexto() == "OK":
								self.DesactivarLecturaAutomaticaSMS()
								self.DesactivarAutoRetransmisionSMS()
								self.DameMarca()
								self.DameModelo()
								self.DameVersion()
								self.DameIMEI()
								self.DameBateria()
								#Envio la informacion para la StatusBar
								self.AddInfoStatusBar(self.Marca,self.Modelo,self.Version,self.OPERADORA,self.IMEI)
								#Vacio la Memoria de SMS
								#self.VaciarMemoriaSMS()
								#Coloco el Modem en Status OK
								self.Status = "OK"
								#Colocamos el Status en el Label
								self.StatusToLabel("OK")
								self.emit(QtCore.SIGNAL("signalCrearServer"))
								while True:
									if self.Status == "OK":
										if len(globalvars.ColaparaEnviar) >= 1:
											#Enviamos Mensajes
											self.EnviarSMS()
										else:
											if len(globalvars.ColaGeneral) >= 1:
												#if self.Master == True:
													if len(globalvars.ColaGeneral) >= 10:
														for i in range(5):
															globalvars.ColaparaEnviar.append(globalvars.ColaGeneral.pop(0))														
													else:
														globalvars.ColaparaEnviar.append(globalvars.ColaGeneral.pop(0))
													self.AddTabMensajeCola()
													#Para que de tiempo de colocar la cola en la interfaz
													time.sleep(1)
											else:
												self.Imprimir("Reading SMS...OK")
												self.LeerSMS()
												#Pedimos la senal para comprobar que tengamos
												while True:
													senal = self.DameSenal()
													if senal == "OK":
														break
													else:
														self.Imprimir("Not signal Operator")
														pass
														time.sleep(1)
											#time.sleep(4)
									elif self.Status == "ERROR":
										#Solo detiene el Cliente si es Tipo Cliente, si es Server sigue corriendo
										#Asi no pueda enviar mensajes.
										if self.Master == False:
											self.emit(QtCore.SIGNAL("signalDetenerCliente"))
										self.Imprimir("Sending Email....Notificate Error 1519")
										break
							else:
								#No se pudo activar Modo Texto
								self.Imprimir("Error 1531") 
						else:
							#No tiene Senal el Modem
							self.Imprimir("Error 1532") 
					else:
						#Problema con la Operadora, No la Consigue
						self.Imprimir("Error 1533") 
				else:
					#Problema con la SIMCARD
					self.Imprimir("Error 1534") 
			else:
				#No se pudo eliminar el ECHO
				self.Imprimir("Error 1535") 
		except Exception as exc:
			excepcion = str(exc)
			GuardarTXTObjeto.GuardarErrorLog(self.NumPuerto,"Not Comunicate Device...  "+str(traceback.format_exc()))
			self.Imprimir("Not Comunicate Device... ")
			


class Modem_HuaweiUSB(QtCore.QThread):
	def __init__(self,puerto,numpuerto):
		QtCore.QThread.__init__(self)
		self.MODEM = puerto #Es el objeto del Puerto
		self.NumPuerto = numpuerto
		self.FallidosSeguidos = 0
		self.Status = "ERROR"
		self.Master = True
		self.TotalSMSEnviados = 0
		self.TotalSMSFallidos = 0
		self.TotalSMSCola = 0
		self.TotalSMSRecibidos = 0
	def run(self):
		self.proceso()
####################################################################
###################### COMANDOS DE INTERFAZ ########################
####################################################################

	def Imprimir(self,*args):
		self.emit(QtCore.SIGNAL("signalEscribirConsola"),*args)
	def AddInfoStatusBar(self,marca,modelo,version,operadora,imei):
		self.emit(QtCore.SIGNAL("signalModificarStatusBar"),marca,modelo,version,operadora,imei)
	def AddTabMensajeRecibido(self,telefono,mensaje):
		#Ojo Tambien suma el numero en el Label
		self.TotalSMSRecibidos = self.TotalSMSRecibidos + 1
		self.emit(QtCore.SIGNAL("signalAddTabMensajeRecibido"),telefono,mensaje,self.TotalSMSRecibidos)
	def AddTabMensajeFallido(self,telefono,mensaje,pk):
		#Ojo Tambien suma el numero en el Label
		self.TotalSMSFallidos = self.TotalSMSFallidos + 1
		self.emit(QtCore.SIGNAL("signalAddTabMensajeFallido"),telefono,mensaje,pk,self.TotalSMSFallidos)
	def AddTabMensajeEnviado(self,telefono,mensaje,pk):
		#Ojo Tambien suma el numero en el Label
		self.TotalSMSEnviados = self.TotalSMSEnviados + 1
		self.emit(QtCore.SIGNAL("signalAddTabMensajeEnviado"),telefono,mensaje,pk,self.TotalSMSEnviados)
	def AddTabMensajeCola(self):
		for i in reversed(globalvars.ColaparaEnviar):
			sms = i.split("|")
			pk = sms[2]
			telefono = sms[0]
			mensaje = sms[1]
			self.emit(QtCore.SIGNAL("signalAddTabMensajeCola"),telefono,mensaje,pk)
	def StatusToLabel(self,status):
		self.emit(QtCore.SIGNAL("signalStatusToLabel"),status)

####################################################################
#################### COMANDOS DE INFORMACION #######################
####################################################################

	def DameMarca(self):
		self.Imprimir('Reading...1')
		self.MODEM.write("AT+CGMI\r\n")
		respuesta = self.LeerBuffer()
		self.Marca = respuesta[0]
		self.Imprimir(str(respuesta))
	def DameModelo(self):
		self.Imprimir('Reading...2')
		self.MODEM.write("AT+CGMM\r\n")
		respuesta = self.LeerBuffer()
		self.Modelo = respuesta[0]
		self.Imprimir(str(respuesta))
	def DameVersion(self):
		self.Imprimir('Reading...3')
		self.MODEM.write("AT+CGMR\r\n")
		respuesta = self.LeerBuffer()
		self.Version = respuesta[0]
		self.Imprimir(str(respuesta))
	def DameIMEI(self):
		self.Imprimir('Reading...4')
		self.MODEM.write("AT+CGSN\r\n")
		respuesta = self.LeerBuffer()
		self.IMEI = respuesta[0]
		self.Imprimir(str(respuesta))
	def DameEstadoSIM(self):
		self.Imprimir('Reading...5')
		self.MODEM.write("AT+CPIN?\r\n")
		respuesta = self.LeerBuffer()
		self.Imprimir(str(respuesta))
		#Si responde que esta READY
		for i in respuesta:
			if re.match("\+CPIN: READY",i):
				return "OK"
			else:
				return "ERROR"

	def DameOperadora(self):
		#Para que cuando le pida me de el nombre y no el codigo
		self.Imprimir('Reading...6')
		self.MODEM.write("AT+COPS=0,0\r\n")
		time.sleep(0.5)
		respuesta = self.LeerBuffer()
		self.Imprimir(str(respuesta))
		#Para que me de el nombre
		self.Imprimir('Reading...7')
		self.MODEM.write("AT+COPS?\r\n")
		respuesta = self.LeerBuffer()
		self.Imprimir(str(respuesta))
		for i in respuesta:
			if re.match("\+COPS",i):
                                try:
                                        operadoraactual2 = i.split(",")
                                        operadoraactual = operadoraactual2[2]
                                        self.OPERADORA = operadoraactual
                                        self.emit(QtCore.SIGNAL("signalModificarOperadora"),operadoraactual)
                                        return "OK"
                                except Exception as exc:
                                        return "OK"
			else:
				return "ERROR"
	def DameBateria(self):
		#Este Modelo no utiliza Bateria por eso
		self.bateria = 100
	def EstasRegistrado(self):
		self.Imprimir('Reading...7')
		self.MODEM.write("AT+CREG?\r\n")
		respuesta = self.LeerBuffer()
		self.Imprimir(str(respuesta))
		for i in respuesta:
			if re.match("\+CREG:",i):
				estadooperadora = i.split(",")
				estadooperadora = estadooperadora[1]
				if estadooperadora == "1" or "5":
					return "OK"
				else:
					return "ERROR"
			else:
				return "ERROR"
	def DameSenal(self):
		#self.Imprimir('Reading...8')
		self.MODEM.write("AT+CSQ\r\n")
		respuesta = self.LeerBuffer()
		#self.Imprimir(str(respuesta))
		for i in respuesta:
			if re.match("\+CSQ",i):
				senal = i.split(",")
				senal = senal[0].replace("+CSQ:","")
				if senal == "99":
					senal = "0"
					self.emit(QtCore.SIGNAL("signalModificarSenal"),senal)
					return "ERROR"
				else:
					self.emit(QtCore.SIGNAL("signalModificarSenal"),senal)
					return "OK"
	def DameBateria(self):
		#Como no usa Bateria
		bateria = 100
		self.emit(QtCore.SIGNAL("signalModificarBateria"),bateria)

####################################################################
################### COMANDOS DE FUNCIONAMIENTO #####################
####################################################################
	

	#Para leer el Buffer de los Mensajes debe ser mas lento
	#Y creo una nueva funcion para no afectar al resto de los
	#Comandos
	def LeerBufferSMS(self):
		time.sleep(0.5)
		todalarespuesta = []
		while self.MODEM.inWaiting() >= 1:
			respuesta = self.MODEM.readline()
			if respuesta == "\r\n":
				pass
			elif re.match("\+CMTI",respuesta):
				pass
			elif re.match("\^",respuesta):
				pass
			else:
				respuesta = respuesta.replace("\r","")
				respuesta = respuesta.replace("\n","")
				todalarespuesta.append(respuesta)
			time.sleep(0.4)
		return todalarespuesta

	def LeerBuffer(self):
		time.sleep(0.5)
		todalarespuesta = []
		while self.MODEM.inWaiting() >= 1:
			respuesta = self.MODEM.readline()
			if respuesta == "\r\n":
				pass
			elif re.match("\+CMTI",respuesta):
				pass
			elif re.match("\^",respuesta):
				pass
			else:
				respuesta = respuesta.replace("\r","")
				respuesta = respuesta.replace("\n","")
				todalarespuesta.append(respuesta)
		return todalarespuesta

####################################################################
################### COMANDOS DE CONFIGURACION ######################
####################################################################

	def ActivarSMSTexto(self):
		self.Imprimir('Reading...9')
		self.MODEM.write("AT+CMGF=1\r\n")
		respuesta = self.LeerBuffer()
		self.Imprimir(str(respuesta))
		if "OK" in respuesta:
			return "OK"
		else:
			return "ERROR"
	def ActivarTextoErrores(self):
		self.Imprimir('Reading...10')
		self.MODEM.write("AT+CMEE=2\r\n")
		respuesta = self.LeerBuffer()
		#Identificamos la Respuesta
		self.Imprimir(str(respuesta))
		if "OK" in respuesta:
			return "OK"
		else:
			return "ERROR"
	def QuitarEcho(self):
		self.Imprimir('Reading...11')
		self.MODEM.write("ATE0\r\n")
		respuesta = self.LeerBuffer()
		#Identificamos la Respuesta
		self.Imprimir(str(respuesta))
		if "OK" in respuesta:
			return "OK"
		else:
			return "ERROR"

####################################################################
######################## COMANDOS DE SMS ###########################
####################################################################
	def LeerSMS(self):
		#self.Imprimir('Reading Incoming Messages')
		self.MODEM.write('AT+CMGL="REC UNREAD"\r\n')
		time.sleep(1.0)
		respuesta = self.LeerBufferSMS()
		#Identificamos la Respuesta
		#self.Imprimir(str(respuesta))
		self.Imprimir('Reading Incoming Messages...'+str(respuesta))
		#Tomamos el Largo de la respuesta
		largorespuesta = len(respuesta)
		p1 = False
		mensajesarreglados = []
		#Acomodamos los Mensajes
		for i in range(largorespuesta):
			if re.match("\+CMGL",(respuesta[i-1])):
				parte1 = respuesta[i-1]
				p1 = True
			elif p1 == True:
				completo =  parte1 + "," + respuesta[i-1]
				mensajesarreglados.append(completo)
				p1 = False
			else:
				pass
		#Tomamos lo que nos interesa y lo insertamos en la interfaz y BD o Texto
		#Depende del Modo [Consultar globalvars]
		#Creamos lista index en blanco.
		listaindex = []
		for i in mensajesarreglados:
			todosms = i.split(",")
			index = int(todosms[0].replace("+CMGL:",""))
			telefono = str(todosms[2].replace('"',''))
			fecha = str(todosms[4].replace('"',''))
			hora = str(todosms[5].replace('"',''))
			mensaje = str(todosms[6])
			self.AddTabMensajeRecibido(telefono,mensaje)
			#Lista de Index para despues borrarlas
			listaindex.append(str(index))
			#Si estamos trabajando con Base de Datos:
			if globalvars.Modo == "1":
				now = datetime.datetime.now()
				mensajeparabd = ['0','0',telefono,mensaje,now,'0',str(self.NumPuerto)]
				globalvars.ColaRecibidos.append(mensajeparabd)
			#Si esta en Modo 2 o 3, [Consultar Globalvars]
			else:
				pass
		#Solo si hay mensajes los borro
		if len(listaindex) >= 1:
			#Ahora Mandamos a borrar todos los mensajes que recibimos
			self.VaciarMemoriaSMS(listaindex)
		else:
			pass

		self.MODEM.write('AT+CMGL="REC READ"\r\n')
		time.sleep(1.5)
		respuesta = self.LeerBufferSMS()
		#Identificamos la Respuesta
		self.Imprimir(str(respuesta))
		#Tomamos el Largo de la respuesta
		largorespuesta = len(respuesta)
		p1 = False
		mensajesarreglados = []
		#Acomodamos los Mensajes
		for i in range(largorespuesta):
			if re.match("\+CMGL",(respuesta[i-1])):
				parte1 = respuesta[i-1]
				p1 = True
			elif p1 == True:
				completo =  parte1 + "," + respuesta[i-1]
				mensajesarreglados.append(completo)
				p1 = False
			else:
				pass
		#Tomamos lo que nos interesa y lo insertamos en la interfaz y BD o Texto
		#Depende del Modo [Consultar globalvars]
		#Creamos lista index en blanco.
		listaindex = []
		for i in mensajesarreglados:
			todosms = i.split(",")
			index = int(todosms[0].replace("+CMGL:",""))
			telefono = str(todosms[2].replace('"',''))
			fecha = str(todosms[4].replace('"',''))
			hora = str(todosms[5].replace('"',''))
			mensaje = str(todosms[6])
			self.AddTabMensajeRecibido(telefono,mensaje)
			#Lista de Index para despues borrarlas
			listaindex.append(str(index))
			#Si estamos trabajando con Base de Datos:
			if globalvars.Modo == "1":
				now = datetime.datetime.now()
				mensajeparabd = ['0','0',telefono,mensaje,now,'0',str(self.NumPuerto)]
				globalvars.ColaRecibidos.append(mensajeparabd)
			#Si esta en Modo 2 o 3, [Consultar Globalvars]
			else:
				pass
		#Solo si hay mensajes los borro
		if len(listaindex) >= 1:
			#Ahora Mandamos a borrar todos los mensajes que recibimos
			self.VaciarMemoriaSMS(listaindex)
		else:
			pass



	
	def EnviarCTRLZ(self):
		self.MODEM.write(chr(26)+"\r\n")
		time.sleep()
	def VaciarMemoriaSMS(self,listaindex):

		#self.Imprimir('Delete Incoming Messages')
		for i in listaindex:
			self.Imprimir("Delete Incoming Messages (" +str(i)+")" )
			self.MODEM.write("AT+CMGD=%s\r\n"%i)
			time.sleep(1.2)
			respuesta = self.LeerBuffer()
			self.Imprimir(str(respuesta))
			#if "OK" in respuesta:
			#	return "OK"
			#elif "ERROR" in respuesta:
			#	return "OK"
	def EnviarSMS(self):
		mensajeytelefono = globalvars.ColaparaEnviar.pop(0)
		self.Imprimir("SENDING SMS: "+ str(mensajeytelefono))
		mensajeytelefono = mensajeytelefono.split("|")
		telefono = mensajeytelefono[0]
		mensaje = mensajeytelefono[1]
		pk = mensajeytelefono[2]
		intento = 1
		while intento <= 3:
			self.MODEM.write('AT+CMGS="%s"\r\n' %str(telefono))
			time.sleep(1)
			self.MODEM.readline()
			completo = ""
			while True:
				caracter = self.MODEM.read()
				completo = completo + caracter
				if caracter == "\x20":
					break
			self.Imprimir(completo)
			self.MODEM.write(str(mensaje)+chr(26)+"\r\n")
			while self.MODEM.inWaiting() <= 6:
				time.sleep(0.1)
				pass
			respuesta = self.LeerBuffer()
			self.Imprimir(str(respuesta))
			for i in respuesta:
				if re.match("\+CMS ERROR",i):
					enviado = False
					intento = intento + 1
					GuardarTXTObjeto.GuardarErrorLog(self.NumPuerto,str(respuesta)+" IntentoSMS = "+str(intento),mensaje)

					#Si van 3 intentos fallidos, se suma a fallidosseguidos
					if intento == 4:
						self.FallidosSeguidos = self.FallidosSeguidos + 1
						#Verificamos si van 10 Fallidos Seguidos para cambiar Status Modem
						if self.FallidosSeguidos == 10:
							#Enviamos el Status al Label
							self.StatusToLabel("ERROR")
							#Cambiamos el Status para Detener
							self.Status = "ERROR"
						break

					self.Imprimir("Error Sending SMS...Notificate Email Administrator...")
					self.Imprimir("Waiting...")
					time.sleep(4)

				elif re.match("\+CMGS",i):
					enviado =  True
					intento = 4
					#En caso de enviar un SMS, se coloca en 0 fallidosseguidos
					self.FallidosSeguidos = 0
					break
				else:
					#En caso de que no responda algo esperado
					enviado = False
					intento = intento + 1
					#Si van 3 intentos fallidos, se suma a fallidosseguidos
					if intento == 4:
						self.FallidosSeguidos = self.FallidosSeguidos + 1
						#Verificamos si van 10 Fallidos Seguidos para cambiar Status Modem
						if self.FallidosSeguidos == 10:
							#Enviamos el Status al Label
							self.StatusToLabel("ERROR")
							#Cambiamos el Status para Detener
							self.Status = "ERROR"
		#Si el PK es simulado es un mensaje simulado que no se guarda. Solo se envia
		if enviado == True and pk != "Simulado":
			self.AddTabMensajeEnviado(telefono,mensaje,pk)
			globalvars.ColaEnviados.append(str(mensajeytelefono[2]))
		elif enviado == False and pk != "Simulado":
			self.AddTabMensajeFallido(telefono,mensaje,pk)
			globalvars.ColaFallidos.append(str(mensajeytelefono[2]))
	def proceso(self):
		try:
			#Enviamos CTRLZ por quedo enviando SMS, Manual con un TimeSleep para Esperar una respuesta mas tiempo
			self.MODEM.write(chr(26)+"\r\n")
			time.sleep(5)
			#Si hay algo en el Buffer, lo leemos
			if self.MODEM.inWaiting() >= 1:
				self.LeerBuffer()
			else:
				pass
			#Verificamos que quitamos el ECHO
			if self.QuitarEcho() == "OK":
				#Colocamos los Errores Completos
				self.ActivarTextoErrores()
				#Verificamos el Estado de la SIM en el Equipo
				if self.DameEstadoSIM() == "OK":
					#Verificamos si estamos Conectados a la Operadora
					if self.EstasRegistrado() == "OK":
						#Verificamos a que Operador estamos registrados
						self.DameOperadora()
						#Verificamos el nivel de señal del equipo
						if self.DameSenal() == "OK":
							#Activamos el Modo Texto
							if self.ActivarSMSTexto() == "OK":
								self.DameMarca()
								self.DameModelo()
								self.DameVersion()
								self.DameIMEI()
								self.DameBateria()
								#Envio la informacion para la StatusBar
								self.AddInfoStatusBar(self.Marca,self.Modelo,self.Version,self.OPERADORA,self.IMEI)
								#Vacio la Memoria de SMS
								#self.VaciarMemoriaSMS()
								#Coloco el Modem en Status OK
								self.Status = "OK"
								#Colocamos el Status en el Label
								self.StatusToLabel("OK")
								self.emit(QtCore.SIGNAL("signalCrearServer"))
								cont = 0
								while True:
                                                                        cont = cont + 1
									if self.Status == "OK":
										if len(globalvars.ColaparaEnviar) >= 1:
											#Enviamos Mensajes
											self.EnviarSMS()
										else:
											if len(globalvars.ColaGeneral) >= 1:
												#if self.Master == True:
													if len(globalvars.ColaGeneral) >= 10:
														for i in range(5):
															globalvars.ColaparaEnviar.append(globalvars.ColaGeneral.pop(0))														
													else:
														globalvars.ColaparaEnviar.append(globalvars.ColaGeneral.pop(0))
													self.AddTabMensajeCola()
													#Para que de tiempo de colocar la cola en la interfaz
													time.sleep(1)
											else:
												self.Imprimir("Read SMS....OK")
												self.LeerSMS()
												if cont == 1: self.AddInfoStatusBar(self.Marca,self.Modelo,self.Version,self.OPERADORA,self.IMEI)
												#Pedimos la senal para comprobar que tengamos
												while True:
													senal = self.DameSenal()
													if senal == "OK":
														break
													else:
														self.Imprimir("Not signal operator")
														pass
														time.sleep(1)
											#time.sleep(4)
									elif self.Status == "ERROR":
										#Solo detiene el Cliente si es Tipo Cliente, si es Server sigue corriendo
										#Asi no pueda enviar mensajes.
										if self.Master == False:
											self.emit(QtCore.SIGNAL("signalDetenerCliente"))
										self.Imprimir("Notificate Error Send Email...")
										break
							else:
								#No se pudo activar Modo Texto
								self.Imprimir("Error 1521") 
						else:
							#No tiene Senal el Modem
							self.Imprimir("Error 1522") 
					else:
						#Problema con la Operadora, No la Consigue
						self.Imprimir("Error 1523") 
				else:
					#Problema con la SIMCARD
					self.Imprimir("Error 1524") 
			else:
				#No se pudo eliminar el ECHO
				self.Imprimir("Error 1525") 
		except Exception as exc:
			excepcion = str(exc)
			GuardarTXTObjeto.GuardarErrorLog(self.NumPuerto,"Not Comunicate Device... "+str(traceback.format_exc()))
			self.Imprimir("Not Comunicate Device...")

