from machine import Pin
from time import sleep_ms

led = Pin(15, Pin.OUT)
button = Pin(16, Pin.IN, Pin.PULL_UP)

while True:
    if button.value() == 0:
        delay = 100
    else:
        delay = 1000
        
    led.toggle()
    sleep_ms(delay)