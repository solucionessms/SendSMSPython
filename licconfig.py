from Crypto.Cipher import XOR
from base64 import b64encode, b64decode
from getpass import getpass
import uuid
from time import sleep
from socket import gethostname
from ConfigParser import ConfigParser

def CualBD():
    while True:
        print 'Indique la version de BD'
        print '1 - SQL2000'
        print '2 - SQL2005'
        print '3 - SQL2008'
        print '4 - SQL2012'
        print '5 - SQL2014'
        cualbd = raw_input('Indique: ')
        if int(cualbd) <= 5:
            if cualbd == '1':
                stringdb = 'DRIVER={SQL Server};SERVER=NOMBREPC;DATABASE=NOMBREBD;UID=USUARIOBD;PWD=PASSWORDBD'
            elif cualbd == '2':
                stringdb = 'Driver={SQL Native Client};Server=NOMBREPC;Database=NOMBREBD;Uid=USUARIOBD;Pwd=PASSWORDBD'
            elif cualbd == '3':
                stringdb = 'Driver={SQL Server Native Client 10.0};Server=NOMBREPC;Database=NOMBREBD;Uid=USUARIOBD;Pwd=PASSWORDBD'
            elif cualbd == '4':
                stringdb = 'Driver={SQL Server Native Client 11.0};Server=NOMBREPC;Database=NOMBREBD;Uid=USUARIOBD;Pwd=PASSWORDBD'
            elif cualbd == '5':
                stringdb = 'Driver={SQL Server Native Client 11.0};Server=NOMBREPC;Database=NOMBREBD;Uid=USUARIOBD;Pwd=PASSWORDBD'
            return stringdb
        else:
            print 'La opcion no es valida'


def ConvertirDatos(stringbd,lic,cualmodo,dondebd):
    print 'Convirtiendo Datos'
    if dondebd == '1':
        stringbd = stringbd.replace('NOMBREPC',str(gethostname()))
    elif dondebd == '2':
        print 'Indique la direccion donde se encuentra la Base de Datos' 
        direccionremota = raw_input('Indique una direccion IP o un DNS para la conexion a Base de Datos: ')
        stringbd = stringbd.replace('NOMBREPC',direccionremota)
    while True:
        print 'Indique si programara Modems'
        print '1 - SI'
        print '2 - NO'
        simodem = raw_input('Indique: ')
        numerosvalidos = []
        if simodem == '1':
            progmodem = 1
            break
        elif simodem == '2':
            progmodem = 2
            break
        else:
            print 'La opcion no es valida'
    if progmodem == 1:
        while True:
            print 'Indique un identificador de numeros validos'
            num = raw_input('Indique: ')
            numerosvalidos.append(num)
            print 'Desea Programar otro identificador?'
            print '1 - SI'
            print '2 - NO'
            otroident = raw_input('Indique: ')
            if otroident == '1':
                pass
            elif otroident == '2':
                progotroiden = 2
                break
            else:
                print 'La opcion no es valida'
    while True:
        print 'Indique el largo de los numeros telefonicos en digitos'
        lennums = raw_input('Indique: ')
        if lennums.isdigit():
            break
        else:
            print 'Debe indicar un numero para el largo'
    print 'Programe el servidor Web'
    print 'Indique la direccion, recuerde tomar en cuenta colocar el puerto en caso de no ser el 80'
    while True:
        direccionweb = raw_input('Indique: ')
        print 'Indico la direccion: ' + str(direccionweb)
        print 'Desea Mantenerla?'
        print '1 - SI'
        print '2 - NO'
        respweb = raw_input('Indique: ')
        if respweb == '1':
            break
        elif respweb == '2':
            pass
        else:
            print 'La opcion no es valida'
    numpruebarapida = []
    while True:
        print 'Indique un numero para prueba rapida de SMS'
        numrapid = raw_input('Indique: ')
        if numrapid.isdigit():
            numpruebarapida.append(numrapid)
        else:
            print 'Indique un numero valido'
        print 'Desea agregar otro numero?'
        print '1 - SI'
        print '2 - NO'
        respmasnum = raw_input('Indique: ')
        if respmasnum == '1':
            pass
        elif respmasnum == '2':
            break
        else:
            print 'Indique una respuesta valida'

    numvalid = str(lennums)
    for num in numerosvalidos:
        numvalid = numvalid +','+num
    numsrapida = ''
    for numpruba in numpruebarapida:
        if numsrapida == '':
            numsrapida = numsrapida + '' + numpruba
        else:
            numsrapida = numsrapida + ',' + numpruba

    stringbd = stringbd.replace('NOMBREBD','Soluciones-SMSSecure')
    stringbd = stringbd.replace('USUARIOBD','sa')
    stringbd = stringbd.replace('PASSWORDBD','jerm')
    deco = XOR.new(b64decode('MjAxMDE3MzMtOTYwOTkyNg=='))
    stringbd =  b64encode(deco.encrypt(str(stringbd)))
    deco = XOR.new(b64decode('MjAxMDE3MzMtOTYwOTkyNg=='))
    lic =  b64encode(deco.encrypt(str(lic)))
    deco = XOR.new(b64decode('MjAxMDE3MzMtOTYwOTkyNg=='))
    cualmodo =  b64encode(deco.encrypt(str(cualmodo)))
    deco = XOR.new(b64decode('MjAxMDE3MzMtOTYwOTkyNg=='))
    numerosvalidos =  b64encode(deco.encrypt(str(numvalid)))
    deco = XOR.new(b64decode('MjAxMDE3MzMtOTYwOTkyNg=='))
    lennums =  b64encode(deco.encrypt(str(lennums)))
    deco = XOR.new(b64decode('MjAxMDE3MzMtOTYwOTkyNg=='))
    numpruebarapida =  b64encode(deco.encrypt(str(numsrapida)))
    deco = XOR.new(b64decode('MjAxMDE3MzMtOTYwOTkyNg=='))
    direccionweb =  b64encode(deco.encrypt(str(direccionweb)))


    print 'Datos Convertidos'
    CrearArchivo(stringbd,lic,cualmodo,numerosvalidos,numpruebarapida,direccionweb)

