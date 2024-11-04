from typing import Optional, Dict, List
from .base_service import BaseService
from ..models.product import Product, ProductActivation, ProductUpdateError
from ..models.barcode import BarcodeCheckResult, BulkBarcodeCheck, BarcodeError
from ..models.product_update import ProductUpdateV2
from ..models.variant import ValidationError
import xmltodict

class ProductService(BaseService):
    """Service for product related operations"""
    
    def check_barcode(self, barcode: str) -> BarcodeCheckResult:
        """
        Tekil barkod kontrolü yapar.
        
        Args:
            barcode (str): Kontrol edilecek barkod
            
        Returns:
            BarcodeCheckResult: Barkod kontrol sonucu
            
        Raises:
            ValidationError: Barkod geçersiz ise
            BarcodeError: Barkod kontrolü sırasında hata oluşursa
        """
        try:
            # Barkod validasyonu
            if not barcode:
                raise ValidationError("Barcode cannot be empty")
            if not isinstance(barcode, str):
                raise ValidationError("Barcode must be a string")
            if len(barcode.strip()) == 0:
                raise ValidationError("Barcode cannot be whitespace")

            response = self.call_service(
                operation="BarkodKontrol",
                params={"Barkod": barcode.strip()}
            )
            
            # API yanıtını işle
            exists = bool(response.get("Success", False))
            message = response.get("Message")
            
            return BarcodeCheckResult(
                barcode=barcode,
                exists=exists,
                message=message
            )
            
        except ValidationError as e:
            raise ValidationError(f"Invalid barcode: {str(e)}")
        except Exception as e:
            raise BarcodeError(f"Barcode check failed: {str(e)}")

    def check_barcodes_bulk(self, barcodes: List[str]) -> List[BarcodeCheckResult]:
        """
        Toplu barkod kontrolü yapar.
        
        Args:
            barcodes (List[str]): Kontrol edilecek barkod listesi
            
        Returns:
            List[BarcodeCheckResult]: Barkod kontrol sonuçları
            
        Raises:
            ValidationError: Barkod listesi geçersiz ise
            BarcodeError: Barkod kontrolü sırasında hata oluşursa
        """
        try:
            # Liste validasyonu
            if not isinstance(barcodes, list):
                raise ValidationError("Barcodes must be a list")
            if not barcodes:
                raise ValidationError("Barcodes list cannot be empty")
            if not all(isinstance(b, str) for b in barcodes):
                raise ValidationError("All barcodes must be strings")
            if not all(b.strip() for b in barcodes):
                raise ValidationError("Empty or whitespace-only barcodes are not allowed")
            
            # Giriş verilerini doğrula
            bulk_check = BulkBarcodeCheck(barcodes=barcodes)
            
            response = self.call_service(
                operation="BarkodKontrolBulk",
                params={
                    "Barkod": {
                        "arr:string": bulk_check.barcodes
                    }
                }
            )
            
            # API yanıtını işle
            results = []
            bulk_results = response.get("BarkodKontrolBulkResult", {})
            
            for barcode in bulk_check.barcodes:
                result = bulk_results.get(barcode, {})
                results.append(
                    BarcodeCheckResult(
                        barcode=barcode,
                        exists=bool(result.get("Success", False)),
                        message=result.get("Message")
                    )
                )
            
            return results
            
        except ValidationError as e:
            raise ValidationError(f"Invalid barcodes: {str(e)}")
        except Exception as e:
            raise BarcodeError(f"Bulk barcode check failed: {str(e)}")

    def get_stock_list(self) -> dict:
        """
        Get stock list from PTT AVM system.
        
        Returns:
            dict: Response from PTT AVM API containing stock list
        """
        soap_action = "http://tempuri.org/IService/StokKontrolListesi"
        
        soap_envelope = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
            <soapenv:Header>
                {self._get_security_header()}
            </soapenv:Header>
            <soapenv:Body>
                <tem:StokKontrolListesi/>
            </soapenv:Body>
        </soapenv:Envelope>
        """

        response = self._make_request(
            soap_action=soap_action,
            soap_envelope=soap_envelope
        )
        
        return xmltodict.parse(response.text)

    def activate_product(self, activation: ProductActivation) -> bool:
        """
        Ürünü aktif/pasif yapar.
        
        Args:
            activation: Ürün aktivasyon bilgileri
            
        Returns:
            bool: İşlem başarılı ise True
            
        Raises:
            ProductUpdateError: Aktivasyon işlemi başarısız olursa
        """
        try:
            response = self.call_service(
                operation="AktifYap",
                params={
                    "req": {
                        "Aktif": "1" if activation.is_active else "0",
                        "UrunId": activation.product_id
                    }
                }
            )
            
            return True if response else False
            
        except Exception as e:
            raise ProductUpdateError(f"Failed to activate product: {str(e)}")

    def update_product_v2(self, product: ProductUpdateV2) -> bool:
        """
        Ürün bilgilerini günceller (V2).
        
        Args:
            product: Güncellenecek ürün bilgileri
            
        Returns:
            bool: İşlem başarılı ise True
            
        Raises:
            ProductUpdateError: Güncelleme işlemi başarısız olursa
        """
        try:
            # Parça listesini hazırla
            parts_xml = ""
            if product.parts:
                for part in product.parts:
                    parts_xml += f"""
                    <ept:PartRequest>
                        <ept:Desi>{part.desi}</ept:Desi>
                        <ept:PartComment>{part.comment or ''}</ept:PartComment>
                        <ept:PartNo>{part.part_no}</ept:PartNo>
                    </ept:PartRequest>"""

            # Resim listesini hazırla
            images_xml = ""
            if product.product_images:
                for image in product.product_images:
                    images_xml += f"""
                    <ept:UrunResim>
                        <ept:Sira>{image.order}</ept:Sira>
                        <ept:Url>{image.url}</ept:Url>
                    </ept:UrunResim>"""

            # Varyant listesini hazırla
            variants_xml = ""
            if product.variants:
                for variant in product.variants:
                    attrs_xml = ""
                    for attr in variant.attributes:
                        attrs_xml += f"""
                        <ept:VariantAttr>
                            <ept:Deger>{attr.value}</ept:Deger>
                            <ept:Fiyat>{attr.price}</ept:Fiyat>
                            <ept:FiyatFarkiMi>{str(attr.is_price_difference).lower()}</ept:FiyatFarkiMi>
                            <ept:Tanim>{attr.name}</ept:Tanim>
                        </ept:VariantAttr>"""

                    variants_xml += f"""
                    <ept:Variant>
                        <ept:AnaUrunKodu>{variant.main_barcode}</ept:AnaUrunKodu>
                        <ept:Attributes>{attrs_xml}</ept:Attributes>
                        <ept:Miktar>{variant.quantity}</ept:Miktar>
                        <ept:VariantBarkod>{variant.variant_barcode}</ept:VariantBarkod>
                    </ept:Variant>"""

            response = self.call_service(
                operation="StokGuncelleV2",
                params={
                    "item": {
                        "Aciklama": product.description,
                        "AdminCode": product.admin_code,
                        "Agirlik": product.weight,
                        "Aktif": str(product.is_active).lower(),
                        "AltKategoriAdi": product.subcategory_name,
                        "AltKategoriId": product.subcategory_id,
                        "AnaKategoriId": product.main_category_id,
                        "Barkod": product.barcode,
                        "BoyX": product.dimensions[0],
                        "BoyY": product.dimensions[1],
                        "BoyZ": product.dimensions[2],
                        "Desi": product.desi,
                        "Durum": product.status,
                        "GarantiSuresi": product.warranty_period,
                        "GarantiVerenFirma": product.warranty_company,
                        "Gtin": product.gtin,
                        "IsAdmin": str(product.is_admin).lower(),
                        "Iskonto": product.discount,
                        "KDVOran": product.vat_rate,
                        "KDVli": product.price_with_vat,
                        "KDVsiz": product.price_without_vat,
                        "KargoProfilId": product.cargo_profile_id,
                        "KategoriBilgisiGuncelle": str(product.update_category_info).lower(),
                        "Mevcut": str(product.is_available).lower(),
                        "Miktar": product.quantity,
                        "Parts": parts_xml if parts_xml else None,
                        "SatisBaslangicTarihi": product.sale_start_date.isoformat() if product.sale_start_date else None,
                        "SatisBitisTarihi": product.sale_end_date.isoformat() if product.sale_end_date else None,
                        "ShopId": product.shop_id,
                        "SingleBox": str(product.is_single_box).lower(),
                        "Tag": product.tag,
                        "TahminiKargoSuresi": product.estimated_shipping_time,
                        "TedarikciAltKategoriAdi": product.supplier_subcategory_name,
                        "TedarikciAltKategoriId": product.supplier_subcategory_id,
                        "TedarikciSanalKategoriId": product.supplier_virtual_category_id,
                        "UrunAdi": product.product_name,
                        "UrunId": product.product_id,
                        "UrunKodu": product.product_code,
                        "UrunResimleri": images_xml if images_xml else None,
                        "UrunUrl": product.product_url,
                        "UzunAciklama": product.long_description,
                        "VariantListesi": variants_xml if variants_xml else None,
                        "YeniKategoriId": product.category_id
                    }
                }
            )
            
            return True if response else False
            
        except Exception as e:
            raise ProductUpdateError(f"Failed to update product: {str(e)}")

    def update_products_v2_bulk(self, products: List[ProductUpdateV2]) -> bool:
        """
        Birden fazla ürünü toplu olarak günceller (V2).
        
        Args:
            products: Güncellenecek ürün listesi
            
        Returns:
            bool: İşlem başarılı ise True
            
        Raises:
            ValidationError: Ürün listesi geçersiz ise
            ProductUpdateError: Güncelleme işlemi başarısız olursa
        """
        try:
            # Liste validasyonu
            if not isinstance(products, list):
                raise ValidationError("Products must be a list")
            if not products:
                raise ValidationError("Products list cannot be empty")
            if len(products) > 100:  # API limiti
                raise ValidationError("Maximum 100 products allowed per request")

            # Tüm ürünler için XML oluştur
            products_xml = ""
            for product in products:
                # Parça listesini hazırla
                parts_xml = ""
                if product.parts:
                    for part in product.parts:
                        parts_xml += f"""
                        <ept:PartRequest>
                            <ept:Desi>{part.desi}</ept:Desi>
                            <ept:PartComment>{part.comment or ''}</ept:PartComment>
                            <ept:PartNo>{part.part_no}</ept:PartNo>
                        </ept:PartRequest>"""

                # Resim listesini hazırla
                images_xml = ""
                if product.product_images:
                    for image in product.product_images:
                        images_xml += f"""
                        <ept:UrunResim>
                            <ept:Sira>{image.order}</ept:Sira>
                            <ept:Url>{image.url}</ept:Url>
                        </ept:UrunResim>"""

                # Varyant listesini hazırla
                variants_xml = ""
                if product.variants:
                    for variant in product.variants:
                        attrs_xml = ""
                        for attr in variant.attributes:
                            attrs_xml += f"""
                            <ept:VariantAttr>
                                <ept:Deger>{attr.value}</ept:Deger>
                                <ept:Fiyat>{attr.price}</ept:Fiyat>
                                <ept:FiyatFarkiMi>{str(attr.is_price_difference).lower()}</ept:FiyatFarkiMi>
                                <ept:Tanim>{attr.name}</ept:Tanim>
                            </ept:VariantAttr>"""

                        variants_xml += f"""
                        <ept:Variant>
                            <ept:AnaUrunKodu>{variant.main_barcode}</ept:AnaUrunKodu>
                            <ept:Attributes>{attrs_xml}</ept:Attributes>
                            <ept:Miktar>{variant.quantity}</ept:Miktar>
                            <ept:VariantBarkod>{variant.variant_barcode}</ept:VariantBarkod>
                        </ept:Variant>"""

                # Her ürün için XML oluştur
                products_xml += f"""
                <ept:StokUrun>
                    <ept:Aciklama>{product.description}</ept:Aciklama>
                    <ept:AdminCode>{product.admin_code}</ept:AdminCode>
                    <ept:Agirlik>{product.weight}</ept:Agirlik>
                    <ept:Aktif>{str(product.is_active).lower()}</ept:Aktif>
                    <ept:AltKategoriAdi>{product.subcategory_name}</ept:AltKategoriAdi>
                    <ept:AltKategoriId>{product.subcategory_id}</ept:AltKategoriId>
                    <ept:AnaKategoriId>{product.main_category_id}</ept:AnaKategoriId>
                    <ept:Barkod>{product.barcode}</ept:Barkod>
                    <ept:BoyX>{product.dimensions[0]}</ept:BoyX>
                    <ept:BoyY>{product.dimensions[1]}</ept:BoyY>
                    <ept:BoyZ>{product.dimensions[2]}</ept:BoyZ>
                    <ept:Desi>{product.desi}</ept:Desi>
                    <ept:Durum>{product.status}</ept:Durum>
                    <ept:GarantiSuresi>{product.warranty_period}</ept:GarantiSuresi>
                    <ept:GarantiVerenFirma>{product.warranty_company}</ept:GarantiVerenFirma>
                    <ept:Gtin>{product.gtin}</ept:Gtin>
                    <ept:IsAdmin>{str(product.is_admin).lower()}</ept:IsAdmin>
                    <ept:Iskonto>{product.discount}</ept:Iskonto>
                    <ept:KDVOran>{product.vat_rate}</ept:KDVOran>
                    <ept:KDVli>{product.price_with_vat}</ept:KDVli>
                    <ept:KDVsiz>{product.price_without_vat}</ept:KDVsiz>
                    <ept:KargoProfilId>{product.cargo_profile_id}</ept:KargoProfilId>
                    <ept:KategoriBilgisiGuncelle>{str(product.update_category_info).lower()}</ept:KategoriBilgisiGuncelle>
                    <ept:Mevcut>{str(product.is_available).lower()}</ept:Mevcut>
                    <ept:Miktar>{product.quantity}</ept:Miktar>
                    <ept:Parts>{parts_xml if parts_xml else None}</ept:Parts>
                    <ept:SatisBaslangicTarihi>{product.sale_start_date.isoformat() if product.sale_start_date else None}</ept:SatisBaslangicTarihi>
                    <ept:SatisBitisTarihi>{product.sale_end_date.isoformat() if product.sale_end_date else None}</ept:SatisBitisTarihi>
                    <ept:ShopId>{product.shop_id}</ept:ShopId>
                    <ept:SingleBox>{str(product.is_single_box).lower()}</ept:SingleBox>
                    <ept:Tag>{product.tag}</ept:Tag>
                    <ept:TahminiKargoSuresi>{product.estimated_shipping_time}</ept:TahminiKargoSuresi>
                    <ept:TedarikciAltKategoriAdi>{product.supplier_subcategory_name}</ept:TedarikciAltKategoriAdi>
                    <ept:TedarikciAltKategoriId>{product.supplier_subcategory_id}</ept:TedarikciAltKategoriId>
                    <ept:TedarikciSanalKategoriId>{product.supplier_virtual_category_id}</ept:TedarikciSanalKategoriId>
                    <ept:UrunAdi>{product.product_name}</ept:UrunAdi>
                    <ept:UrunId>{product.product_id}</ept:UrunId>
                    <ept:UrunKodu>{product.product_code}</ept:UrunKodu>
                    <ept:UrunResimleri>{images_xml if images_xml else None}</ept:UrunResimleri>
                    <ept:UrunUrl>{product.product_url}</ept:UrunUrl>
                    <ept:UzunAciklama>{product.long_description}</ept:UzunAciklama>
                    <ept:VariantListesi>{variants_xml if variants_xml else None}</ept:VariantListesi>
                    <ept:YeniKategoriId>{product.category_id}</ept:YeniKategoriId>
                </ept:StokUrun>"""

            response = self.call_service(
                operation="StokGuncelleV2Bulk",
                params={
                    "items": products_xml
                }
            )
            
            return True if response else False
            
        except ValidationError as e:
            raise ValidationError(f"Invalid products data: {str(e)}")
        except Exception as e:
            raise ProductUpdateError(f"Failed to update products in bulk: {str(e)}")
