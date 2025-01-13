import machine
import utime

# PWM sinyali oluşturma
PWM_PIN = 2  # PWM sinyalini oluşturacağımız pin (örneğin GP2)
PWM_FREQ = 1000  # PWM sinyalinin frekansı (örneğin 1000 Hz)
DUTY_CYCLE = 50  # PWM sinyalinin görev döngüsü yüzdesi (örneğin %50)

pwm_sig = machine.PWM(machine.Pin(PWM_PIN))
pwm_sig.freq(PWM_FREQ)
pwm_sig.duty_u16(int(65535 * DUTY_CYCLE / 100))

# ADC oluşturma
adc = machine.ADC(machine.Pin(26))

try:
    # Sonsuz döngü
    while True:
        # PWM sinyalini okuyun ve değeri yazdırın
        adc_value = adc.read_u16()
        # ADC okuma değerini gerilime çevirin (0 ile 3.3V arasında)
        voltage = adc_value * 3.3 / 65535
        print("ADC Okuma Değeri:", adc_value)
        print("Gerilim:", voltage, "V")
        # Biraz bekle
        utime.sleep(0.5)

except KeyboardInterrupt:
    # Ctrl+C tuş kombinasyonu algılandığında programı sonlandır
    print("\nProgram sonlandırıldı.")

finally:
    # PWM sinyalini kapat
    pwm_sig.duty_u16(0)
    pwm_sig.deinit()