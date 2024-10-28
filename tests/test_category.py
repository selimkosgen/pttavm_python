import pytest
from pttavm.services.category_service import CategoryService

def test_get_category():
    service = CategoryService(
        username="test_username",
        password="test_password"
    )
    
    category = service.get_category(1)
    
    assert category is not None
    assert category.id == 1
    assert category.name is not None
    assert isinstance(category.children, list)
