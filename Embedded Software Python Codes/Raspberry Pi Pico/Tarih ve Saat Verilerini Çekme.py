import utime

# Tarih ve saati al
tarih_saat = utime.localtime()

# Alınan tarih ve saati istenen formatta yazdır
print("{:02d}/{:02d}/{:04d} - {:02d}:{:02d}:{:02d}".format(
    tarih_saat[2], tarih_saat[1], tarih_saat[0],  # Tarih bilgisi (gün, ay, yıl)
    tarih_saat[3], tarih_saat[4], tarih_saat[5]  # Saat bilgisi (saat, dakika, saniye)
))