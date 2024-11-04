import pytest
from pttavm.services.stock_service import StockService

def test_get_stock_list():
    service = StockService(
        username="test_username",
        password="test_password"
    )
    
    try:
        stocks = service.get_stock_list(0)
        assert isinstance(stocks, list)
        
        if stocks:
            stock = stocks[0]
            assert hasattr(stock, 'barcode')
            assert hasattr(stock, 'is_active')
            assert hasattr(stock, 'quantity')
            assert hasattr(stock.product, 'product_name')
            assert hasattr(stock.price, 'price_with_vat')
            
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")

def test_get_single_stock():
    service = StockService(
        username="test_username",
        password="test_password"
    )
    
    stock = service.get_single_stock("test_barcode")
    if stock:
        assert stock.barcode == "test_barcode"
        assert isinstance(stock.quantity, int)

def test_get_total_stock_count():
    service = StockService(
        username="test_username",
        password="test_password"
    )
    
    count = service.get_total_stock_count()
    assert isinstance(count, int)
    assert count >= 0

def test_get_all_stocks():
    service = StockService(
        username="test_username",
        password="test_password"
    )
    
    def test_callback(stocks, page, total):
        assert isinstance(stocks, list)
        assert page <= total
    
    all_stocks = service.get_all_stocks(batch_callback=test_callback)
    assert isinstance(all_stocks, list)
    
    if all_stocks:
        assert len(all_stocks) == service.get_total_stock_count()

if __name__ == "__main__":
    pytest.main([__file__]) 