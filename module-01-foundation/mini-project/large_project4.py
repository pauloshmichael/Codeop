# The Account Class (V1) - Larger Project

class Account:
    def __init__(self, account_number, owner_name, initial_balance=0):
        self.account_number = account_number
        self.owner_name = owner_name
        self.__balance = max(0, initial_balance)  # Private attribute, cannot go negative
    
    @property
    def balance(self):
        """Getter for the private balance attribute"""
        return self.__balance
    
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"Deposited {amount:.2f} ETB. New balance: {self.__balance:.2f} ETB")
            return True
        else:
            print("Deposit amount must be positive!")
            return False
    
    def withdraw(self, amount):
        if amount > 0:
            if amount <= self.__balance:
                self.__balance -= amount
                print(f"Withdrew {amount:.2f} ETB. New balance: {self.__balance:.2f} ETB")
                return True
            else:
                print(f"Insufficient funds! Balance: {self.__balance:.2f} ETB")
                return False
        else:
            print("Withdrawal amount must be positive!")
            return False
    
    def display_info(self):
        print("=" * 40)
        print(f"Account Number: {self.account_number}")
        print(f"Owner Name: {self.owner_name}")
        print(f"Current Balance: {self.__balance:.2f} ETB")
        print("=" * 40)
    
    def __str__(self):
        """String representation of the account"""
        return f"Account({self.account_number}) - {self.owner_name}: {self.__balance:.2f} ETB"


# Test the Account class
if __name__ == "__main__":
    print("=== Account Class Test ===")
    
    # Create accounts
    acc1 = Account("ETH001", "Alem Tesfaye", 1000)
    acc2 = Account("ETH002", "Bekele Hailu", 500)
    
    # Display initial info
    acc1.display_info()
    acc2.display_info()
    
    # Perform transactions
    print("\n--- Transactions ---")
    acc1.deposit(250)
    acc1.withdraw(100)
    acc1.withdraw(2000)  # Should fail
    
    acc2.deposit(300)
    acc2.withdraw(200)
    
    # Display final info
    print("\n--- Final Account Status ---")
    acc1.display_info()
    acc2.display_info()
    
    # Test string representation
    print("\n--- String Representation ---")
    print(acc1)
    print(acc2)
    
    print("\nAccount class V1 ready. This will be extended in future days!")