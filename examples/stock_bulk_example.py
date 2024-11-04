from pttavm import PTTClient
import os

def main():
    
    client = PTTClient(
        username="username",
        password="password"
    )
    
    # Progress tracking callback
    def show_progress(stocks, page, total):
        print(f"Loaded page {page} (Total items: {total})")
    
    # Get all stocks with progress tracking
    all_stocks = client.get_all_stocks(progress_callback=show_progress)
    print(f"\nTotal loaded items: {len(all_stocks)}")
    
    # Show some statistics
    active_stocks = sum(1 for stock in all_stocks if stock.is_active)
    print(f"Active products: {active_stocks}")
    print(f"Total quantity: {sum(stock.quantity for stock in all_stocks)}")

if __name__ == "__main__":
    main() 