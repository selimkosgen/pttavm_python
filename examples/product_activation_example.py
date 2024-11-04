from pttavm import PTTClient
from pttavm.models.product import ProductUpdateError
import os

def main():
    client = PTTClient(
        username=os.getenv("PTT_USERNAME"),
        password=os.getenv("PTT_PASSWORD")
    )
    
    # Ürünü aktif yap
    try:
        product_id = 744444957
        result = client.activate_product(product_id, is_active=True)
        print(f"Ürün aktivasyon: {'Başarılı' if result else 'Başarısız'}")
        
    except ProductUpdateError as e:
        print(f"Aktivasyon hatası: {e}")
    except Exception as e:
        print(f"Beklenmeyen hata: {e}")

    # Ürünü pasif yap
    try:
        result = client.activate_product(product_id, is_active=False)
        print(f"Ürün deaktivasyon: {'Başarılı' if result else 'Başarısız'}")
        
    except ProductUpdateError as e:
        print(f"Deaktivasyon hatası: {e}")
    except Exception as e:
        print(f"Beklenmeyen hata: {e}")

if __name__ == "__main__":
    main() 