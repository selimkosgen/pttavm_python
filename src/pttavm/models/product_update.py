from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from .variant import Variant

@dataclass
class ProductImage:
    """Ürün resmi modeli"""
    url: str
    order: int  # Sira
    
    def __post_init__(self):
        if not self.url:
            raise ValueError("Image URL is required")
        if not isinstance(self.order, int) or self.order < 1:
            raise ValueError("Image order must be a positive integer")

@dataclass
class ProductPart:
    """Ürün parça modeli"""
    part_no: int
    desi: float
    comment: Optional[str] = None

    def __post_init__(self):
        if not isinstance(self.part_no, int) or self.part_no < 1:
            raise ValueError("Part number must be a positive integer")
        if self.desi < 0:
            raise ValueError("Desi cannot be negative")

@dataclass
class ProductUpdateV2:
    """Ürün güncelleme modeli (V2)"""
    # Required fields
    barcode: str  # Barkod
    product_name: str  # UrunAdi
    product_code: str  # UrunKodu
    category_id: int  # YeniKategoriId

    # Optional fields with defaults
    description: str = ""  # Aciklama
    admin_code: Optional[str] = None  # AdminCode
    weight: float = 0  # Agirlik
    is_active: bool = True  # Aktif
    subcategory_name: Optional[str] = None  # AltKategoriAdi
    subcategory_id: int = 0  # AltKategoriId
    main_category_id: int = 0  # AnaKategoriId
    dimensions: tuple = (0, 0, 0)  # BoyX, BoyY, BoyZ
    desi: float = 0  # Desi
    status: str = "Mevcut"  # Durum
    warranty_period: int = 0  # GarantiSuresi
    warranty_company: Optional[str] = None  # GarantiVerenFirma
    gtin: Optional[str] = None
    is_admin: bool = False  # IsAdmin
    discount: float = 0  # Iskonto
    vat_rate: float = 0  # KDVOran
    price_with_vat: float = 0  # KDVli
    price_without_vat: float = 0  # KDVsiz
    cargo_profile_id: int = 0  # KargoProfilId
    update_category_info: bool = False  # KategoriBilgisiGuncelle
    is_available: bool = True  # Mevcut
    quantity: int = 0  # Miktar
    parts: List[ProductPart] = None  # Parts
    sale_start_date: Optional[datetime] = None  # SatisBaslangicTarihi
    sale_end_date: Optional[datetime] = None  # SatisBitisTarihi
    shop_id: int = 0  # ShopId
    is_single_box: bool = True  # SingleBox
    tag: Optional[str] = None
    estimated_shipping_time: int = 0  # TahminiKargoSuresi
    supplier_subcategory_name: Optional[str] = None  # TedarikciAltKategoriAdi
    supplier_subcategory_id: int = 0  # TedarikciAltKategoriId
    supplier_virtual_category_id: int = 0  # TedarikciSanalKategoriId
    product_id: int = 0  # UrunId
    product_images: List[ProductImage] = None  # UrunResimleri
    product_url: Optional[str] = None  # UrunUrl
    long_description: Optional[str] = None  # UzunAciklama
    variants: List[Variant] = None  # VariantListesi

    def __post_init__(self):
        # Required field validations
        if not self.barcode:
            raise ValueError("Barcode is required")
        if not self.product_name:
            raise ValueError("Product name is required")
        if not self.product_code:
            raise ValueError("Product code is required")
        if self.category_id <= 0:
            raise ValueError("Valid category ID is required")

        # Optional field validations
        if self.weight < 0:
            raise ValueError("Weight cannot be negative")
        if self.desi < 0:
            raise ValueError("Desi cannot be negative")
        if self.warranty_period < 0:
            raise ValueError("Warranty period cannot be negative")
        if self.discount < 0:
            raise ValueError("Discount cannot be negative")
        if not 0 <= self.vat_rate <= 100:
            raise ValueError("VAT rate must be between 0 and 100")
        if self.price_without_vat < 0:
            raise ValueError("Price without VAT cannot be negative")
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")
        if self.estimated_shipping_time < 0:
            raise ValueError("Estimated shipping time cannot be negative")

        # Initialize empty lists
        if self.parts is None:
            self.parts = []
        if self.product_images is None:
            self.product_images = []
        if self.variants is None:
            self.variants = [] 