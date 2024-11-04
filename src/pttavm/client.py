from typing import List, Optional, Dict
from .services.category_service import CategoryService
from .services.stock_service import StockService
from .services.product_service import ProductService
from .services.version_service import VersionService
from .models.category import Category
from .models.stock import Stock
from .models.product import Product
from .models.variant import StockPriceUpdate
from .models.product import ProductActivation, ProductUpdateError
from .models.barcode import BarcodeCheckResult, BulkBarcodeCheck, BarcodeError
from .models.product_update import ProductUpdateV2

class PTTClient:
    """
    PTT AVM API'si için ana istemci sınıfı.
    Tüm servisleri tek bir noktadan yönetir.
    """
    
    def __init__(self, username: str, password: str):
        """
        Args:
            username: PTT AVM kullanıcı adı
            password: PTT AVM şifresi
        """
        self.username = username
        self.password = password
        
        # Initialize services
        self._category_service = CategoryService(username, password)
        self._stock_service = StockService(username, password)
        self._product_service = ProductService(username, password)
        self._version_service = VersionService(username, password)

    # Category Operations
    def get_category(self, category_id: int) -> Optional[Category]:
        """Kategori bilgilerini getirir."""
        return self._category_service.get_categories(category_id)

    # Stock Operations
    def get_stock(self, barcode: str) -> Optional[Stock]:
        """Tek bir ürünün stok bilgisini getirir."""
        return self._stock_service.get_single_stock(barcode)
    
    def get_stocks(self, page: int = 0) -> List[Stock]:
        """Stok listesini sayfa sayfa getirir."""
        return self._stock_service.get_stock_list(page)
    
    def get_all_stocks(self, progress_callback=None) -> List[Stock]:
        """Tüm stok listesini getirir."""
        return self._stock_service.get_all_stocks(batch_callback=progress_callback)
    
    def get_stock_count(self) -> int:
        """Toplam stok sayısını getirir."""
        return self._stock_service.get_total_stock_count()

    # Product Operations
    def check_barcode(self, barcode: str) -> BarcodeCheckResult:
        """Tekil barkod kontrolü yapar."""
        return self._product_service.check_barcode(barcode)

    def check_barcodes_bulk(self, barcodes: List[str]) -> List[BarcodeCheckResult]:
        """Toplu barkod kontrolü yapar."""
        return self._product_service.check_barcodes_bulk(barcodes)

    def activate_product(self, product_id: int, is_active: bool = True) -> bool:
        """Ürünü aktif/pasif yapar."""
        activation = ProductActivation(
            product_id=product_id,
            is_active=is_active
        )
        return self._product_service.activate_product(activation)

    def update_product_v2(self, product: ProductUpdateV2) -> bool:
        """Ürün bilgilerini günceller (V2)."""
        return self._product_service.update_product_v2(product)

    def update_products_v2_bulk(self, products: List[ProductUpdateV2]) -> bool:
        """Birden fazla ürünü toplu olarak günceller (V2)."""
        return self._product_service.update_products_v2_bulk(products)

    def update_stock_price(self, update_data: StockPriceUpdate) -> bool:
        """Stok ve fiyat bilgilerini günceller."""
        return self._stock_service.update_stock_price(update_data)

    def update_stock_price_bulk(self, update_data_list: List[StockPriceUpdate]) -> bool:
        """Stok ve fiyat bilgilerini toplu olarak günceller."""
        return self._stock_service.update_stock_price_bulk(update_data_list)

    # Version Operations
    def get_version(self) -> Dict[str, str]:
        """API versiyonunu getirir."""
        return self._version_service.get_version()

    # Utility Methods
    def get_service(self, service_type: str):
        """İstenilen servisi döndürür."""
        services = {
            'category': self._category_service,
            'stock': self._stock_service,
            'product': self._product_service,
            'version': self._version_service
        }
        return services.get(service_type.lower())
