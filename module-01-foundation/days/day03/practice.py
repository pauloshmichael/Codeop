# 1. Unique cities
print("=== Unique Cities ===")
cities = ["Addis Ababa", "Nairobi", "Addis Ababa", "Cairo", "Nairobi", "Lagos", "Addis Ababa"]
unique_cities = set(cities)
print("Distinct cities:", unique_cities)
print("Number of distinct cities:", len(unique_cities))

# 2. Price report
print("=== Price Report ===")
grocery_prices = {
    "Tej": 350,
    "Coffee": 450,
    "Injera": 120,
    "Doro Wat": 650,
    "Shiro": 280
}
print("Grocery items and prices in ETB:")
for item, price in grocery_prices.items():
    print(f"{item}: {price} ETB")

# 3. Tax comprehension
print("=== Tax Comprehension ===")
prices = [100, 250, 400, 80]
prices_with_tax = [price * 1.15 for price in prices]
print(f"Original prices: {prices}")
print(f"Prices with 15% tax: {prices_with_tax}")

# 4. Cheap items
print("=== Cheap Items ===")
cheap_items = [price for price in prices if price < 200]
print(f"Original prices: {prices}")
print(f"Prices under 200: {cheap_items}")

# 5. Write & read
print("=== Write & Read ===")
customer_names = ["Alem", "Bekele", "Chaltu"]

# Write names to file
with open("names.txt", "w") as file:
    for name in customer_names:
        file.write(name + "\n")
print("Customer names written to names.txt")

# Read names from file
print("Customer names from file:")
with open("names.txt", "r") as file:
    for line in file:
        print(line.strip())  # strip() removes the newline character

# 6. Safe division
print("=== Safe Division ===")
try:
    number = float(input("Enter a number to divide 1000 by: "))
    result = 1000 / number
    print(f"1000 divided by {number} equals {result:.2f}")
except ValueError:
    print("Error: Please enter a valid number!")
except ZeroDivisionError:
    print("Error: Cannot divide by zero!")
print()
