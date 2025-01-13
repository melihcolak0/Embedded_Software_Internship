import machine
import time

# ADC pinini tanımla (GPIO26 veya GPIO27)
adc_pin = machine.Pin(27)  # Örneğin, GPIO26'yı kullanıyoruz

# ADC'yi başlat
adc = machine.ADC(adc_pin)

while True:
    # ADC'den okuma yap
    adc_value = adc.read_u16()
    
    # Okunan değeri gerilime çevir
    voltage = (adc_value * 3.3085) / 65535  # 12-bit çözünürlük ve 3.3V referans gerilim kullanıyoruz
    
    # Gerilimi yazdır
    print("Okunan Gerilim: {:.2f} V".format(voltage))
    
    # 0.1 saniye bekle
    time.sleep(0.1)

