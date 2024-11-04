from pttavm import PTTClient
from pttavm.models.product_update import ProductUpdateV2, ProductImage, ProductPart
from pttavm.models.variant import Variant, VariantAttribute
import os
from datetime import datetime

def update_single_product():
    """Tekli ürün güncelleme örneği"""
    client = PTTClient(
        username=os.getenv("PTT_USERNAME"),
        password=os.getenv("PTT_PASSWORD")
    )
    
    # Ürün parçaları
    parts = [
        ProductPart(
            part_no=1,
            desi=5,
            comment="Part1 Test"
        ),
        ProductPart(
            part_no=2,
            desi=6,
            comment="Part2 Test"
        )
    ]
    
    # Ürün resimleri
    images = [
        ProductImage(
            url="https://example.com/image1.jpg",
            order=1
        ),
        ProductImage(
            url="https://example.com/image2.jpg",
            order=2
        )
    ]
    
    # Varyantlar
    variant_attrs = [
        VariantAttribute(name="Renk", value="Kırmızı", price=30, is_price_difference=True),
        VariantAttribute(name="Beden", value="XL")
    ]
    
    variants = [
        Variant(
            main_barcode="test-123",
            variant_barcode="test-123-red-xl",
            quantity=10,
            attributes=variant_attrs
        )
    ]
    
    # Ürün güncelleme verisi
    product = ProductUpdateV2(
        barcode="test-123",
        product_name="Test Ürün",
        product_code="test-123",
        category_id=1192,
        description="Test açıklama",
        weight=1.5,
        dimensions=(10, 20, 30),
        desi=5,
        warranty_period=24,
        warranty_company="Test Garanti",
        price_without_vat=1000,
        vat_rate=18,
        cargo_profile_id=1,
        estimated_shipping_time=3,
        parts=parts,
        product_images=images,
        variants=variants,
        long_description="<p>Detaylı açıklama</p>"
    )
    
    try:
        result = client.update_product_v2(product)
        print(f"Ürün güncelleme: {'Başarılı' if result else 'Başarısız'}")
    except Exception as e:
        print(f"Hata: {e}")

def update_bulk_products():
    """Toplu ürün güncelleme örneği"""
    client = PTTClient(
        username=os.getenv("PTT_USERNAME"),
        password=os.getenv("PTT_PASSWORD")
    )
    
    # Birden fazla ürün için güncelleme verisi
    products = [
        ProductUpdateV2(
            barcode="test-123",
            product_name="Test Ürün 1",
            product_code="test-123",
            category_id=1192,
            price_without_vat=1000,
            vat_rate=18
        ),
        ProductUpdateV2(
            barcode="test-124",
            product_name="Test Ürün 2",
            product_code="test-124",
            category_id=1192,
            price_without_vat=2000,
            vat_rate=18
        )
    ]
    
    try:
        result = client.update_products_v2_bulk(products)
        print(f"Toplu güncelleme: {'Başarılı' if result else 'Başarısız'}")
    except Exception as e:
        print(f"Hata: {e}")

def main():
    print("Tekli Ürün Güncelleme:")
    update_single_product()
    
    print("\nToplu Ürün Güncelleme:")
    update_bulk_products()

if __name__ == "__main__":
    main() 