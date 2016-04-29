from sendmail import EnviarEmailPlain
from pcinfo import PCInfo
from getmac import mac

def AvisodeApertura(lic):
	try:
		Asunto = 'Evento AlertSMS Abierto'
		informacion = PCInfo()
		Mensaje = 'AlertSMS abierto por la IP Publica= ' + str(informacion.ObtenerIPPublica()) + '\r\n' + 'Nombre del Equipo e IP Local= ' + str(informacion.ObtenerNombreIpLocal()) + '\r\n' + 'Direccion MAC= ' + str(mac) + '\r\n' + "Licencia= " + str(lic)
		EnviarEmailPlain('jermsoft@gmail.com',Asunto,Mensaje)
		#EnviarEmailPlain('vioren@gmail.com',Asunto,Mensaje)
	except:
		pass
