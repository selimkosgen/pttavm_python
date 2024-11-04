# Changelog

Bu dosya PTT AVM API İstemcisi'nin tüm önemli değişikliklerini belgelemektedir.

Format [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) standardını takip etmektedir,
ve bu proje [Semantic Versioning](https://semver.org/spec/v2.0.0.html) kullanmaktadır.

## [0.1.4] - 2024-11-04

### Eklenenler
- ✨ Ürün güncelleme servisleri (V2) eklendi
  - Tekli ürün güncelleme (`update_product_v2`)
  - Toplu ürün güncelleme (`update_products_v2_bulk`)
  - Varyant desteği
  - Parça yönetimi
  - Resim yönetimi
- ✨ Stok fiyat güncelleme servisi eklendi
  - `StokFiyatGuncelle3` desteği
  - Varyant fiyat güncellemeleri
  - Toplu güncelleme desteği
- 🔒 Kapsamlı validasyon kuralları
  - KDV oranı kontrolü (0, 1, 10, 20)
  - Fiyat validasyonları
  - Stok limitleri (0-9999)
  - Karakter uzunluğu kontrolleri
  - Varyant tutarlılık kontrolleri
- 🧮 Otomatik hesaplamalar
  - KDV hesaplama
  - İndirim hesaplama
  - Desi hesaplama
- 📝 Detaylı hata mesajları
- 🔄 5 dakika güncelleme kuralı kontrolü

### Değişenler
- 🏗️ Servis yapısı iyileştirildi
- 📊 Validasyon kuralları merkezi hale getirildi
- 🎯 Örnek kodlar geliştirildi
- 📚 Dokümantasyon güncellendi

### Düzeltmeler
- 🐛 Varyant güncelleme hataları giderildi
- 🔧 XML oluşturma hataları düzeltildi
- ✅ Test kapsamı artırıldı

## [0.1.3] - 2024-11-04

### Eklenenler
- ✨ Stok servisleri eklendi
  - `get_stock()`: Tek ürün stok kontrolü
  - `get_stocks()`: Sayfalı stok listesi
  - `get_all_stocks()`: Tüm stokları getirme
  - `get_stock_count()`: Toplam stok sayısı
- 📊 İlerleme takibi için callback sistemi
  - Sayfa başına işlem durumu
  - Toplam işlem durumu
- 🔄 Sayfalama desteği
  - Sayfa başına 1000 ürün
  - Otomatik sayfalama

### Değişenler
- 🔨 Import yapısı basitleştirildi
  - `from pttavm import PTTClient` şeklinde direkt import
- 📝 API metodları yeniden adlandırıldı
  - Daha açıklayıcı metod isimleri
  - Türkçe karakter kullanımı kaldırıldı
- ⚡️ Hata yönetimi geliştirildi
  - Daha detaylı hata mesajları
  - Exception handling iyileştirmeleri

### Düzeltmeler
- 🐛 SOAP istek formatı düzeltildi
- 🔧 Veri dönüşüm hataları giderildi
- ✅ Test coverage artırıldı

## [0.1.2] - 2024-10-30

### Değişenler
- `PTTAVMClient` sınıfı `PTTClient` olarak yeniden adlandırıldı
- Stok servisleri eklendi
- İlerleme takibi için callback desteği eklendi
- Sayfalı listeleme desteği eklendi

### Düzeltmeler
- Hata yönetimi geliştirildi
- Dokümantasyon güncellendi

## [0.1.1] - 2024-10-29

### Eklenenler
- İlk sürüm
- Temel API işlevselliği
- Kategori servisleri
- Ürün servisleri
- Versiyon kontrolü

[0.1.4]: https://github.com/selimkosgen/pttavm_python/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/selimkosgen/pttavm_python/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/selimkosgen/pttavm_python/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/selimkosgen/pttavm_python/releases/tag/v0.1.1 