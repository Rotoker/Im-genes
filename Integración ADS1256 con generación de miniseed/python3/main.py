#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
import ADS1256
import RPi.GPIO as GPIO
try:
    ADC = ADS1256.ADS1256()
    ADC.ADS1256_init()
    ADC.ADS1256_ConfigADC(ADS1256.ADS1256_GAIN_E['ADS1256_GAIN_1'], ADS1256.ADS1256_DRATE_E['ADS1256_30000SPS'])
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(5, GPIO.OUT)
    #start_time=time.time()
    total_samples = 0
    
    while (1):
            #current_time = time.time()
        #110 1101 0110 1010 0001 0000 Ej para 1k mps
        #110 1101 1101 1001 0011 0011 Ej para 30k mps
        #110 1101 1110 0011 0001 1111 Ej para 2.5 mps
            while total_samples < 600:
                    ADC_Value = ADC.ADS1256_Get3()
                    #ENE, ENN, ENZ (X,Y,Z)
                    
                    #print("0 ADC = {:b}".format(ADC_Value[0]))
                    #print("1 ADC = %lf" % (ADC_Value[1]* 5.0 / 0x7fffff))
                    #print("2 ADC = %lf" % (ADC_Value[2]))
                    #print("2 ADC = %lf" % (ADC_Value[2] * 5.0 / 0x7fffff))
                    total_samples += 3  # Increment by 3 since we're sampling three channels
                    if total_samples == 600:
                        GPIO.output(5, GPIO.HIGH)
                        #elapsed_time = current_time - start_time
                        print("Samples = %lf" % (total_samples))
                        #print("Acquisition time: ", time.time()-start_time)
                        total_samples = 0
                    else:      
                        GPIO.output(5,GPIO.LOW)      
except :
    GPIO.cleanup()
    print ("\r\nProgram end     ")
    exit()

