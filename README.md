# UNOFFICIAL PTT AVM API İstemcisi

PTT AVM API entegrasyonu için Python istemci kütüphanesi. 

## Son Sürüm: v0.1.4

### Yeni Eklenenler
- ✨ Ürün güncelleme servisleri (V2)
  - Tekli ve toplu güncelleme
  - Varyant yönetimi
  - Parça ve resim yönetimi
- 🔒 Kapsamlı validasyon sistemi
  - KDV oranı kontrolü
  - Fiyat validasyonları
  - Stok limitleri
  - Varyant tutarlılığı
- 🧮 Otomatik hesaplamalar
  - KDV ve indirim
  - Desi hesaplama
- 📝 Gelişmiş hata yönetimi

### Değişenler
- 🏗️ Servis yapısı iyileştirildi
- 📊 Validasyon kuralları merkezi hale getirildi
- 🎯 Örnek kodlar geliştirildi
- 📚 Dokümantasyon güncellendi

[Devamı için tıklayın](#değişiklik-geçmişi)

## Motivasyon

Bu proje, PTT AVM SOAP API'nin site docs ile verilen ultra yetersiz dokümantasyonuna tepki olarak doğmuştur.

## Kurulum

### Gereksinimler

- Python 3.7 veya üstü
- pip (Python paket yöneticisi)

### Pip ile kurulum

```bash
pip install pttavm-python
```

### Geliştirici Kurulumu

1. **Repoyu Klonlayın:**

   ```bash
   git clone https://github.com/selimkosgen/pttavm_python.git
   cd pttavm
   ```

2. **Sanal Ortam Oluşturun ve Aktifleştirin:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # veya
   .\venv\Scripts\activate  # Windows
   ```

3. **Gereksinimleri Yükleyin:**

   ```bash
   pip install -e .
   ```

### Kullanım

1. **Çevre Değişkenlerini Ayarlayın:**

   `.env` dosyası oluşturun ve API kimlik bilgilerinizi ekleyin:

   ```bash
   cp .env.example .env
   ```

   `.env` dosyasını düzenleyerek API kimlik bilgilerinizi girin:

   ```
   PTT_USERNAME=your_username
   PTT_PASSWORD=your_password
   ```

2. **Örnek Kullanım:**

```python
from pttavm import PTTClient

# İstemciyi başlat
client = PTTClient(
    username="your_username",
    password="your_password"
)

# Stok işlemleri
total_stocks = client.get_stock_count()
print(f"Toplam stok: {total_stocks}")

# Tek ürün bilgisi
stock = client.get_stock("barcode123")
if stock:
    print(f"Ürün: {stock.product.product_name}")
    print(f"Stok: {stock.quantity}")

# Tüm stokları getir
def progress_callback(stocks, page, total):
    print(f"Sayfa {page} yüklendi (Toplam: {total} ürün)")

all_stocks = client.get_all_stocks(progress_callback=progress_callback)
```

Örnek kullanımlar için `examples/` klasörüne göz atabilirsiniz:

- `examples/version_example.py`: API versiyon bilgisi alma örneği
- `examples/category_example.py`: Kategori listesi alma örneği 
- `examples/product_example.py`: Ürün bilgisi sorgulama örneği
- `examples/stock_example.py`: Stok işlemleri örneği

## Özellikler

### Mevcut Özellikler

- ✅ Authentication (API Kimlik Doğrulama)
- ✅ GetVersion (API Versiyon Bilgisi)
- ✅ Kategori Servisleri
  - GetCategoryTree
  - 🟠 AltKategoriListesi (Deprecated)
- ✅ Stok Servisleri
  - StokKontrolListesi (Sayfalı listeleme)
  - Tek ürün stok kontrolü
  - Toplu stok listeleme
  - Toplam stok sayısı hesaplama
- ✅ Ürün Servisleri
  - ✅ StokGuncelleV2 (Yeni)
  - ✅ StokGuncelleV2Bulk (Yeni)
  - ✅ StokFiyatGuncelle3
  - ✅ BarkodKontrol
  - ✅ BarkodKontrolBulk
  - ✅ AktifYap
  - 🟠 StokFiyatGuncelle (Deprecated)
  - 🟠 StokFiyatGuncelle2 (Deprecated)
  - 🟠 UpdateProductVariant (Deprecated)
- 🔴 Sipariş Servisleri
  - SaveInvoince
  - SiparisKontrolListesiV2
- 🔴 Mağaza Servisleri
  - GetCargoProfiles
  - KullaniciTedarikciBilgisiGetir

### Hedeflenen Temel Özellikler

- ✅ Kapsamlı dokümantasyon ve örnekler
- ✅ Kolay kullanımlı Python arayüzü
- ✅ Hata yönetimi ve doğrulama
- ✅ Validasyon kuralları
- ✅ Otomatik hesaplamalar
- ✅ İlerleme takibi
- ✅ Sayfalı listeleme desteği

## Eklenmesi Planlanan Özellikler

Henüz eklenmemiş olan ve gelecekteki güncellemelerde yer alması planlanan özellikler şunlardır:

- **Sipariş Servisleri**
  - SiparisKontrolListesi, KargoBilgiListesi

- **Kargo ve Teslimat Servisleri**
  - /v1/barcode-status, /v1/create-barcode, /v1/get-warehouse vb.

## Değişiklik Geçmişi

### v0.1.4
- ✨ Ürün güncelleme servisleri (V2)
- 🔒 Kapsamlı validasyon sistemi
- 🧮 Otomatik hesaplamalar
- 📝 Gelişmiş hata yönetimi

### v0.1.3
- ✨ Stok servisleri eklendi
- 📊 İlerleme takibi için callback sistemi eklendi
- 🔄 Sayfalama desteği (1000 ürün/sayfa)
- 🔨 Import yapısı basitleştirildi
- 📝 API kullanımı sadeleştirildi
- ⚡️ Hata yönetimi geliştirildi

### v0.1.2
- PTTAVMClient ismi PTTClient olarak değiştirildi
- Stok servisleri eklendi ve geliştirildi
- İlerleme takibi için callback desteği eklendi
- Sayfalı listeleme desteği eklendi
- Hata yönetimi geliştirildi
