from pttavm import PTTClient
from pttavm.models.variant import StockPriceUpdate, Variant, VariantAttribute

def update_stock_example():
    client = PTTClient(
        username="your_username",
        password="your_password"
    )
    
    # Varyantlı ürün güncelleme
    variant_attrs = [
        VariantAttribute(
            name="Renk",
            value="Kırmızı",
            price=30,
            is_price_difference=True
        ),
        VariantAttribute(
            name="Beden",
            value="XL",
            price=0,
            is_price_difference=False
        )
    ]
    
    variant = Variant(
        main_barcode="barcode-test-123",
        variant_barcode="barcode-test-123-1071",
        quantity=10,
        attributes=variant_attrs
    )
    
    update_data = StockPriceUpdate(
        barcode="barcode-test-123",
        is_active=False,
        discount=0,
        vat_rate=10,
        price_with_vat=0,
        price_without_vat=1000,
        quantity=5,
        category_id=101,
        variants=[variant]
    )
    
    result = client.update_stock_price(update_data)
    print(f"Güncelleme {'başarılı' if result else 'başarısız'}")

if __name__ == "__main__":
    update_stock_example() 