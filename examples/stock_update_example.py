from pttavm import PTTClient
from pttavm.models.variant import (
    StockPriceUpdate, Variant, VariantAttribute,
    StockUpdateError, RequiredFieldError, ValidationError
)
import os

def update_simple_product():
    """Example for updating a simple product without variants"""
    client = PTTClient(
        username="username",
        password="password"
    )
    
    try:
        # Simple product update
        update_data = StockPriceUpdate(
            barcode="simple-product-123",
            price_without_vat=100.0,
            vat_rate=18,
            category_id=101,
            quantity=50
        )
        
        result = client.update_stock_price(update_data)
        print(f"Simple product update: {'Success' if result else 'Failed'}")
        
    except RequiredFieldError as e:
        print(f"Missing required field: {e}")
    except ValidationError as e:
        print(f"Validation error: {e}")
    except StockUpdateError as e:
        print(f"Stock update error: {e}")

def update_product_with_variants():
    """Example for updating a product with variants"""
    client = PTTClient(
        username="username",
        password="password"
    )
    
    try:
        # Create variant attributes
        color_attr = VariantAttribute(
            name="Color",
            value="Red",
            price=30,
            is_price_difference=True
        )
        
        size_attr = VariantAttribute(
            name="Size",
            value="XL"
        )
        
        # Create variant
        variant = Variant(
            main_barcode="variant-product-123",
            variant_barcode="variant-product-123-red-xl",
            quantity=10,
            attributes=[color_attr, size_attr]
        )
        
        # Create update data
        update_data = StockPriceUpdate(
            barcode="variant-product-123",
            price_without_vat=200.0,
            vat_rate=18,
            category_id=101,
            quantity=10,
            variants=[variant]
        )
        
        result = client.update_stock_price(update_data)
        print(f"Variant product update: {'Success' if result else 'Failed'}")
        
    except RequiredFieldError as e:
        print(f"Missing required field: {e}")
    except ValidationError as e:
        print(f"Validation error: {e}")
    except StockUpdateError as e:
        print(f"Stock update error: {e}")

def main():
    update_simple_product()
    print("\n---\n")
    update_product_with_variants()

if __name__ == "__main__":
    main() 