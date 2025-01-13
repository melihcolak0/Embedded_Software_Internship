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

# CSV dosyasına veri yazma fonksiyonu
def write_to_csv(filename, data):
    with open(filename, 'a') as file:
        file.write(';'.join(map(str, data)) + '\n')

# Ana döngü
while True:
    # Sensör verilerini oku
    data = read_sensor_data()
    
    # Verileri işle
    pressure_data, temperature_data = process_sensor_data(data)
    
    # Basınç ve sıcaklık değerlerini hesapla
    pressure, temperature = calculate_pressure_temperature(pressure_data, temperature_data)
    
    # Tarih ve saati al
    tarih_saat = utime.localtime()

    # Sonuçları yazdır
    print("Basınç: {} Pa, Sıcaklık: {} °C".format(pressure, temperature))
    print("{:02d}/{:02d}/{:04d} - {:02d}:{:02d}:{:02d}".format(
        tarih_saat[2], tarih_saat[1], tarih_saat[0],  # Tarih bilgisi (gün, ay, yıl)
        tarih_saat[3], tarih_saat[4], tarih_saat[5]  # Saat bilgisi (saat, dakika, saniye)
    ))

    # Verileri CSV dosyasına yaz
    write_to_csv('data.csv', [f"{tarih_saat[2]}/{tarih_saat[1]}/{tarih_saat[0]} - {tarih_saat[3]}:{tarih_saat[4]}:{tarih_saat[5]}", pressure, temperature])
    
    # 2 saniye bekle
    utime.sleep(1)