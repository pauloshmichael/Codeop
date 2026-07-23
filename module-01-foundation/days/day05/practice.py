# day05/account.py
# The Account Family - Extended from Day 4

from abc import ABC, abstractmethod

class Account(ABC):
    """
    Abstract base class for bank accounts.
    This is the base class that all account types will inherit from.
    """
    
    def __init__(self, account_number, owner_name, initial_balance=0):
        """
        Initialize a new account with account number, owner name, and initial balance.
        
        Args:
            account_number (str): The account number
            owner_name (str): The name of the account owner
            initial_balance (float): Starting balance (default 0)
        """
        self.account_number = account_number
        self.owner_name = owner_name
        self.__balance = max(0, initial_balance)  # Private attribute
        self.transaction_history = []  # Track all transactions
    
    @property
    def balance(self):
        """Getter for the private balance attribute"""
        return self.__balance
    
    def deposit(self, amount):
        """
        Deposit money into the account.
        
        Args:
            amount (float): The amount to deposit
            
        Returns:
            bool: True if successful, False otherwise
        """
        if amount > 0:
            self.__balance += amount
            self._add_transaction(f"Deposit: +{amount:.2f} ETB")
            print(f"Deposited {amount:.2f} ETB. New balance: {self.__balance:.2f} ETB")
            return True
        else:
            print("Deposit amount must be positive!")
            return False
    
    def withdraw(self, amount):
        """
        Withdraw money from the account.
        This is an abstract method - subclasses must implement their own logic.
        
        Args:
            amount (float): The amount to withdraw
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    def _add_transaction(self, description):
        """Add a transaction to the history"""
        self.transaction_history.append(description)
    
    def get_transaction_history(self):
        """Return the transaction history"""
        return self.transaction_history.copy()
    
    def display_info(self):
        """Display account information"""
        print("=" * 50)
        print(f"Account Type: {self.__class__.__name__}")
        print(f"Account Number: {self.account_number}")
        print(f"Owner Name: {self.owner_name}")
        print(f"Current Balance: {self.__balance:.2f} ETB")
        print("=" * 50)
    
    def display_transactions(self):
        """Display all transactions"""
        if not self.transaction_history:
            print("No transactions yet.")
        else:
            print(f"Transaction History for {self.owner_name}:")
            for i, transaction in enumerate(self.transaction_history, 1):
                print(f"  {i}. {transaction}")
    
    def __str__(self):
        """String representation of the account"""
        return f"{self.__class__.__name__}({self.account_number}) - {self.owner_name}: {self.__balance:.2f} ETB"


class SavingsAccount(Account):
    """
    Savings account with interest and minimum balance requirement.
    """
    
    def __init__(self, account_number, owner_name, initial_balance=0, interest_rate=0.05, minimum_balance=100):
        """
        Initialize a savings account.
        
        Args:
            account_number (str): The account number
            owner_name (str): The name of the account owner
            initial_balance (float): Starting balance
            interest_rate (float): Annual interest rate (default 5%)
            minimum_balance (float): Minimum required balance (default 100 ETB)
        """
        super().__init__(account_number, owner_name, initial_balance)
        self.interest_rate = interest_rate
        self.minimum_balance = minimum_balance
    
    def withdraw(self, amount):
        """
        Withdraw money from savings account with minimum balance check.
        
        Args:
            amount (float): The amount to withdraw
            
        Returns:
            bool: True if successful, False otherwise
        """
        if amount > 0:
            if amount <= self.balance:
                new_balance = self.balance - amount
                if new_balance >= self.minimum_balance:
                    self._add_transaction(f"Withdrawal: -{amount:.2f} ETB")
                    self.__class__.balance.fset(self, new_balance)  # Access private balance
                    print(f"Withdrew {amount:.2f} ETB. New balance: {self.balance:.2f} ETB")
                    return True
                else:
                    print(f"Cannot withdraw. Minimum balance of {self.minimum_balance:.2f} ETB required!")
                    return False
            else:
                print(f"Insufficient funds! Balance: {self.balance:.2f} ETB")
                return False
        else:
            print("Withdrawal amount must be positive!")
            return False
    
    def add_interest(self):
        """Add interest to the account balance"""
        interest = self.balance * self.interest_rate
        self._add_transaction(f"Interest: +{interest:.2f} ETB")
        self.__class__.balance.fset(self, self.balance + interest)  # Access private balance
        print(f"Added interest: {interest:.2f} ETB. New balance: {self.balance:.2f} ETB")
    
    def display_info(self):
        """Override display_info to include savings-specific information"""
        super().display_info()
        print(f"Interest Rate: {self.interest_rate * 100}%")
        print(f"Minimum Balance: {self.minimum_balance:.2f} ETB")


class CheckingAccount(Account):
    """
    Checking account with overdraft protection.
    """
    
    def __init__(self, account_number, owner_name, initial_balance=0, overdraft_limit=200):
        """
        Initialize a checking account.
        
        Args:
            account_number (str): The account number
            owner_name (str): The name of the account owner
            initial_balance (float): Starting balance
            overdraft_limit (float): Maximum overdraft allowed (default 200 ETB)
        """
        super().__init__(account_number, owner_name, initial_balance)
        self.overdraft_limit = overdraft_limit
    
    def withdraw(self, amount):
        """
        Withdraw money from checking account with overdraft protection.
        
        Args:
            amount (float): The amount to withdraw
            
        Returns:
            bool: True if successful, False otherwise
        """
        if amount > 0:
            if amount <= self.balance + self.overdraft_limit:
                new_balance = self.balance - amount
                self.__class__.balance.fset(self, new_balance)  # Access private balance
                if new_balance < 0:
                    self._add_transaction(f"Overdraft Withdrawal: -{amount:.2f} ETB (New balance: {new_balance:.2f})")
                    print(f"Warning: Overdraft! Withdrew {amount:.2f} ETB. New balance: {new_balance:.2f} ETB")
                else:
                    self._add_transaction(f"Withdrawal: -{amount:.2f} ETB")
                    print(f"Withdrew {amount:.2f} ETB. New balance: {new_balance:.2f} ETB")
                return True
            else:
                print(f"Insufficient funds! Balance: {self.balance:.2f} ETB, Overdraft limit: {self.overdraft_limit:.2f} ETB")
                return False
        else:
            print("Withdrawal amount must be positive!")
            return False
    
    def display_info(self):
        """Override display_info to include checking-specific information"""
        super().display_info()
        print(f"Overdraft Limit: {self.overdraft_limit:.2f} ETB")


class FixedDepositAccount(Account):
    """
    Fixed deposit account with lock-in period and higher interest.
    """
    
    def __init__(self, account_number, owner_name, initial_balance=0, interest_rate=0.08, lock_period_months=12):
        """
        Initialize a fixed deposit account.
        
        Args:
            account_number (str): The account number
            owner_name (str): The name of the account owner
            initial_balance (float): Starting balance
            interest_rate (float): Annual interest rate (default 8%)
            lock_period_months (int): Lock-in period in months (default 12)
        """
        super().__init__(account_number, owner_name, initial_balance)
        self.interest_rate = interest_rate
        self.lock_period_months = lock_period_months
        self.maturity_date = f"{lock_period_months} months from now"
    
    def withdraw(self, amount):
        """
        Withdraw from fixed deposit (may be restricted before maturity).
        
        Args:
            amount (float): The amount to withdraw
            
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"Warning: Fixed deposit account. Early withdrawal may incur penalties.")
        if amount > 0:
            if amount <= self.balance:
                # In reality, we'd check maturity here
                new_balance = self.balance - amount
                self.__class__.balance.fset(self, new_balance)  # Access private balance
                penalty = amount * 0.02  # 2% penalty for early withdrawal
                if penalty > 0:
                    self.__class__.balance.fset(self, self.balance - penalty)
                    self._add_transaction(f"Withdrawal: -{amount:.2f} ETB (Penalty: {penalty:.2f} ETB)")
                    print(f"Withdrew {amount:.2f} ETB with early withdrawal penalty of {penalty:.2f} ETB")
                else:
                    self._add_transaction(f"Withdrawal: -{amount:.2f} ETB")
                    print(f"Withdrew {amount:.2f} ETB. New balance: {self.balance:.2f} ETB")
                return True
            else:
                print(f"Insufficient funds! Balance: {self.balance:.2f} ETB")
                return False
        else:
            print("Withdrawal amount must be positive!")
            return False
    
    def add_interest(self):
        """Add interest to the fixed deposit"""
        interest = self.balance * self.interest_rate
        self._add_transaction(f"Interest: +{interest:.2f} ETB")
        self.__class__.balance.fset(self, self.balance + interest)
        print(f"Added interest: {interest:.2f} ETB. New balance: {self.balance:.2f} ETB")
    
    def display_info(self):
        """Override display_info to include fixed deposit information"""
        super().display_info()
        print(f"Interest Rate: {self.interest_rate * 100}%")
        print(f"Lock Period: {self.lock_period_months} months")
        print(f"Maturity: {self.maturity_date}")


