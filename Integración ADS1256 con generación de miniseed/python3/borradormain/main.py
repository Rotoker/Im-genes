import ADS1256
import RPi.GPIO as GPIO

ADC = ADS1256.ADS1256()
ADC.ADS1256_init()
ADC.ADS1256_ConfigADC(ADS1256.ADS1256_GAIN_E['ADS1256_GAIN_1'], ADS1256.ADS1256_DRATE_E['ADS1256_30000SPS'])

total_muestras = 0

def interrupt(channel):
    global total_muestras
    total_muestras += 1
    ADC_Value = ADC.ADS1256_GetChannalValue()
    print(f'Conversión lista: {total_muestras}')
    
GPIO.add_event_detect(17, GPIO.FALLING, callback=interrupt, bouncetime=1)