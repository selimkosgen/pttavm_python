from datetime import datetime, timedelta
from typing import List, Dict, Optional

class ValidationRules:
    """Stok güncelleme validasyon kuralları"""
    
    # Sabit değerler
    MAX_VARIANTS = 100
    MAX_STOCK = 9999
    MIN_STOCK = 0
    MAX_DESI = 300
    MAX_WARRANTY_PERIOD = 240
    MAX_SHIPPING_DAYS = 30
    MAX_IMAGES = 12
    VALID_VAT_RATES = [0, 1, 10, 20]
    
    # Karakter limitleri
    MAX_CHARS = {
        'warranty_company': 250,
        'product_code': 250,
        'barcode': 250,
        'product_name': 120,
        'short_description': 2500,
        'long_description': 102400,
        'part_no': 255,
        'part_comment': 255
    }
    
    @staticmethod
    def calculate_desi(dimensions: Optional[tuple] = None, weight: Optional[float] = None) -> float:
        """
        Desi hesaplama
        
        Args:
            dimensions: (en, boy, yükseklik) boyutları
            weight: Ağırlık (gram)
            
        Returns:
            float: Hesaplanan desi değeri
        """
        desi_from_volume = 0
        desi_from_weight = 0
        
        if dimensions:
            x, y, z = dimensions
            desi_from_volume = (x * y * z) / 3000.0
            
        if weight:
            desi_from_weight = weight / 1000.0
            
        return max(desi_from_volume, desi_from_weight)

    @staticmethod
    def can_update_barcode(last_update: datetime) -> bool:
        """
        Barkod güncelleme kontrolü (5 dakika kuralı)
        """
        return datetime.now() - last_update > timedelta(minutes=5)

    @staticmethod
    def calculate_discounted_price(price: float, discount: float) -> float:
        """
        İndirimli fiyat hesaplama
        
        Formula: KDVsiz = KDVsiz * (1 - (İndirim / 100))
        """
        return price * (1 - (discount / 100))

    @staticmethod
    def validate_stock_quantity(quantity: int, is_variant: bool = False) -> int:
        """
        Stok miktarı validasyonu ve düzeltme
        """
        if quantity < ValidationRules.MIN_STOCK:
            return ValidationRules.MIN_STOCK
        if quantity > ValidationRules.MAX_STOCK:
            return ValidationRules.MAX_STOCK
        return quantity

    @staticmethod
    def validate_variants_total_stock(variants: List[Dict]) -> bool:
        """
        Varyant toplam stok kontrolü
        """
        total_stock = sum(v.get('quantity', 0) for v in variants)
        return total_stock <= ValidationRules.MAX_STOCK

    @staticmethod
    def validate_images(images: List[Dict]) -> List[Dict]:
        """
        Ürün resimlerini validate et ve limitle
        """
        if not images:
            raise ValueError("En az 1 ürün resmi gerekli")
        return images[:ValidationRules.MAX_IMAGES]

    @staticmethod
    def validate_field_length(field_name: str, value: str) -> bool:
        """
        Alan uzunluğu kontrolü
        """
        max_length = ValidationRules.MAX_CHARS.get(field_name)
        if max_length and len(value) > max_length:
            return False
        return True 