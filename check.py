#Importamos el modulo para archivos INI
from ConfigParser import ConfigParser
#Importamos Desencriptador XOR Pycrypto
from Crypto.Cipher import XOR
import base64
#Importamos getmac
from getmac import mac

	
def LicCheck():
	config = ConfigParser()
	config.read("conf/config.ini")
	LicCif = config.get('CUENTA', 'Lic')
	contrasena = base64.b64decode('MjAxMDE3MzMtOTYwOTkyNg==')
	PASSWORD = XOR.new(str(contrasena))
	try:
		#Por si da algun error en la decodificacion
		LicDecif = PASSWORD.decrypt(base64.b64decode(str(LicCif)))
	except:
		LicDecif = None
	if str(mac) == str(LicDecif):
		return True
	else:
		if LicDecif == None:
			Salida = "[LICENCIA. ERROR TIPO1] Contacte al +584142788259"
		else:
			Salida = "[LICENCIA. ERROR TIPO2] Contacte al +584142788259"
		return True

		
def ModoCheck():
	config = ConfigParser()
	config.read("conf/config.ini")
	ModoCif = config.get('CUENTA', 'Modo')
	contrasena = base64.b64decode('MjAxMDE3MzMtOTYwOTkyNg==')
	PASSWORD = XOR.new(str(contrasena))
	try:
		#Por si da algun error en la decodificacion
		Modo = PASSWORD.decrypt(base64.b64decode(str(ModoCif)))
		if Modo == '1':
			return Modo
		elif Modo == '2':
			return Modo
	except:
		Salida = "[LICENCIA. ERROR TIPO3] Contacte al +584142788259"
		Modo = None
		return Modo
