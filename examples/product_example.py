import os
from pttavm.client import PTTAVMClient

def main():
    # Get credentials from environment variables
    username = os.getenv('PTT_USERNAME')
    password = os.getenv('PTT_PASSWORD')
    
    if not username or not password:
        print("Error: PTT_USERNAME and PTT_PASSWORD environment variables must be set")
        return
    
    # Initialize client
    client = PTTAVMClient(
        username=username,
        password=password
    )
    
    try:
        # Get product service
        product_service = client.get_product_service()
        
        # Check barcode (example barcode)
        barcode = os.getenv('PTT_TEST_BARCODE', 'DEFAULT_BARCODE')
        product = product_service.check_barcode(barcode)
        
        if product:
            print("\nProduct Information:")
            print(f"Product ID: {product.product_id}")
            print(f"Name: {product.name}")
            print(f"Description: {product.description}")
            print(f"Product Code: {product.product_code}")
            print(f"Barcode: {product.barcode}")
            print(f"Category ID: {product.category_id}")
            print("\nPricing:")
            print(f"Price (without VAT): {product.price_without_vat} TL")
            print(f"VAT Rate: {product.vat_rate}%")
            print(f"Price (with VAT): {product.price_with_vat} TL")
            print(f"Discount: {product.discount}%")
            print("\nStock Information:")
            print(f"Stock Quantity: {product.stock_quantity}")
            print(f"Status: {product.status}")
            print(f"Is Available: {product.is_available}")
            print(f"Is Active: {product.is_active}")
            print("\nShipping Information:")
            print(f"Weight: {product.weight} gr")
            print(f"Dimensions: {product.dimension_x}x{product.dimension_y}x{product.dimension_z} cm")
            print(f"Desi: {product.desi}")
            print(f"Shipping Period: {product.shipping_period} day(s)")
            print(f"Cargo Profile ID: {product.cargo_profile_id}")
            print("\nWarranty Information:")
            print(f"Warranty Period: {product.warranty_period} months")
            print(f"Warranty Company: {product.warranty_company}")
            print("\nOther Information:")
            print(f"Shop ID: {product.shop_id}")
            print(f"GTIN: {product.gtin}")
            print(f"Single Box: {product.single_box}")
            print(f"Tag: {product.tag}")
            print(f"Product URL: {product.product_url}")
        else:
            print(f"No product found with barcode: {barcode}")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()
