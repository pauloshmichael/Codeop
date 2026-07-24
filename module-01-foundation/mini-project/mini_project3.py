# --- Mini-Project: Pharmacy Inventory Tracker ---
print("=== Pharmacy Inventory Tracker ===")
print("(Mini-Project)")

# Initialize inventory
inventory = {
    "Paracetamol": {"price": 45, "stock": 100},
    "Amoxicillin": {"price": 120, "stock": 50},
    "Ibuprofen": {"price": 80, "stock": 75},
    "Vitamin C": {"price": 60, "stock": 200},
    "Antacid": {"price": 55, "stock": 30}
}

# Display current inventory
print("\nCurrent Pharmacy Inventory:")
print("-" * 50)
for item, details in inventory.items():
    print(f"{item}: {details['stock']} units at {details['price']} ETB each")
print("-" * 50)

# Interactive stock checker
while True:
    print("\nOptions:")
    print("1. Check stock for an item")
    print("2. Update stock quantity")
    print("3. Add new item")
    print("4. Save inventory to file")
    print("5. Load inventory from file")
    print("6. Exit")
    
    choice = input("Enter your choice (1-6): ")
    
    if choice == "1":
        item = input("Enter item name: ")
        if item in inventory:
            details = inventory[item]
            print(f"{item}: {details['stock']} units in stock, Price: {details['price']} ETB")
        else:
            print(f"Item '{item}' not found in inventory!")
    
    elif choice == "2":
        item = input("Enter item name: ")
        if item in inventory:
            try:
                new_stock = int(input(f"Enter new stock quantity for {item}: "))
                if new_stock < 0:
                    print("Error: Stock cannot be negative!")
                else:
                    inventory[item]["stock"] = new_stock
                    print(f"Updated {item} stock to {new_stock} units")
            except ValueError:
                print("Error: Please enter a valid number!")
        else:
            print(f"Item '{item}' not found in inventory!")
    
    elif choice == "3":
        item = input("Enter new item name: ")
        if item in inventory:
            print(f"Item '{item}' already exists!")
        else:
            try:
                price = float(input("Enter price in ETB: "))
                stock = int(input("Enter initial stock quantity: "))
                if price < 0 or stock < 0:
                    print("Error: Price and stock cannot be negative!")
                else:
                    inventory[item] = {"price": price, "stock": stock}
                    print(f"Added '{item}' to inventory with price {price} ETB and stock {stock}")
            except ValueError:
                print("Error: Please enter valid numbers!")
    
    elif choice == "4":
        try:
            with open("pharmacy_inventory.txt", "w") as file:
                for item, details in inventory.items():
                    file.write(f"{item},{details['price']},{details['stock']}\n")
            print("Inventory saved to pharmacy_inventory.txt")
        except Exception as e:
            print(f"Error saving to file: {e}")
    
    elif choice == "5":
        try:
            with open("pharmacy_inventory.txt", "r") as file:
                inventory.clear()
                for line in file:
                    parts = line.strip().split(",")
                    if len(parts) == 3:
                        item, price, stock = parts
                        inventory[item] = {"price": float(price), "stock": int(stock)}
            print("Inventory loaded from pharmacy_inventory.txt")
            print("Current inventory:")
            for item, details in inventory.items():
                print(f"{item}: {details['stock']} units at {details['price']} ETB each")
        except FileNotFoundError:
            print("Error: pharmacy_inventory.txt not found!")
        except Exception as e:
            print(f"Error loading from file: {e}")
    
    elif choice == "6":
        print("Exiting Pharmacy Inventory Tracker. Goodbye!")
        break
    
    else:
        print("Invalid choice. Please enter a number from 1-6.")

print("\nAll exercises completed!")
