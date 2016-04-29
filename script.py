import serial
import time
import re

ser = serial.Serial(2,115200,serial.EIGHTBITS,serial.PARITY_NONE,serial.STOPBITS_ONE)

def Leer():
    #while True:
        #envio = raw_input("Escriba lo que le enviara al Modem")
        #ser.write(envio+"\r\n")
        time.sleep(2)
        todalarespuesta = []
        while ser.inWaiting() >= 1:
            respuesta = ser.readline()
            if respuesta == "\r\n":
                pass
            elif re.match("\+CMTI",respuesta):
                pass
            else:
                respuesta = respuesta.replace("\r","")
                respuesta = respuesta.replace("\n","")
                todalarespuesta.append(respuesta)
        print todalarespuesta

def EnviarSMS():
    telefono = raw_input("Dame Telefono ")
    ser.write('AT+CMGS="%s"\r\n' %telefono)
    time.sleep(1)
    ser.readline()
    completo = ""
    while True:
        caracter = ser.read()
        completo = completo + caracter
        if caracter == "\x20":
            break
    mensaje = raw_input("Dame el Mensaje")
    ser.write(mensaje+chr(26)+"\r\n")
    time.sleep(5)
    Leer()
    





EnviarSMS()
