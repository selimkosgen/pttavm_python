# UNOFFICIAL PTT AVM API İstemcisi

PTT AVM API entegrasyonu için Python istemci kütüphanesi. 

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

### PyPI üzerinden kurulum

```bash
pip install pttavm
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

Örnek kullanımlar için `examples/` klasörüne göz atabilirsiniz:

- `examples/version_example.py`: API versiyon bilgisi alma örneği
- `examples/category_example.py`: Kategori listesi alma örneği 
- `examples/product_example.py`: Ürün bilgisi sorgulama örneği


## Özellikler

### Mevcut Özellikler

- ✅ Authentication (API Kimlik Doğrulama)
- ✅ GetVersion (API Versiyon Bilgisi)
- ✅ Kategori Servisleri
  - AltKategoriListesi
  - KategoriListesi 
  - GetCategoryTree
- ✅ Barkod Kontrol (Ürün Servisleri)
- 🔴 Ürün Servisleri
  - AktifYap
  - BarkodKontrolBulk
  - GetProductsWithVariants
  - StokFiyatGuncelle
  - StokFiyatGuncelle2 
  - StokFiyatGuncelle3
  - StokFiyatGuncelleBulk
  - StokGuncelle
  - StokGuncelleBulk
  - StokGuncelleV2
  - StokGuncelleV2Bulk
  - StokKontrolListesi
  - UpdateProductVariant
- 🔴 Kategori Servisleri
  - GetCategory
  - GetMainCategories
  - TedarikciAltKategoriListesi
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

## Eklenmesi Planlanan Özellikler

Henüz eklenmemiş olan ve gelecekteki güncellemelerde yer alması planlanan özellikler şunlardır:

- **Stok ve Fiyat Güncelleme Servisleri**
  - StokFiyatGuncelle, StokFiyatGuncelleBulk, StokGuncelleV2 vb.

- **Sipariş Servisleri**
  - SiparisKontrolListesi, KargoBilgiListesi

- **Kargo ve Teslimat Servisleri**
  - /v1/barcode-status, /v1/create-barcode, /v1/get-warehouse vb.
