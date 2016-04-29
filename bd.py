#Importamos el Modulo Pyodbc para conexion con la base de datos
import pyodbc
#Importamos el modulo para archivos INI
from ConfigParser import ConfigParser
#Importamos Desencriptador XOR Pycrypto
from Crypto.Cipher import XOR
import base64

class BasedeDatos(object):
	def __init__(self):
		self.resultado = None
		#Buscando el archivo INI para saber el String de Conexion
		config = ConfigParser()
		config.read("Conect.dat")
		self.conexioncifrada = config.get('DB', 'StringDB')
		PASSWORD = XOR.new(base64.b64decode('MjAxMDE3MzMtOTYwOTkyNg=='))
		self.conexion = PASSWORD.decrypt(base64.b64decode(str(self.conexioncifrada)))
		self.conexion = 'Driver={SQL Server Native Client 11.0};Server=AXNER-HP\JERMSOFT;Database=365DB_2;Uid=sa;Pwd=jerm'

	def Conectar(self):
		self.cnxn = pyodbc.connect(self.conexion)
		self.cursor = self.cnxn.cursor()
	def Seleccionar(self,query):
		self.cursor.execute(query)
		rows = self.cursor.fetchall()
		self.resultado = rows
		return self.resultado
	def SeleccionarUno(self,query,dato):
		self.cursor.execute(query,dato)
		row = self.cursor.fetchone()
		self.resultado = row
		return self.resultado

	def Insertar(self,query,datos):
		self.cursor.execute(query,datos)
		self.cnxn.commit()
	def Actualizar(self,query,*datos):
		self.cursor.execute(query,datos)
		self.cnxn.commit()
	def Borrar(self,query,dato):
		self.cursor.execute(query,dato)
		self.cnxn.commit()





