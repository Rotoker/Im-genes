#Progrma con comunicacion UART
import serial
import time
from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO
import numpy
from obspy.core import Trace,Stream,UTCDateTime
import random #Para hacer pruebas con datos aleatorios
import time  #Para generar retardos
#Retira el prefijo '0B' y convierte la cadena en un entero
def bytes_to_int(bin_str):
    entero = int(bin_str[2:], 2)
    return entero
#Funcion para convertir bytes a entero (codificacion datos enviados)
#def bytes_to_int(bytes):
 #   result = 0
  #  for b in bytes:
   #     result = result * 256 + int(b)
    #return result

#def bytes_to_int(bytes):
#    for b in bytes:
#        result=(bytes[2]>>0) | (bytes[1] >> 0) | (bytes[0]>>0);
#    return result
#Función para generar 3 bytes
def genera_dato_3_bytes():
    numero_aleatorio = random.randint(0, 2**24)
    numero_binario = f'0B{numero_aleatorio:024b}'
    return numero_binario
#Puerto
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(38, GPIO.OUT)
#GPIO.output(38, True) #aqui se encendia un led , pero no es necesario

#Habilitacion puerto UART
datapoints=112    # Se definen 112 muestras que se van a tomar, esto para un archivo miniseed que va a contener 112 datos enteros de 32 bits
seq = 1        # El número de secuencia de archivo miniseed inicial es 1
data= numpy.zeros((datapoints,3),dtype=numpy.int32) #se crea un array de 112 x 3 (112 muestras por canal ENE, ENN, ENZ)
#ser = serial.Serial ("/dev/ttyS0", 256000)    #Open port with baud rate
print('Iniciando sensado')

#se hace la lectura iniciar, la cual tiene datos incompletos, sin embargo esta lectura no se guardará en el archivo miniseed
convertidor_1=genera_dato_3_bytes()
convertidor_2=genera_dato_3_bytes()
convertidor_3=genera_dato_3_bytes()
starttime=UTCDateTime()

while True:

  starttime=starttime + 0.56 #los 0.56s son el tiempo que tarda en guardar las 112 muestras.
  fecha = str(starttime)[0:13] +"-"+str(starttime)[14:22] #obtenemos del caracter 0a 13 y del 14 al 22, esto para darle formato   
  for x in range(datapoints):  #112 veces, 112 muestras
    #Lectura convertidores
    convertidor_1 = genera_dato_3_bytes()# Hacemos las lecturas de los convertidores
    convertidor_2 = genera_dato_3_bytes()
    convertidor_3 = genera_dato_3_bytes()
    conv1 = convertidor_1
    conv2 = convertidor_2
    conv3 = convertidor_3
    #Decodificacion bytes
    conv_1 = bytes_to_int(conv1) & 0x1FFFFF #convertimos de bytes a entero y enmascaramos los 3 bits mas significativos
    conv_2 = bytes_to_int(conv2) & 0x1FFFFF
    conv_3 = bytes_to_int(conv3) & 0x1FFFFF
    data[x,0]=conv_1 #almacenamos en el arreglo previamente generado con numpy
    data[x,1]=conv_2
    data[x,2]=conv_3
  final= seq + 1
 #esto va fuera del for, aqui ya tenemos data para 1 archivo miniseed, podemos aumentar el numero de registro miniseed, para el sig archivo
  path = 'miniseed/' 
#definimos la variable con la direccion raiz en donde queremos que se almacene el archivo miniseed, en este caso en la carpeta miniseed que esta donde se ejecuta este código
  ENE = path + 'ENE['+fecha+'].mseed' 
#se genera un string con la ruta del archivo, la cual incluye el nombre del archivo, aqui se nombra al archivo y se indica el path previamente definido
  #definimos las varianbles de header de nuestro miniseed en stats
  stats= {'network': 'II','station': 'RASPB','location': '01','channel': 'ENE','npts': datapoints,'sampling_rate': '200',
          'mseed' : {'dataquality' : 'D'},'starttime': starttime}
  #convertimos los stats a un stream, le pasamos la parte dle arreglo que contiene ENE, y el header que definimos
  stream =Stream([Trace(data=data[:,0], header=stats)])
  #el archivo miniseed se guarda con las caracteristicas indicadas
  stream.write(ENE,format='MSEED',flush=True,reclen=512,byteorder=1,encoding='INT32',verbose=1,sequence_number=seq)
# stream.plot() #descomentar para que tambien haga un plot de los datos miniseed
  
  #lo mismo que ENE pero para ENN
  ENN = path+'ENN['+fecha+'].mseed'
  stats= {'network': 'II','station': 'RASPB','location': '01','channel': 'ENN','npts': datapoints,'sampling_rate': '200',
        'mseed' : {'dataquality' : 'D'},'starttime': starttime}
  stream =Stream([Trace(data=data[:,1], header=stats)])
  stream.write(ENN,format='MSEED',flush=True,reclen=512,byteorder=1,encoding='INT32',verbose=1,sequence_number=1)
#  stream.plot()
  
  #lo mismo que ENE pero para ENZ
  ENZ = path+'ENZ['+fecha+'].mseed'
  stats= {'network': 'II','station': 'RASPB','location': '01','channel': 'ENZ','npts': datapoints,'sampling_rate': '200',
          'mseed' : {'dataquality' : 'D'},'starttime': starttime}
  stream =Stream([Trace(data=data[:,2], header=stats)])
  stream.write(ENZ,format='MSEED',flush=True,reclen=512,byteorder=1,encoding='INT32',verbose=1,sequence_number=1)
  #stream.plot()
  seq = final
  print('Archivo '+ ENE+' generado.')
  print('Archivo '+ ENN+' generado.')
  print('Archivo '+ ENZ+' generado.')
  time.sleep(5)
#GPIO.output(38, False)

