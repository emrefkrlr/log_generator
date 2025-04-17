# Web Server Log Generator

## Proje Amacı
Bu proje, Nginx web sunucusu için gerçekçi erişim (`access.log`) ve hata (`error.log`) logları üreten bir Python betiğidir. Üretilen loglar, test, analiz veya simülasyon amaçlı kullanılabilir. Proje, normal trafik ve belirli IP adreslerinden gelen anormal trafik desenlerini simüle eder ve log dosyalarını boyut sınırlarına uygun şekilde döndürerek (rotated logs) kaydeder.

## Özellikler
- **Erişim ve Hata Logları Üretimi:** Nginx formatında erişim ve hata logları oluşturur.
- **Anormal Trafik Simülasyonu:** Belirtilen IP adreslerinden yüksek hacimli trafik üretir.
- **Log Rotasyonu:** Log dosyaları, belirlenen boyut sınırını aştığında otomatik olarak bölünür.
- **Farklı Kullanıcı Temsilcileri (User Agents):** Web, mobil ve IoT cihazları için çeşitli kullanıcı temsilcileri içerir.
- **Zaman Damgası:** Belirtilen gün sayısı boyunca rastgele zaman damgaları ile log üretir.

## Bağımlılıklar
Proje, aşağıdaki Python kütüphanelerine ihtiyaç duyar:
- `faker`: Sahte IP adresleri ve diğer veriler için.
- `python` (3.x sürümü önerilir).

Bağımlılıkları yüklemek için:
```bash
pip install faker
```

## Kurulum
1. Bu repository'yi klonlayın:
   ```bash
   git clone git@github.com:emrefkrlr/webserver_log_generator.git
   cd webserver_log_generator
   ```
2. Gerekli bağımlılıkları yükleyin:
   ```bash
   pip install faker
   ```
3. Betiği çalıştırın:
   ```bash
   python generate_logs.py
   ```

## Kullanım
1. Betiği çalıştırdığınızda, `logs/` klasöründe aşağıdaki dosyalar oluşturulur:
   - `access.log` (ve gerekirse `access.log.1`, `access.log.2`, vb.)
   - `error.log` (ve gerekirse `error.log.1`, `error.log.2`, vb.)
2. Log dosyaları, Nginx formatına uygun şekilde üretilir ve her biri maksimum 200 KB boyutundadır.
3. Varsayılan yapılandırma:
   - Normal trafik: 2000 kayıt/gün
   - Anormal trafik: 1000 kayıt/gün (belirtilen IP'lerden)
   - Gün sayısı: 5
   - Anormal IP'ler: `192.168.100.100`, `10.0.0.99`

### Örnek Çıktı
**access.log:**
```
192.168.1.1 - - [17/Apr/2025:12:34:56 +0000] "GET /home HTTP/1.1" 200 1024 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
10.0.0.99 - - [17/Apr/2025:12:35:01 +0000] "POST /api/user/profile HTTP/1.1" 404 512 "-" "curl/7.68.0"
```

**error.log:**
```
[17/Apr/2025:12:35:01 +0000] [error] [client 10.0.0.99] File does not exist: /var/www/favicon.ico
```

## Yapılandırma
Betiğin yapılandırma parametreleri `generate_logs.py` dosyasındaki aşağıdaki değişkenlerle ayarlanabilir:
- `ANOMALY_IPS`: Anormal trafik üreten IP adresleri.
- `ANOMALY_TRAFFIC_COUNT`: Anormal trafik kayıt sayısı.
- `NORMAL_TRAFFIC_COUNT`: Normal trafik kayıt sayısı.
- `LOG_SIZE_LIMIT`: Log dosyalarının maksimum boyutu (bayt cinsinden).
- `DAYS`: Logların kapsadığı gün sayısı.

Örnek:
```python
ANOMALY_IPS = ["192.168.1.100", "10.0.0.50"]
ANOMALY_TRAFFIC_COUNT = 500
NORMAL_TRAFFIC_COUNT = 1000
LOG_SIZE_LIMIT = 100 * 1024  # 100 KB
DAYS = 3
```
