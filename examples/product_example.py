from pttavm import PTTClient
import os

def main():
    client = PTTClient(
        username=os.getenv("PTT_USERNAME"),
        password=os.getenv("PTT_PASSWORD")
    )
    
    # Barkod kontrolü
    barcode_info = client.check_barcode("example_barcode")
    print("Barkod Kontrolü:", barcode_info)
    
    # Ürün stok listesi
    stock_list = client.get_product_stock()
    print("\nÜrün Stok Listesi:", stock_list)
    
    # API versiyonu
    version = client.get_version()
    print("\nAPI Versiyonu:", version)

if __name__ == "__main__":
    main()