# Test the account family
if __name__ == "__main__":
    print("=== Account Family Test ===")
    
    # Create different account types
    savings = SavingsAccount("SAV001", "Alem Tesfaye", 1000, 0.05, 100)
    checking = CheckingAccount("CHK001", "Bekele Hailu", 500, 200)
    fixed = FixedDepositAccount("FIX001", "Chaltu Abebe", 5000, 0.08, 12)
    
    # Test savings account
    print("\n--- Savings Account ---")
    savings.display_info()
    savings.deposit(200)
    savings.withdraw(50)
    savings.withdraw(1000)  # Should fail (minimum balance)
    savings.add_interest()
    savings.display_transactions()
    
    # Test checking account
    print("\n--- Checking Account ---")
    checking.display_info()
    checking.deposit(100)
    checking.withdraw(700)  # Should use overdraft
    checking.withdraw(100)  # Should fail
    checking.display_transactions()
    
    # Test fixed deposit account
    print("\n--- Fixed Deposit Account ---")
    fixed.display_info()
    fixed.deposit(1000)
    fixed.add_interest()
    fixed.withdraw(2000)
    fixed.display_transactions()
    
    # Demonstrate polymorphism
    print("\n--- Polymorphism Demonstration ---")
    accounts = [savings, checking, fixed]
    for account in accounts:
        print(f"\n{account}")  # Uses __str__ method
        print(f"Type: {account.__class__.__name__}")
        print(f"Balance: {account.balance:.2f} ETB")
        # Try to withdraw a small amount from each
        account.withdraw(50)
    
    print("\nAccount family V2 ready. Next: SOLID principles and design patterns!")