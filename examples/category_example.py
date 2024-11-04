from pttavm import PTTClient
import os

def main():
    client = PTTClient(
        username=os.getenv("PTT_USERNAME"),
        password=os.getenv("PTT_PASSWORD")
    )
    
    # Ana kategoriyi al
    category = client.get_category(1)
    
    if category:
        print(f"Ana Kategori: {category.name}")
        print(f"ID: {category.id}")
        
        # Alt kategorileri göster
        for child in category.children:
            print(f"\nAlt kategori: {child.name}")
            print(f"ID: {child.id}")

if __name__ == "__main__":
    main()
