import machine
import utime
from machine import Pin
from gpio_lcd import GpioLcd


# I2C busunu başlat
i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))

# LCD'nin pin bağlantılarını tanımla
lcd = GpioLcd(rs_pin=Pin(16),
              enable_pin=Pin(17),
              d4_pin=Pin(18),
              d5_pin=Pin(19),
              d6_pin=Pin(20),
              d7_pin=Pin(21),
              num_lines=2, num_columns=16)

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
    
    pressure2 = (pressure * 2.4929) - 30.931
    
    if 16766000 <= t_data <= 16777194 or 0 <= t_data <= 2800:
        temperature = 24.9526792
    elif 2800 < t_data <= 2980000:
        temperature = (t_data / 65536) + 25
    elif 14460000 <= t_data <= 16766000:
        temperature = ((t_data / 65536) + 25) - 256
    else:
        temperature = None
        
    return pressure2, temperature

# Sıcaklık ve basıncı LCD'ye yazdır
def print_pressure_temperature_on_lcd(pressure, temperature, lcd):
    lcd.clear()  # LCD ekranını temizle
    lcd.move_to(0, 0)  # İmleci başlangıç konumuna taşı
    lcd.putstr("Basinc: {:.2f} Pa".format(pressure))  # Basıncı ekrana yazdır
    lcd.move_to(0, 1)  # İmleci alt satırın başlangıç konumuna taşı
    lcd.putstr("Sicaklik: {:.2f} C".format(temperature))  # Sıcaklığı ekrana yazdır
    

# Ana döngü
while True:
    # Sensör verilerini oku
    data = read_sensor_data()
    
    # Verileri işle
    pressure_data, temperature_data = process_sensor_data(data)
    
    # Basınç ve sıcaklık değerlerini hesapla
    pressure, temperature = calculate_pressure_temperature(pressure_data, temperature_data)
    
    # LCD'ye basınç ve sıcaklık değerlerini yazdır
    print_pressure_temperature_on_lcd(pressure, temperature, lcd)
    
    # 1 saniye bekle
    utime.sleep(1)

