# UNOFFICIAL PTT AVM API İstemcisi

PTT AVM API entegrasyonu için Python istemci kütüphanesi. 

## Son Sürüm: v0.1.3

### Yeni Eklenenler
- ✨ Stok servisleri eklendi
  - Toplu stok listeleme
  - Tek ürün stok kontrolü
  - Sayfalı listeleme desteği
  - Toplam stok sayısı hesaplama
- 📊 İlerleme takibi için callback sistemi
- 🔄 Sayfalama desteği (1000 ürün/sayfa)

### Değişenler
- 🔨 Import yapısı basitleştirildi
  - Eski: `from pttavm.client import PTTAVMClient`
  - Yeni: `from pttavm import PTTClient`
- 📝 Daha temiz ve anlaşılır API
- ⚡️ Daha verimli hata yönetimi
- 🎯 Son kullanıcı odaklı geliştirmeler

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
  - 🟠 AltKategoriListesi (Deprecated)
  - GetCategoryTree
- ✅ Stok Servisleri
  - StokKontrolListesi (Sayfalı listeleme)
  - Tek ürün stok kontrolü
  - Toplu stok listeleme
  - Toplam stok sayısı hesaplama
- ✅ Barkod Kontrol (Ürün Servisleri)
- 🔴 Ürün Servisleri
  - AktifYap
  - BarkodKontrolBulk
  - GetProductsWithVariants
  - 🟠 StokFiyatGuncelle (Deprecated)
  - 🟠 StokFiyatGuncelle2 (Deprecated)
  - StokFiyatGuncelle3
  - 🟠 StokFiyatGuncelleBulk (Deprecated)
  - 🟠 StokGuncelle (Deprecated)
  - 🟠 StokGuncelleBulk (Deprecated)
  - StokGuncelleV2
  - StokGuncelleV2Bulk
  - 🟠 UpdateProductVariant (Deprecated)
- 🔴 Kategori Servisleri
  - GetCategory
  - GetMainCategories 
  - 🟠 TedarikciAltKategoriListesi (Deprecated)
- 🔴 Sipariş Servisleri
  - SaveInvoince
  - SiparisKontrolListesiV2
- 🔴 Mağaza Servisleri
  - GetCargoProfiles
  - KullaniciTedarikciBilgisiGetir
- 🔴 Kargo ve Teslimat Servisleri
  - /v1/get-barcode-tag

### Hedeflenen Temel Özellikler

- ✅ Kapsamlı dokümantasyon ve örnekler
- ✅ Kolay kullanımlı Python arayüzü
- ✅ Hata yönetimi ve doğrulama
- ✅ Tip güvenliği
- ✅ Otomatik test desteği
- ✅ İlerleme takibi (Progress callback)
- ✅ Sayfalı listeleme desteği

## Eklenmesi Planlanan Özellikler

Henüz eklenmemiş olan ve gelecekteki güncellemelerde yer alması planlanan özellikler şunlardır:

- **Stok ve Fiyat Güncelleme Servisleri**
  - StokFiyatGuncelle, StokFiyatGuncelleBulk, StokGuncelleV2 vb.

- **Sipariş Servisleri**
  - SiparisKontrolListesi, KargoBilgiListesi

- **Kargo ve Teslimat Servisleri**
  - /v1/barcode-status, /v1/create-barcode, /v1/get-warehouse vb.

## Değişiklik Geçmişi

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
