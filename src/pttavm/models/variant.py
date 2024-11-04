from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from .validation_rules import ValidationRules
from datetime import datetime

class StockUpdateError(Exception):
    """Stok güncelleme hatası"""
    pass

class RequiredFieldError(StockUpdateError):
    """Zorunlu alan eksik hatası"""
    pass

class ValidationError(StockUpdateError):
    """Veri doğrulama hatası"""
    pass

@dataclass
class VariantAttribute:
    """Varyant özellik modeli"""
    name: str  # Tanim (Required)
    value: str  # Deger (Required)
    price: float = 0.0  # Fiyat (Optional)
    is_price_difference: bool = False  # FiyatFarkiMi (Optional)

    def __post_init__(self):
        if not self.name:
            raise RequiredFieldError("Variant attribute name (Tanim) is required")
        if not self.value:
            raise RequiredFieldError("Variant attribute value (Deger) is required")

@dataclass
class Variant:
    """Ürün varyant modeli"""
    main_barcode: str  # AnaUrunKodu (Required)
    variant_barcode: str  # VariantBarkod (Required)
    quantity: int  # Miktar (Required)
    attributes: List[VariantAttribute]  # Attributes (Required)

    def __post_init__(self):
        if not self.main_barcode:
            raise RequiredFieldError("Main barcode (AnaUrunKodu) is required")
        if not self.variant_barcode:
            raise RequiredFieldError("Variant barcode (VariantBarkod) is required")
        if not isinstance(self.quantity, int):
            raise ValidationError("Quantity (Miktar) must be an integer")
        if self.quantity < 0:
            raise ValidationError("Quantity (Miktar) cannot be negative")
        if not self.attributes:
            raise RequiredFieldError("At least one variant attribute is required")

@dataclass
class StockPriceUpdate:
    """Stok ve fiyat güncelleme modeli"""
    # Required fields
    barcode: str  # Barkod (Required)
    price_without_vat: float  # KDVsiz (Required)
    vat_rate: float  # KDVOran (Required)

    # Optional fields with defaults
    is_active: bool = True  # Aktif (Optional)
    discount: float = 0.0  # Iskonto (Optional)
    price_with_vat: float = 0.0  # KDVli (Optional, calculated if not provided)
    quantity: int = 0  # Miktar (Optional)
    category_id: int = 0  # YeniKategoriId (Optional)
    variants: Optional[List[Variant]] = None  # VariantListesi (Optional)

    def __post_init__(self):
        # Required field validations
        if not self.barcode:
            raise RequiredFieldError("Barcode (Barkod) is required")
        if not ValidationRules.validate_field_length('barcode', self.barcode):
            raise ValidationError(f"Barkod maksimum {ValidationRules.MAX_CHARS['barcode']} karakter olabilir")

        # Price validations
        if self.price_without_vat <= 0 and self.price_with_vat <= 0:
            raise ValidationError("KDV'li veya KDV'siz fiyat 0'dan büyük olmalı")
        if self.vat_rate not in ValidationRules.VALID_VAT_RATES:
            raise ValidationError(f"KDV oranı geçersiz. Geçerli değerler: {ValidationRules.VALID_VAT_RATES}")

        # Discount calculations
        if self.discount > 0:
            self.price_without_vat = ValidationRules.calculate_discounted_price(
                self.price_without_vat, 
                self.discount
            )

        # Stock validations
        self.quantity = ValidationRules.validate_stock_quantity(self.quantity)

        # Variant validations
        if self.variants:
            if len(self.variants) > ValidationRules.MAX_VARIANTS:
                raise ValidationError(f"Maksimum {ValidationRules.MAX_VARIANTS} varyant eklenebilir")
            if not ValidationRules.validate_variants_total_stock(self.variants):
                raise ValidationError(f"Toplam varyant stok miktarı {ValidationRules.MAX_STOCK}'u geçemez")

        # Category ID validations
        if self.category_id < 0:
            raise ValidationError("Category ID (YeniKategoriId) cannot be negative")

    def calculate_price_with_vat(self) -> float:
        """KDV'li fiyatı hesapla"""
        return self.price_without_vat * (1 + self.vat_rate / 100)

    def validate_variants(self) -> bool:
        """Varyant bilgilerini doğrula"""
        if not self.variants:
            return True
        return all(
            variant.main_barcode == self.barcode
            for variant in self.variants
        )