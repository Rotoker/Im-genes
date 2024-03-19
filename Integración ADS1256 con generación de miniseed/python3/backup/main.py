#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
import ADS1256
import RPi.GPIO as GPIO

try:
    ADC = ADS1256.ADS1256()
    ADC.ADS1256_init()
    ADC.ADS1256_ConfigADC(ADS1256.ADS1256_GAIN_E['ADS1256_GAIN_1'], ADS1256.ADS1256_DRATE_E['ADS1256_30000SPS'])
    sample_interval = 1.0 / 600
    total_samples = 0
    start_time=time.time()
    while total_samples < 6000:
            current_time = time.time()
            elapsed_time = current_time - start_time
            
            if elapsed_time >= sample_interval:
                    ADC_Value = ADC.ADS1256_Get3()
                    print("0 ADC = %lf" % (ADC_Value[0]))
                    print("1 ADC = %lf" % (ADC_Value[1]))
                    print("2 ADC = %lf" % (ADC_Value[2]))
                    #print("2 ADC = %lf" % (ADC_Value[2] * 5.0 / 0x7fffff))
                    
                    start_time = current_time
                    total_samples += 3  # Increment by 3 since we're sampling three channels
                    print("Samples = %lf" % (total_samples))
                    print("Acquisition time: ", time.time()-start_time)
        
except :
    GPIO.cleanup()
    print ("\r\nProgram end     ")
    exit()

