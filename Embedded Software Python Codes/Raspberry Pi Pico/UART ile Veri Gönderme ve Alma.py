import machine
import time

# RS485 DE/RE pinlerini tanımla
de_re_pin = machine.Pin(2, machine.Pin.OUT)

# UART tanımla
uart = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1))

def enable_transmit():
    de_re_pin.value(1)

def enable_receive():
    de_re_pin.value(0)

def send_data(data):
    enable_transmit()
    uart.write(data)
    time.sleep_us(50)  # Bekleme süresi, gereksinime göre ayarlayabilirsiniz.
    enable_receive()

def receive_data():
    enable_receive()
    if uart.any():
        return uart.read()
    else:
        return None

# Ana döngü
while True:
    # Sürekli olarak "Merhaba" yaz
    enable_transmit()
    data_to_send = "Hello, World!\n"  # Gönderilecek veri
    uart.write(data_to_send)  # Veriyi UART üzerinden gönder
    print("Sent:", data_to_send.strip())  # Gönderilen veriyi ekrana yazdır
    time.sleep(0.1)  # Bir saniye bekleme ekleyelim, sürekli gönderim olmaması için
    enable_receive()
    if uart.any():  # UART üzerinde veri var mı kontrol et
        #enable_receive()
        received_data = receive_data()
        print("Received data:", received_data.decode().strip())  # Gelen veriyi ekrana yazdır
    time.sleep(0.1)  # Biraz bekleme ekleyelim, işlemciyi yormamak için