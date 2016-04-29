from check import ModoCheck

#Variable para conocer el Modo
#1 - Base de Datos SMSAlarmas
#2 - StandAlone Archivo Config
#3 - Argumentos al ejecutable
def initvars():
	global Modo
	Modo = ModoCheck()
	global ColaGeneral
	ColaGeneral = []
	global ColaRecibidos
	ColaRecibidos = []
	global ColaparaEnviar
	ColaparaEnviar = []
	global ColaEnviados
	ColaEnviados = []
	global ColaFallidos
	ColaFallidos = []
	global ModemsConectados
	ModemsConectados = []
	global CantidadporModem
	CantidadporModem = 0
	global nombresPySerial
	nombresPySerial = {'BiteSize': {'5':'serial.FIVEBITS','6':'serial.SIXBITS','7':'serial.SEVENBITS','8':'serial.EIGHTBITS'}, 'Parity': {'N':'serial.PARITY_NONE','E':'serial.PARITY_EVEN','O':'serial.PARITY_ODD','M':'serial.PARITY_MARK'}, 'StopBits': {'1':'serial.STOPBITS_ONE','1.5':'serial.STOPBITS_ONE_POINT_FIVE','2':'serial.STOPBITS_TWO'}}

