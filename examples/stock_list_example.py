from pttavm import PTTClient
import os

def main():
    # Load environment variables
    
    client = PTTClient(
        username="username",
        password="password"
    )
    
    # Get total stock count
    total = client.get_stock_count()
    print(f"Total stock count: {total}")
    
    # Get stocks with pagination
    page = 0
    stocks = client.get_stocks(page)
    print(f"\nStocks on page {page}:")
    for stock in stocks[:5]:  # Show first 5 items
        print(f"Product: {stock.product.product_name}")
        print(f"Barcode: {stock.barcode}")
        print(f"Quantity: {stock.quantity}")
        print("---")

if __name__ == "__main__":
    main() 