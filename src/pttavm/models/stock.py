from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class StockWarranty:
    warranty_period: int
    warranty_company: Optional[str]

@dataclass
class StockDimensions:
    x: float
    y: float
    z: float

@dataclass
class StockPrice:
    price_discount: float
    price_vat_rate: float
    price_with_vat: float
    price_without_vat: float

@dataclass
class StockProduct:
    product_name: str
    product_id: int
    product_code: Optional[str]
    product_url: Optional[str]
    product_long_description: Optional[str]

@dataclass
class Stock:
    description: Optional[str]
    weight: float
    is_active: bool
    barcode: Optional[str]
    dimensions: StockDimensions
    desi: float
    status: Optional[str]
    warranty: StockWarranty
    gtin: Optional[str]
    price: StockPrice
    cargo_profile_id: int
    is_available: bool
    quantity: int
    shop_id: int
    is_single_box: bool
    product: StockProduct
    category_id: int 