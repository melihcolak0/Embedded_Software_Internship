import network
import socket

#wifi_ssid = "your_ssid"
#wifi_password = "yourpassword"

# Parametreleri dosyadan al
with open("param.txt", "r") as f:
    exec(f.read())

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(wifi_ssid, wifi_password)

while not wifi.isconnected():
    pass

print("Connected to WiFi")
print("IP Address:", wifi.ifconfig()[0])


#server_ip = "your_server_ip"
#server_port = your_port

data_to_send = b"deneme"  # Gönderilecek veri

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server_ip, server_port))
sock.send(data_to_send)
sock.close()