from ConfigParser import ConfigParser
#Importamos Desencriptador XOR Pycrypto
from Crypto.Cipher import XOR
import base64
import string

class NumAdmins(object):
	def __init__(self):
	#Buscando el archivo INI para saber la configuracion del formato de numeros
		self.config = ConfigParser()
		self.config.read("conf/config.ini")
		self.numsenc = self.config.get('MODEMS', 'nums')
		self.Cipher = XOR.new(base64.b64decode('MjAxMDE3MzMtOTYwOTkyNg=='))
		self.nums = self.Cipher.decrypt(base64.b64decode(str(self.numsenc)))
		self.nums = self.nums.split(",")
		self.dictnums = {}
		letra = 0
		for n in self.nums:
			self.dictnums[str(string.lowercase[letra])]=n
			letra = letra + 1


NumAdminsObjeto = NumAdmins()



