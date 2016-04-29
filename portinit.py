import serial
from PyQt4 import QtCore
from modem import Modem_HuaweiUSB, Modem_EnforaSerial
from globalvars import *

class Puertos(QtCore.QThread):
	def __init__(self,num_puerto,baudrate,bitesize,parity,stopbits,modem):
		QtCore.QThread.__init__(self)
		self.num_puerto = int(num_puerto)
		self.baudrate = int(baudrate)
		self.bitesize = eval(bitesize)
		self.parity = eval(parity)
		self.stopbits = eval(stopbits)
		self.modem = int(modem)
	def asignar(self):
		#try:
			self.puerto = serial.Serial(self.num_puerto-1,self.baudrate,self.bitesize,self.parity,self.stopbits)
			PuertosCorriendoCOM[self.num_puerto] = self.puerto
			PuertosparaTabs.append(self.puerto)
			self.estadopuerto = True
			print "Puerto Asignado"
			print self.puerto
		#except:
			#print 'No se pudo asignar el puerto ' + str(self.num_puerto)

	def run(self):
		self.asignar()
		#try:
		if self.modem == 1:
			HUAWEIUSB = Modem_HuaweiUSB(self.num_puerto)
			listademodems['HUAWEIUSB'+str(self.num_puerto)] = HUAWEIUSB
			print "Modem Seleccionado, HUAWEIUSB"
			listademodems['HUAWEIUSB'+str(self.num_puerto)].proceso(self.puerto)
		elif self.modem == 2:
			ENFORASERIAL = Modem_EnforaSerial(self.num_puerto)
			listademodems['ENFORASERIAL'+str(self.num_puerto)] = ENFORASERIAL
			print "Modem Seleccionado, ENFORASERIAL"
			listademodems['ENFORASERIAL'+str(self.num_puerto)].proceso(self.puerto)

		#except:
		#	print 'No se pudo comenzar la escucha, verifica que el puerto ' + str(self.num_puerto) + ' esta disponible'