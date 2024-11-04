import pytest
from pttavm.client import PTTClient
from pttavm.models.product_update import ProductUpdateV2, ProductImage, ProductPart
from pttavm.models.variant import Variant, VariantAttribute, ValidationError
from datetime import datetime

@pytest.fixture
def client():
    return PTTClient(
        username="test_user",
        password="test_pass"
    )

def test_product_update_validation():
    """Test product update model validation"""
    # Valid update
    product = ProductUpdateV2(
        barcode="test-123",
        product_name="Test Product",
        product_code="test-123",
        category_id=1,
        price_without_vat=100,
        vat_rate=18
    )
    assert product.barcode == "test-123"
    
    # Missing required fields
    with pytest.raises(ValidationError):
        ProductUpdateV2(
            product_name="Test",
            product_code="test",
            category_id=1
        )
    
    # Invalid values
    with pytest.raises(ValidationError):
        ProductUpdateV2(
            barcode="test-123",
            product_name="Test",
            product_code="test",
            category_id=1,
            price_without_vat=-100,  # Negative price
            vat_rate=18
        )

def test_product_image_validation():
    """Test product image model validation"""
    # Valid image
    image = ProductImage(
        url="https://example.com/image.jpg",
        order=1
    )
    assert image.url == "https://example.com/image.jpg"
    
    # Invalid order
    with pytest.raises(ValueError):
        ProductImage(
            url="https://example.com/image.jpg",
            order=0  # Must be positive
        )
    
    # Empty URL
    with pytest.raises(ValueError):
        ProductImage(
            url="",
            order=1
        )

def test_product_part_validation():
    """Test product part model validation"""
    # Valid part
    part = ProductPart(
        part_no=1,
        desi=5,
        comment="Test"
    )
    assert part.part_no == 1
    
    # Invalid part number
    with pytest.raises(ValueError):
        ProductPart(
            part_no=0,  # Must be positive
            desi=5
        )
    
    # Negative desi
    with pytest.raises(ValueError):
        ProductPart(
            part_no=1,
            desi=-5  # Cannot be negative
        )

def test_update_product_v2(client):
    """Test product update v2 service"""
    product = ProductUpdateV2(
        barcode="test-123",
        product_name="Test Product",
        product_code="test-123",
        category_id=1,
        price_without_vat=100,
        vat_rate=18
    )
    
    result = client.update_product_v2(product)
    assert isinstance(result, bool)

def test_update_products_v2_bulk(client):
    """Test bulk product update v2 service"""
    products = [
        ProductUpdateV2(
            barcode="test-123",
            product_name="Test Product 1",
            product_code="test-123",
            category_id=1,
            price_without_vat=100,
            vat_rate=18
        ),
        ProductUpdateV2(
            barcode="test-124",
            product_name="Test Product 2",
            product_code="test-124",
            category_id=1,
            price_without_vat=200,
            vat_rate=18
        )
    ]
    
    result = client.update_products_v2_bulk(products)
    assert isinstance(result, bool)

    # Test validation for maximum products
    with pytest.raises(ValidationError):
        # Create more than 100 products
        many_products = [
            ProductUpdateV2(
                barcode=f"test-{i}",
                product_name=f"Test Product {i}",
                product_code=f"test-{i}",
                category_id=1,
                price_without_vat=100,
                vat_rate=18
            )
            for i in range(101)  # API limit is 100
        ]
        client.update_products_v2_bulk(many_products)