from pttavm import PTTClient
import os

def main():
    # İstemciyi başlat
    client = PTTClient(
        username="",
        password=""
    )
    
    # Toplam stok sayısını öğren
    total = client.get_stock_count()
    print(f"Toplam stok sayısı: {total}")
    
    # Tek bir ürün bilgisi al
    stock = client.get_stock("example_barcode")
    if stock:
        print(f"\nÜrün: {stock.product.product_name}")
        print(f"Stok: {stock.quantity}")
    
    # İlerleme takibi ile tüm stokları getir
    def show_progress(stocks, page, total):
        print(f"Sayfa {page} yüklendi. (Toplam: {total} ürün)")
    
    all_stocks = client.get_all_stocks(progress_callback=show_progress)
    print(all_stocks)
    print(f"\nToplam {len(all_stocks)} ürün yüklendi.")
    
if __name__ == "__main__":
    main() 