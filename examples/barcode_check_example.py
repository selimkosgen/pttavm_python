from pttavm import PTTClient
from pttavm.models.barcode import BarcodeError
import os

def main():
    client = PTTClient(
        username=os.getenv("PTT_USERNAME"),
        password=os.getenv("PTT_PASSWORD")
    )
    
    # Tekil barkod kontrolü
    try:
        result = client.check_barcode("part-test-10x5")
        print(f"\nTekil Barkod Kontrolü:")
        print(f"Barkod: {result.barcode}")
        print(f"Mevcut: {'Evet' if result.exists else 'Hayır'}")
        if result.message:
            print(f"Mesaj: {result.message}")
            
    except BarcodeError as e:
        print(f"Barkod kontrol hatası: {e}")

    # Toplu barkod kontrolü
    try:
        barcodes = [
            "tkmkbarbie-1066mx2",
            "tkmkbarbie-1066"
        ]
        
        results = client.check_barcodes_bulk(barcodes)
        
        print(f"\nToplu Barkod Kontrolü:")
        for result in results:
            print(f"\nBarkod: {result.barcode}")
            print(f"Mevcut: {'Evet' if result.exists else 'Hayır'}")
            if result.message:
                print(f"Mesaj: {result.message}")
                
    except BarcodeError as e:
        print(f"Toplu barkod kontrol hatası: {e}")

if __name__ == "__main__":
    main() 