def CrearArchivo(stringbd,lic,cualmodo,numerosvalidos,numpruebarapida,direccionweb):
        print 'Creando Archivo'
    #try:
        cfgfile = open("conf/config.ini",'w')
        Config = ConfigParser()
        Config.add_section('BASE DE DATOS')
        Config.set('BASE DE DATOS','Conexion',stringbd)
        Config.add_section('CUENTA')
        Config.set('CUENTA','Lic',lic)
        Config.set('CUENTA','Modo',cualmodo)
        Config.add_section('MODEMS')
        Config.set('MODEMS','formatos',numerosvalidos)

        Config.set('MODEMS','nums',numpruebarapida)
        Config.add_section('WEB')
        Config.set('WEB','srv',direccionweb)
        Config.write(cfgfile)
        print 'Archivo Creado'
        cfgfile.close()
    #except:
    #   print 'Error de Ubicacion'


##################################################################################


print 'Configurador de Licencia 365'
usuarioiniciar = raw_input('Usuario: ')
passwordiniciar = getpass(prompt='Contrasena: ')
if usuarioiniciar == '' and passwordiniciar == b64decode('MjAxMDE3MzMtOTYwOTkyNg=='):
    while True:
        print 'Indique el MODO del Receptor'
        print '1 - BD'
        print '2 - StandAlone'
        cualmodo = raw_input('Indique: ')
        if cualmodo == '1' or cualmodo == '2':
            break
        else:
            print 'La opcion no es valida'
    #MODO BASE DE DATOS
    if cualmodo == '1':
        while True:
            print 'Indique si la base de datos es Local o Remota'
            print '1 - Local'
            print '2 - Remota'
            dondebd = raw_input('Indique: ')
            if dondebd == '1' or dondebd == '2':
                break
            else:
                print 'La opcion no es valida'
        if dondebd == '1':
            stringbd = CualBD()
        elif dondebd == '2':
            stringbd = CualBD()
    #MODO STANDALONE
    elif cualmodo == '2':
        dondebd = False
        stringbd = 'NoHayBaseDeDatos'
    lic = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])



       



    print 'Introduza la clave Generadora de Licencia'
    clavegeneradora = getpass(prompt='Indique: ')
    if clavegeneradora == b64decode('OTYwOTkyNi0yMDEwMTczMw=='):
        print 'Generando Datos'
        sleep(1)
        print 'Datos Generados'
        ConvertirDatos(stringbd,lic,cualmodo,dondebd)
        
        
    
        
            
        
        
