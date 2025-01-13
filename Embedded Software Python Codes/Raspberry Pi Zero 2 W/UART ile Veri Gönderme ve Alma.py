import serial
import RPi.GPIO as GPIO
import time

# RS485 DE/RE pinlerini tanımla
DE_RE_PIN = 2

# GPIO pinlerini BCM modunda ayarla
GPIO.setmode(GPIO.BCM)
GPIO.setup(DE_RE_PIN, GPIO.OUT)

# UART tanımla
uart = serial.Serial(port='/dev/ttyAMA0', baudrate=9600, timeout=0.1)

def enable_transmit():
    GPIO.output(DE_RE_PIN, GPIO.HIGH)

def enable_receive():
    GPIO.output(DE_RE_PIN, GPIO.LOW)

def send_data(data):
    enable_transmit()
    uart.write(data.encode())
    time.sleep(0.05)  # Bekleme süresi, gereksinime göre ayarlayabilirsiniz.
    enable_receive()

def receive_data():
    enable_receive()
    data = uart.readline()
    return data.decode().strip() if data else None

# Ana döngü
while True:
    # Sürekli olarak "Merhaba" yaz
    enable_transmit()
    data_to_send = "Hello, World!\n"  # Gönderilecek veri
    uart.write(data_to_send.encode())  # Veriyi UART üzerinden gönder
    print("Sent:", data_to_send.strip())  # Gönderilen veriyi ekrana yazdır
    time.sleep(0.1)  # Bir saniye bekleme ekleyelim, sürekli gönderim olmaması için
    
    received_data = receive_data()  # Gelen veriyi al
    if received_data is not None:
        print("Received data:", received_data)  # Gelen veriyi ekrana yazdır
    time.sleep(0.1)  # Biraz bekleme ekleyelim, işlemciyi yormamak için
