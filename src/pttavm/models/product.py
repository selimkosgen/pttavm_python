from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    """Product model representing PTT AVM product data"""
    barcode: str
    product_id: int
    name: str
    description: Optional[str] = None
    long_description: Optional[str] = None
    product_code: Optional[str] = None
    product_url: Optional[str] = None
    weight: float = 0.0
    is_active: bool = False
    dimension_x: int = 0
    dimension_y: int = 0
    dimension_z: int = 0
    desi: float = 0.0
    status: str = ""
    warranty_period: int = 0
    warranty_company: str = ""
    gtin: str = ""
    discount: float = 0.0
    vat_rate: float = 0.0
    price_with_vat: float = 0.0
    price_without_vat: float = 0.0
    cargo_profile_id: int = 0
    is_available: bool = False
    stock_quantity: int = 0
    shop_id: int = 0
    single_box: int = 0
    tag: str = ""
    shipping_period: int = 0
    category_id: str = "0"

    @classmethod
    def from_dict(cls, data: dict) -> 'Product':
        """Create Product instance from dictionary data"""
        try:
            # Convert string values to appropriate types with error handling
            def safe_int(value, default=0):
                try:
                    if isinstance(value, dict):
                        return default
                    return int(value) if value is not None else default
                except (ValueError, TypeError):
                    return default

            def safe_float(value, default=0.0):
                try:
                    if isinstance(value, dict):
                        return default
                    return float(value) if value is not None else default
                except (ValueError, TypeError):
                    return default

            def safe_bool(value, default=False):
                if isinstance(value, str):
                    return value.lower() == 'true'
                return bool(value) if value is not None else default

            return cls(
                barcode=str(data.get('a:Barkod', '')),
                product_id=safe_int(data.get('a:UrunId')),
                name=str(data.get('a:UrunAdi', '')),
                description=str(data.get('a:Aciklama', '')),
                long_description=str(data.get('a:UzunAciklama', '')),
                product_code=str(data.get('a:UrunKodu', '')),
                product_url=str(data.get('a:UrunUrl', '')),
                weight=safe_float(data.get('a:Agirlik')),
                is_active=safe_bool(data.get('a:Aktif')),
                dimension_x=safe_int(data.get('a:BoyX')),
                dimension_y=safe_int(data.get('a:BoyY')),
                dimension_z=safe_int(data.get('a:BoyZ')),
                desi=safe_float(data.get('a:Desi')),
                status=str(data.get('a:Durum', '')),
                warranty_period=safe_int(data.get('a:GarantiSuresi')),
                warranty_company=str(data.get('a:GarantiVerenFirma', '')),
                gtin=str(data.get('a:Gtin', '')),
                discount=safe_float(data.get('a:Iskonto')),
                vat_rate=safe_float(data.get('a:KDVOran')),
                price_with_vat=safe_float(data.get('a:KDVli')),
                price_without_vat=safe_float(data.get('a:KDVsiz')),
                cargo_profile_id=safe_int(data.get('a:KargoProfilId')),
                is_available=safe_bool(data.get('a:Mevcut')),
                stock_quantity=safe_int(data.get('a:Miktar')),
                shop_id=safe_int(data.get('a:ShopId')),
                single_box=safe_int(data.get('a:SingleBox')),
                tag=str(data.get('a:Tag', '')),
                shipping_period=safe_int(data.get('a:TahminiKargoSuresi')),
                category_id=str(data.get('a:YeniKategoriId', '0'))
            )
        except Exception as e:
            raise Exception(f"Error parsing product data: {str(e)}")

class ProductUpdateError(Exception):
    """Ürün güncelleme hatası"""
    pass

class RequiredFieldError(ProductUpdateError):
    """Zorunlu alan eksik hatası"""
    pass

class ValidationError(ProductUpdateError):
    """Veri doğrulama hatası"""
    pass

@dataclass
class ProductActivation:
    """Ürün aktivasyon modeli"""
    product_id: int  # UrunId (Required)
    is_active: bool = True  # Aktif (Optional, default: True)

    def __post_init__(self):
        if not isinstance(self.product_id, int):
            raise ValidationError("Product ID must be an integer")
        if self.product_id <= 0:
            raise RequiredFieldError("Valid product ID is required")
