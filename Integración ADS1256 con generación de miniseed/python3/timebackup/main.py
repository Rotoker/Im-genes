import numpy as np
import matplotlib.pyplot as plt
import time
import os
import ADS1256
import RPi.GPIO as GPIO
import config

def read_data():
    ADC.ADS1256_WaitDRDY()
    buf = config.spi_readbytes(3)
    
    read = (buf[0] << 16) & 0xff0000
    read |= (buf[1] << 8) & 0xff00
    read |= buf[2] & 0xff
    
    if read & 0x800000:
        read = -(0xffffff - read +1)
    return read * 5.0 / 0x7fffff
    
 ####### MAIN CODE ##########
    
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.OUT)  # imposta numero pin output
GPIO.setup(26, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
  
ADC = ADS1256.ADS1256()
fs = 50 #15KHz
signal =[]
  
ADC.ADS1256_reset()
gain = ADS1256.ADS1256_GAIN_E['ADS1256_GAIN_1']
drate = ADS1256.ADS1256_DRATE_E['ADS1256_50SPS']
channel = 2
ADC.ADS1256_init(gain,drate,channel)  # inizializzazione
ADC.ADS1256_WriteCmd(ADS1256.CMD['CMD_SYNC'])
ADC.ADS1256_WriteCmd(ADS1256.CMD['CMD_WAKEUP'])
ADC.ADS1256_WaitDRDY() 
    
config.digital_write(config.CS_PIN, GPIO.LOW)  # CS 0
config.spi_writebyte([ADS1256.CMD['CMD_RDATAC']])
config.digital_write(config.CS_PIN, GPIO.HIGH)  # CS 1
time.sleep(7/10000) 
    
config.digital_write(config.CS_PIN, GPIO.LOW)  # cs  0
start_time = time.time()
     
while len(signal)<=50*fs:
    
    signal.append(read_data())
    print("Acquisition time: ", time.time()-start_time) 