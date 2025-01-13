import network
import socket
from machine import Pin, I2C
import utime

# I2C busunu başlat
i2c = I2C(0, scl=Pin(1), sda=Pin(0))

# Sensörün I2C adresi
SENSOR_ADDR = 0x6D

# Basınç ve sıcaklık verilerini oku
def read_sensor_data():
    data = bytearray(6)
    i2c.readfrom_mem_into(SENSOR_ADDR, 0x06, data)
    return data

# Basınç ve sıcaklık verilerini işle
def process_sensor_data(data):
    p_data = (data[0] << 16) | (data[1] << 8) | data[2]
    t_data = (data[3] << 16) | (data[4] << 8) | data[5]
    return p_data, t_data

# Basınç ve sıcaklık değerlerini hesapla
def calculate_pressure_temperature(p_data, t_data):
    pressure = (((p_data-838861)/6710886)*(80)) + 10
    
    if 16766000 <= t_data <= 16777194 or 0 <= t_data <= 2800: # A ve B Sensörü
        temperature = 24.9526792 # A ve B Sensörü
    elif 2800 < t_data <= 2980000: # A ve B Sensörü
        temperature = (t_data / 65536) + 25 # A ve B Sensörü
    elif 14460000 <= t_data <= 16766000: # A ve B Sensörü 
        temperature = ((t_data / 65536) + 25) - 256 # A ve B Sensörü
    else:
        temperature = None  # Belirtilen aralıklar dışında ise None döndür
        
    return pressure, temperature

# HTML şablonu
html = """<!DOCTYPE html><html>
<head><meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="1"> <!-- Sayfanın 1 saniyede bir yenilenmesi -->
<link rel="icon" href="data:,">
<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}
.text { text-decoration: none; font-size: 30px; margin: 2px;}
</style></head>
<body><center><h1>Pressure and Temperature Measurement</h1></center><br><br>
<p class="text">%s</p>
<p class="text">%s</p>
</body></html>
"""

# Wi-Fi bilgileri
wifi_ssid = 'your_ssid'
wifi_password = 'your_password'

# Sunucu bilgileri
server_ip = 'your_server_ip'
server_port = your_port

# Wi-Fi bağlantısını başlat
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(wifi_ssid, wifi_password)

while not wifi.isconnected():
    pass

print("Connected to WiFi")
print("IP Address:", wifi.ifconfig()[0])

# Sunucuyu başlat
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('Listening on', addr)

# Ana döngü
while True:
    try:       
        cl, addr = s.accept()
        print('Client connected from', addr)
        
        # Sensör verilerini oku
        data = read_sensor_data()
        
        # Verileri işle
        pressure_data, temperature_data = process_sensor_data(data)
        
        # Basınç ve sıcaklık değerlerini hesapla
        pressure, temperature = calculate_pressure_temperature(pressure_data, temperature_data)
        
        # Veriyi birleştir
        data_to_send = "Pressure: {} Pa, Temperature: {} °C".format(pressure, temperature)
        data_to_send = data_to_send.encode()  # Gönderilecek veriyi byte'a çevir
        
        # Veriyi sunucuya gönder
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(html % ("Pressure: {} Pa".format(pressure), "Temperature: {} °C".format(temperature)))
        cl.close()
        
        # Veriyi belirli bir IP adresi ve porta gönder
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_ip, server_port))
        sock.send(data_to_send)
        sock.close()
        
    except OSError as e:
        cl.close()
        print('Connection closed')