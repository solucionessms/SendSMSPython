from date import LaFecha
import os

class GuardarTXT(object):
	def __init__(self):
		pass
	def GuardarErrorLog(self,modem=None,comando=None,sms=None):
		dia = LaFecha.damedia()
		fecha = LaFecha.damefecha()
		filename = 'Log/'+str(modem)+"-"+str(dia)+'ErrorLog.dat'
		if not os.path.exists(os.path.dirname(filename)):
		    try:
		        os.makedirs(os.path.dirname(filename))
		    except OSError as exc: # Guard against race condition
		        if exc.errno != errno.EEXIST:
		            raise
		self.SMSFail=open(filename,'a')
		self.SMSFail.write(str(comando)+' - '+str(sms)+' - '+str(modem)+' - '+str(fecha)+"\n")
		print str(comando)+' - '+str(sms)+' - '+str(modem)+' - '+str(fecha)+"\n"
		self.SMSFail.close()


GuardarTXTObjeto = GuardarTXT()


