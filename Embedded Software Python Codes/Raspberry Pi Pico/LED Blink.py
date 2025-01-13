import machine
import utime

led_onboard = machine.Pin("LED", machine.Pin.OUT)

while True:
    led_onboard.value(1)
    print('on')
    utime.sleep_ms(1000)
    
    led_onboard.value(0)
    print('off')
    utime.sleep_ms(1000)
