# CSV dosyasına veri yazma fonksiyonu
def write_to_csv(filename, data):
    with open(filename, 'a') as file:
        # Veriyi uygun biçimde biçimlendirerek dosyaya yaz
        file.write(','.join(map(str, data)) + '\n')

# Örnek veri
veri = ['05/03/2024 - 12:43:12', 1000, 25]  # TarihSaat, Basınç, Sıcaklık

# CSV dosyasına veri yaz
write_to_csv('data.csv', veri)