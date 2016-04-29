from check import BDCheck

global Modo
Modo = BDCheck()

global ColaGeneral
ColaGeneral = []
global ColaparaEnviar
ColaparaEnviar = []
global ColaEnviados
ColaEnviados = []
global ColaFallidos
ColaFallidos = []
global CantidadporModem
CantidadporModem = 5
ModemsConectados = []

nombresPySerial = {'BiteSize': {'5':'serial.FIVEBITS','6':'serial.SIXBITS','7':'serial.SEVENBITS','8':'serial.EIGHTBITS'}, 'Parity': {'N':'serial.PARITY_NONE','E':'serial.PARITY_EVEN','O':'serial.PARITY_ODD','M':'serial.PARITY_MARK'}, 'StopBits': {'1':'serial.STOPBITS_ONE','1.5':'serial.STOPBITS_ONE_POINT_FIVE','2':'serial.STOPBITS_TWO'}}

