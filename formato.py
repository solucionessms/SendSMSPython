import re
from ConfigParser import ConfigParser
#Importamos Desencriptador XOR Pycrypto
from guardarlog import GuardarTXTObjeto
from Crypto.Cipher import XOR
import base64

class ValidarNumero(object):
	def __init__(self):
	#Buscando el archivo INI para saber la configuracion del formato de numeros
		self.config = ConfigParser()
		self.config.read("conf/config.ini")
		self.formatoenc = self.config.get('MODEMS', 'formatos')
		self.Cipher = XOR.new(base64.b64decode('MjAxMDE3MzMtOTYwOTkyNg=='))
		self.formato = self.Cipher.decrypt(base64.b64decode(str(self.formatoenc)))
		self.formatos = self.formato.split(",")
		self.largo = self.formatos.pop(0)

	def Validar(self,numero):
		self.numero = numero
		#len(self.numero) == int(self.largo)
		if True:
			for i in self.formatos:
				if re.match(i,self.numero):
					return "Ok"
                			break
		else:
			GuardarTXTObjeto.GuardarErrorLog("Movil Len Max..",str(self.numero))
			return "Ok" #None

Validar = ValidarNumero()
