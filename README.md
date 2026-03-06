# nehir-debi-rapor
DSI 11. Bolge Mudurlugu - Gunluk Nehir Debi Takip Sistemi

## 💧 Proje Hakkında

Bu proje, DSİ 11. Bölge Müdürlüğü'nün [Edirne Nehir Debi Takip Sistemi](https://edirnenehir.dsi.gov.tr/) üzerinden günlük nehir debi verilerini otomatik olarak çekerek:

- 📊 **Görsel grafik** oluşturur
- 📄 **HTML raporu** hazırlar
- 📧 **E-posta ile gönderir**
- 🌐 **GitHub Pages'te yayınlar**

GitHub Actions ile her gün saat **08:00**'da otomatik olarak çalışır.

## 🚀 Özellikler

- ✅ Otomatik veri çekme (Web Scraping)
- ✅ Matplotlib ile görsel grafik oluşturma
- ✅ Responsive HTML rapor
- ✅ Gmail SMTP ile otomatik e-posta gönderimi
- ✅ GitHub Pages üzerinde canlı yayın
- ✅ GitHub Actions ile zamanlanmış otomasyonu

## 📚 Dosya Yapısı

```
nehir-debi-rapor/
├── .github/
│   └── workflows/
│       └── rapor.yml          # GitHub Actions workflow
├── scraper.py              # Ana Python scripti
├── requirements.txt        # Python bağımlılıkları
├── output/
│   ├── index.html          # Oluşturulan HTML rapor
│   └── debi_grafik.png     # Debi grafiği
└── README.md
```

## ⚙️ Kurulum

### 1. Repository'yi Fork/Clone Edin

```bash
git clone https://github.com/KULLANICI_ADINIZ/nehir-debi-rapor.git
cd nehir-debi-rapor
```

### 2. GitHub Secrets Ayarlayın

Repository ayarlarından (`Settings > Secrets and variables > Actions > New repository secret`) aşağıdaki secret'ları ekleyin:

| Secret Adı | Açıklama |
|------------|----------|
| `GMAIL_USER` | Gmail adresiniz (örn: example@gmail.com) |
| `GMAIL_PASS` | Gmail uygulama şifresi ([Nasıl alınır?](https://support.google.com/accounts/answer/185833)) |
| `GITHUB_TOKEN` | Otomatik oluşturulur (`${{ secrets.GITHUB_TOKEN }}`) |

⚠️ **Önemli:** Gmail için normal şifrenizi DEĞİL, "Uygulama Şifresi" oluşturmanız gerekir:
1. Google Hesabı > Güvenlik > 2 Adımlı Doğrulama'yı etkinleştirin
2. Uygulama Şifresi oluşturun
3. Bu şifreyi `GMAIL_PASS` olarak ekleyin

### 3. GitHub Pages'i Etkinleştirin

1. Repository ayarlarına gidin (`Settings > Pages`)
2. **Source**: `GitHub Actions` seçin
3. Kaydedin

### 4. İlk Çalıştırmayı Başlatın
```bash
git add .
git commit -m "Initial commit: DSI nehir debi otomasyonu"
git push origin main
```

Ya da `Actions` sekmesinden manuel olarak çalıştırın.

## 💻 Yerel Kullanım

```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# Scripti çalıştır
python scraper.py
```

## 📅 Zamanlanmış Çalışma

GitHub Actions workflow'u her gün saat **08:00 UTC+3**'te otomatik olarak çalışır:

```yaml
schedule:
  - cron: '0 5 * * *'  # Her gün 08:00 (UTC+3)
```

Manuel olarak da çalıştırabilirsiniz: `Actions > Raporu oluştur > Run workflow`

## 🌐 Canlı Rapor

Oluşturulan rapor şu adreste canlı olarak yayınlanır:

🔗 **https://KULLANICI_ADINIZ.github.io/nehir-debi-rapor/**

## 📧 E-posta Bildirimi

Her gün saat 08:00'da rapor otomatik olarak `serdarerman@gmail.com` adresine gönderilir.

E-posta adresini değiştirmek için `scraper.py` dosyasındaki 201. satırı düzenleyin:

```python
msg['To'] = 'YENI_EMAIL@gmail.com'
```

## 🛠️ Teknolojiler

- **Python 3.11**
- **BeautifulSoup4** - Web scraping
- **Matplotlib** - Grafik oluşturma
- **Requests** - HTTP istekleri
- **GitHub Actions** - CI/CD otomasyonu
- **GitHub Pages** - Statik site barındırma

## 👤 Yazar

Bu proje, DSİ nehir debi verilerinin düzgün takibi için oluşturulmuştur.

## 📜 Lisans

MIT License - Detaylar için LICENSE dosyasına bakınız.
