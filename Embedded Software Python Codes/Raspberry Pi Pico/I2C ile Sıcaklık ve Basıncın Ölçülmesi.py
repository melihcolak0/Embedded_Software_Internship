import machine
import utime

# I2C busunu başlat
i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))

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
    #t_data = (data[3]*65536) + (data[4]*256) + data[5]
    return p_data, t_data

# Basınç ve sıcaklık değerlerini hesapla
def calculate_pressure_temperature(p_data, t_data):
    
    pressure = (((p_data-838861)/6710886)*(80)) + 10
    
    #temperature = (t_data/65536) + 25
    #temperature = ((t_data >> 8) / 256.0) + 25
    
    pressure2 = (pressure * 2.4929) - 30.931 # Grafik denklemi uygulanmış son basınç değeri
        
    #if 0 <= t_data <= 2970000:
        #temperature = (t_data / 65536) + 25
    #elif 14467000 <= t_data <= 16766000:
        #temperature = ((t_data / 65536) + 25) - 256
    
   #--------------------------------------------------------------------------------     
    if 16766000 <= t_data <= 16777194 or 0 <= t_data <= 2800: # A ve B Sensörü
        temperature = 24.9526792 # A ve B Sensörü
    elif 2800 < t_data <= 2980000: # A ve B Sensörü
        temperature = (t_data / 65536) + 25 # A ve B Sensörü
    elif 14460000 <= t_data <= 16766000: # A ve B Sensörü 
        temperature = ((t_data / 65536) + 25) - 256 # A ve B Sensörü
    else:
        temperature = None  # Belirtilen aralıklar dışında ise None döndür
        
  #--------------------------------------------------------------------------------
    
    
    return t_data, temperature

# Ana döngü
while True:
    # Sensör verilerini oku
    data = read_sensor_data()
    
    # Verileri işle
    pressure_data, temperature_data = process_sensor_data(data)
    
    # Basınç ve sıcaklık değerlerini hesapla
    pressure, temperature = calculate_pressure_temperature(pressure_data, temperature_data)
    
    # Sonuçları yazdır
    print("Basınç: {} Pa, Sıcaklık: {} °C".format(pressure, temperature))
    
    # 2 saniye bekle
    utime.sleep(0.01)