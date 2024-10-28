import os
from pttavm.client import PTTAVMClient

def print_category(category, level=0):
    """Helper function to print category hierarchy"""
    indent = "  " * level
    print(f"{indent}ID: {category.id}, Name: {category.name}")
    if category.children:
        for child in category.children:
            print_category(child, level + 1)

def main():
    # Get credentials from environment variables
    username = os.getenv('PTT_USERNAME')
    password = os.getenv('PTT_PASSWORD')
    
    if not username or not password:
        print("Error: PTT_USERNAME and PTT_PASSWORD environment variables must be set")
        return
    
    # Initialize client
    client = PTTAVMClient(
        username=username,
        password=password
    )
    
    try:
        # Get category service
        category_service = client.get_category_service()
        
        # Get root category and its children
        category = category_service.get_categories()
        
        if category and category.success:
            print("\nCategory Hierarchy:")
            print_category(category)
            
            print("\nCategory Details:")
            print(f"ID: {category.id}")
            print(f"Name: {category.name}")
            print(f"Parent ID: {category.parent_id}")
            print(f"Updated At: {category.updated_at}")
            print(f"Number of children: {len(category.children) if category.children else 0}")
        else:
            print("Failed to get categories")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()
