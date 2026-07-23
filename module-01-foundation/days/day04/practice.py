
# 1. Book class
print("=== Book Class ===")
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
    
    def describe(self):
        return f"'{self.title}' by {self.author}, {self.pages} pages"

# Create two books
book1 = Book("The Alchemist", "Paulo Coelho", 163)
book2 = Book("Dertogada", "Yishmake Werku", 544)

print(book1.describe())
print(book2.describe())

# 2. Product class
print("=== Product Class ===")
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price  # in ETB
        self.quantity = quantity
    
    def restock(self, n):
        if n > 0:
            self.quantity += n
            print(f"Restocked {n} units of {self.name}. New quantity: {self.quantity}")
        else:
            print("Restock amount must be positive")
    
    def sell(self, n):
        if n > 0 and n <= self.quantity:
            self.quantity -= n
            print(f"Sold {n} units of {self.name}. New quantity: {self.quantity}")
        elif n > self.quantity:
            print(f"Not enough stock! Only {self.quantity} units available")
        else:
            print("Sell amount must be positive")

# Test Product class
product = Product("Coffee", 450, 10)
print(f"Product: {product.name}, Price: {product.price} ETB, Stock: {product.quantity}")
product.restock(5)
product.sell(3)
print()

# 3. Make it private
print("=== Private Attribute ===")
class PrivateProduct:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.__quantity = quantity  # Private attribute
    
    @property
    def quantity(self):
        """Getter for private quantity"""
        return self.__quantity
    
    def restock(self, n):
        if n > 0:
            self.__quantity += n
            print(f"Restocked {n} units of {self.name}. New quantity: {self.__quantity}")
        else:
            print("Restock amount must be positive")
    
    def sell(self, n):
        if n > 0 and n <= self.__quantity:
            self.__quantity -= n
            print(f"Sold {n} units of {self.name}. New quantity: {self.__quantity}")
        elif n > self.__quantity:
            print(f"Not enough stock! Only {self.__quantity} units available")
        else:
            print("Sell amount must be positive")

# Test private attribute
p1 = PrivateProduct("Tej", 350, 20)
print(f"Product: {p1.name}, Price: {p1.price} ETB, Stock: {p1.quantity}")  # Using getter
p1.restock(10)
p1.sell(5)
print()

# 4. Validate - Add setter to prevent negative quantity
print("=== Validation ===")
class ValidatedProduct:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.__quantity = max(0, quantity)  # Ensure initial quantity isn't negative
    
    @property
    def quantity(self):
        return self.__quantity
    
    @quantity.setter
    def quantity(self, value):
        """Prevent quantity from going below zero"""
        if value < 0:
            print("Error: Cannot set quantity below zero!")
            self.__quantity = 0
        else:
            self.__quantity = value
    
    def restock(self, n):
        if n > 0:
            self.__quantity += n
            print(f"Restocked {n} units. New quantity: {self.__quantity}")
        else:
            print("Restock amount must be positive")
    
    def sell(self, n):
        if n > 0:
            if n <= self.__quantity:
                self.__quantity -= n
                print(f"Sold {n} units. New quantity: {self.__quantity}")
            else:
                print(f"Not enough stock! Only {self.__quantity} units available")
        else:
            print("Sell amount must be positive")

# Test validation
vp = ValidatedProduct("Injera", 120, 5)
print(f"Product: {vp.name}, Stock: {vp.quantity}")
vp.sell(3)  # Works
vp.sell(3)  # Should show error (not enough stock)
vp.quantity = -5  # Should show error and set to 0
print(f"Stock after validation: {vp.quantity}")
print()

# 5. Prove independence
print("=== Prove Independence ===")
class IndependentProduct:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.__quantity = max(0, quantity)
    
    @property
    def quantity(self):
        return self.__quantity
    
    @quantity.setter
    def quantity(self, value):
        if value < 0:
            print(f"Error: Cannot set quantity below zero for {self.name}!")
            self.__quantity = 0
        else:
            self.__quantity = value
    
    def restock(self, n):
        if n > 0:
            self.__quantity += n
            print(f"{self.name}: Restocked {n} units. New: {self.__quantity}")
        else:
            print("Restock amount must be positive")
    
    def sell(self, n):
        if n > 0:
            if n <= self.__quantity:
                self.__quantity -= n
                print(f"{self.name}: Sold {n} units. Remaining: {self.__quantity}")
            else:
                print(f"{self.name}: Not enough stock! Only {self.__quantity} available")
        else:
            print("Sell amount must be positive")

# Create three products
prod1 = IndependentProduct("Coffee", 450, 10)
prod2 = IndependentProduct("Tea", 200, 15)
prod3 = IndependentProduct("Juice", 100, 8)

print("Initial quantities:")
print(f"{prod1.name}: {prod1.quantity}")
print(f"{prod2.name}: {prod2.quantity}")
print(f"{prod3.name}: {prod3.quantity}")

print("\nChanging only Product 1:")
prod1.restock(20)
prod1.sell(5)
prod1.quantity = 30

print("\nAll products after changes:")
print(f"{prod1.name}: {prod1.quantity}")
print(f"{prod2.name}: {prod2.quantity}")
print(f"{prod3.name}: {prod3.quantity}")

print("\nDemonstrating independence - Product 2 and 3 are unchanged!")
print()

print("All exercises completed!")