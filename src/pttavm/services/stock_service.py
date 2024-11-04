from typing import List, Tuple, Optional
import math
from ..models.stock import (
    Stock, StockWarranty, StockDimensions, 
    StockPrice, StockProduct
)
from .base_service import BaseService

class StockService(BaseService):
    ITEMS_PER_PAGE = 1000  # PTT AVM API'nin sayfa başına döndüğü maksimum ürün sayısı
    
    def __init__(self, username: str, password: str):
        super().__init__(username=username, password=password)

    def get_single_stock(self, barcode: str) -> Optional[Stock]:
        """
        Tek bir ürünün stok bilgisini getirir.
        
        Args:
            barcode (str): Ürün barkodu
            
        Returns:
            Optional[Stock]: Stok bilgisi, ürün bulunamazsa None
        """
        try:
            response = self.call_service(
                operation="StokKontrolListesi",
                params={"Barkod": barcode}
            )
            
            if not response or 'a:StokKontrolDetay' not in response:
                return None

            stock_data = response['a:StokKontrolDetay']
            return self._parse_stock_data(stock_data)
            
        except Exception as e:
            raise Exception(f"Failed to get stock info: {str(e)}")

    def get_total_stock_count(self) -> int:
        """
        Toplam stok sayısını hesaplar.
        Sayfa sayfa kontrol ederek boş sayfa gelene kadar devam eder.
        
        Returns:
            int: Toplam stok sayısı
        """
        try:
            total_count = 0
            page = 0
            
            while True:
                stocks = self.get_stock_list(page)
                
                if not stocks:  # Eğer boş liste gelirse son sayfaya ulaşmışız demektir
                    break
                    
                total_count += len(stocks)
                
                # Eğer gelen ürün sayısı sayfa başına maksimum ürün sayısından azsa
                # son sayfaya ulaşmışız demektir
                if len(stocks) < self.ITEMS_PER_PAGE:
                    break
                    
                page += 1
                
            return total_count
            
        except Exception as e:
            raise Exception(f"Failed to get total stock count: {str(e)}")

    def get_all_stocks(self, batch_callback=None) -> List[Stock]:
        """
        Tüm stok listesini pagination ile getirir.
        
        Args:
            batch_callback: Her sayfa çekildiğinde çağrılacak callback fonksiyonu
                          Örnek: lambda stocks, page, total_items: print(f"Sayfa {page} - Toplam {total_items} ürün")
        
        Returns:
            List[Stock]: Tüm stokların listesi
        """
        try:
            all_stocks = []
            page = 0
            
            while True:
                stocks = self.get_stock_list(page)
                
                if not stocks:  # Boş liste gelirse bitir
                    break
                    
                all_stocks.extend(stocks)
                
                if batch_callback:
                    batch_callback(stocks, page + 1, len(all_stocks))
                    
                # Son sayfaya ulaştıysak bitir
                if len(stocks) < self.ITEMS_PER_PAGE:
                    break
                    
                page += 1
                    
            return all_stocks
            
        except Exception as e:
            raise Exception(f"Failed to get all stocks: {str(e)}")

    def get_stock_list(self, page: int = 0) -> List[Stock]:
        """
        Belirtilen sayfa için stok kontrol listesini getirir.
        
        Args:
            page (int): Sayfa numarası (varsayılan: 0)
            
        Returns:
            List[Stock]: Stok listesi
        """
        try:
            response = self.call_service(
                operation="StokKontrolListesi",
                params={"SearchPage": page}
            )
            
            if not response:
                return []

            stock_data_list = response.get('a:StokKontrolDetay', [])
            
            # Tek bir sonuç varsa liste haline getir
            if isinstance(stock_data_list, dict):
                stock_data_list = [stock_data_list]
                
            stocks = []
            for data in stock_data_list:
                try:
                    stock = self._parse_stock_data(data)
                    if stock:
                        stocks.append(stock)
                except (ValueError, TypeError) as e:
                    print(f"Error parsing stock data: {e}")
                    continue
                    
            return stocks
            
        except Exception as e:
            raise Exception(f"Failed to get stock list: {str(e)}")

    def _parse_stock_data(self, data: dict) -> Optional[Stock]:
        """
        API'den gelen stok verisini Stock nesnesine dönüştürür.
        
        Args:
            data (dict): API'den gelen ham veri
            
        Returns:
            Optional[Stock]: Dönüştürülmüş Stock nesnesi
        """
        try:
            return Stock(
                description=data.get('a:Aciklama'),
                weight=float(data.get('a:Agirlik', 0)),
                is_active=data.get('a:Aktif') == 'true',
                barcode=data.get('a:Barkod'),
                dimensions=StockDimensions(
                    x=float(data.get('a:BoyX', 0)),
                    y=float(data.get('a:BoyY', 0)),
                    z=float(data.get('a:BoyZ', 0))
                ),
                desi=float(data.get('a:Desi', 0)),
                status=data.get('a:Durum'),
                warranty=StockWarranty(
                    warranty_period=int(data.get('a:GarantiSuresi', 0)),
                    warranty_company=data.get('a:GarantiVerenFirma')
                ),
                gtin=data.get('a:Gtin'),
                price=StockPrice(
                    price_discount=float(data.get('a:Iskonto', 0)),
                    price_vat_rate=float(data.get('a:KDVOran', 0)),
                    price_with_vat=float(data.get('a:KDVli', 0)),
                    price_without_vat=float(data.get('a:KDVsiz', 0))
                ),
                cargo_profile_id=int(data.get('a:KargoProfilId', 0)),
                is_available=data.get('a:Mevcut') == 'true',
                quantity=int(data.get('a:Miktar', 0)),
                shop_id=int(data.get('a:ShopId', 0)),
                is_single_box=data.get('a:SingleBox') == 'true',
                product=StockProduct(
                    product_name=data.get('a:UrunAdi'),
                    product_id=int(data.get('a:UrunId', 0)),
                    product_code=data.get('a:UrunKodu'),
                    product_url=data.get('a:UrunUrl'),
                    product_long_description=data.get('a:UzunAciklama')
                ),
                category_id=int(data.get('a:YeniKategoriId', 0))
            )
        except (ValueError, TypeError) as e:
            print(f"Error parsing stock data: {e}")
            return None