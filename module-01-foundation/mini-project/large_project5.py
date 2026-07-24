# The Account Family - A Complete Banking System

from abc import ABC, abstractmethod
from datetime import datetime
import json

class Account(ABC):
    """
    Abstract base class for all bank accounts.
    This class defines the interface that all account types must implement.
    """
    
    def __init__(self, account_number, owner_name, initial_balance=0, currency="ETB"):
        """
        Initialize a new account.
        
        Args:
            account_number (str): Unique account identifier
            owner_name (str): Name of the account owner
            initial_balance (float): Starting balance (default 0)
            currency (str): Currency code (default "ETB")
        """
        self.account_number = account_number
        self.owner_name = owner_name
        self.currency = currency
        self.__balance = max(0, initial_balance)  # Private attribute
        self.created_at = datetime.now()
        self.transaction_history = []
        self.is_active = True
        
        # Record initial deposit if any
        if initial_balance > 0:
            self._add_transaction(f"Initial deposit: +{initial_balance:.2f} {currency}")
    
    @property
    def balance(self):
        """Getter for the private balance attribute"""
        return self.__balance
    
    @balance.setter
    def balance(self, value):
        """Protected setter for balance with validation"""
        if value < 0:
            raise ValueError("Balance cannot be negative!")
        self.__balance = value
    
    def deposit(self, amount):
        """
        Deposit money into the account.
        
        Args:
            amount (float): The amount to deposit
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_active:
            print(f"Account {self.account_number} is closed!")
            return False
            
        if amount <= 0:
            print("Deposit amount must be positive!")
            return False
            
        self.balance += amount
        self._add_transaction(f"Deposit: +{amount:.2f} {self.currency}")
        print(f"✅ Deposited {amount:.2f} {self.currency}. New balance: {self.balance:.2f} {self.currency}")
        return True
    
    @abstractmethod
    def withdraw(self, amount):
        """
        Withdraw money from the account.
        Subclasses must implement their own withdrawal logic.
        
        Args:
            amount (float): The amount to withdraw
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass
    
    def transfer(self, target_account, amount):
        """
        Transfer money to another account.
        
        Args:
            target_account (Account): The account to transfer to
            amount (float): The amount to transfer
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_active or not target_account.is_active:
            print("One or both accounts are closed!")
            return False
            
        if amount <= 0:
            print("Transfer amount must be positive!")
            return False
            
        # Try to withdraw from this account
        if self.withdraw(amount):
            # If withdrawal successful, deposit to target
            target_account.deposit(amount)
            self._add_transaction(f"Transfer to {target_account.owner_name}: -{amount:.2f} {self.currency}")
            target_account._add_transaction(f"Transfer from {self.owner_name}: +{amount:.2f} {self.currency}")
            print(f"🔄 Transferred {amount:.2f} {self.currency} to {target_account.owner_name}")
            return True
        
        return False
    
    def _add_transaction(self, description):
        """Add a transaction to the history"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_history.append({
            "timestamp": timestamp,
            "description": description,
            "balance": self.balance
        })
    
    def get_transaction_history(self):
        """Return the transaction history"""
        return self.transaction_history.copy()
    
    def display_info(self):
        """Display account information"""
        print("=" * 60)
        print(f"🏦 Account Type: {self.__class__.__name__}")
        print(f"📋 Account Number: {self.account_number}")
        print(f"👤 Owner: {self.owner_name}")
        print(f"💰 Balance: {self.balance:.2f} {self.currency}")
        print(f"📅 Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 Status: {'Active' if self.is_active else 'Closed'}")
        print(f"📝 Transactions: {len(self.transaction_history)}")
        self._display_additional_info()
        print("=" * 60)
    
    def _display_additional_info(self):
        """Hook for subclasses to add their own info"""
        pass
    
    def display_transactions(self, limit=10):
        """Display recent transactions"""
        if not self.transaction_history:
            print("📭 No transactions yet.")
            return
            
        print(f"\n📜 Transaction History for {self.owner_name} (last {min(limit, len(self.transaction_history))}):")
        print("-" * 60)
        for transaction in self.transaction_history[-limit:]:
            print(f"  {transaction['timestamp']} | {transaction['description']}")
            print(f"  Balance: {transaction['balance']:.2f} {self.currency}")
            print("-" * 60)
    
    def close_account(self):
        """Close the account"""
        if self.is_active:
            self.is_active = False
            self._add_transaction("Account closed")
            print(f"🔒 Account {self.account_number} has been closed.")
        else:
            print(f"Account {self.account_number} is already closed.")
    
    def __str__(self):
        """String representation of the account"""
        return f"{self.__class__.__name__}({self.account_number}) - {self.owner_name}: {self.balance:.2f} {self.currency}"
    
    def to_dict(self):
        """Convert account to dictionary for JSON serialization"""
        return {
            "type": self.__class__.__name__,
            "account_number": self.account_number,
            "owner_name": self.owner_name,
            "balance": self.balance,
            "currency": self.currency,
            "created_at": self.created_at.isoformat(),
            "is_active": self.is_active,
            "transaction_history": self.transaction_history
        }


class SavingsAccount(Account):
    """
    Savings account with interest and minimum balance requirement.
    """
    
    def __init__(self, account_number, owner_name, initial_balance=0, 
                 interest_rate=0.05, minimum_balance=100, currency="ETB"):
        """
        Initialize a savings account.
        
        Args:
            account_number (str): The account number
            owner_name (str): The name of the account owner
            initial_balance (float): Starting balance
            interest_rate (float): Annual interest rate (default 5%)
            minimum_balance (float): Minimum required balance (default 100 ETB)
            currency (str): Currency code
        """
        super().__init__(account_number, owner_name, initial_balance, currency)
        self.interest_rate = interest_rate
        self.minimum_balance = minimum_balance
        self.last_interest_date = datetime.now()
        self.withdrawal_count = 0
        self.monthly_withdrawal_limit = 3  # Limited withdrawals
    
    def withdraw(self, amount):
        """
        Withdraw money from savings account with minimum balance check.
        
        Args:
            amount (float): The amount to withdraw
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_active:
            print(f"Account {self.account_number} is closed!")
            return False
            
        if amount <= 0:
            print("Withdrawal amount must be positive!")
            return False
            
        # Check monthly withdrawal limit
        if self.withdrawal_count >= self.monthly_withdrawal_limit:
            print(f"❌ Monthly withdrawal limit ({self.monthly_withdrawal_limit}) exceeded!")
            return False
            
        if amount > self.balance:
            print(f"❌ Insufficient funds! Balance: {self.balance:.2f} {self.currency}")
            return False
            
        new_balance = self.balance - amount
        if new_balance < self.minimum_balance:
            print(f"❌ Cannot withdraw. Minimum balance of {self.minimum_balance:.2f} {self.currency} required!")
            return False
            
        self.balance = new_balance
        self.withdrawal_count += 1
        self._add_transaction(f"Withdrawal: -{amount:.2f} {self.currency}")
        print(f"✅ Withdrew {amount:.2f} {self.currency}. New balance: {self.balance:.2f} {self.currency}")
        return True
    
    def add_interest(self):
        """Add interest to the account balance"""
        if not self.is_active:
            print(f"Account {self.account_number} is closed!")
            return
            
        interest = self.balance * self.interest_rate
        self.balance += interest
        self.last_interest_date = datetime.now()
        self._add_transaction(f"Interest: +{interest:.2f} {self.currency} ({self.interest_rate*100:.1f}%)")
        print(f"💰 Added interest: {interest:.2f} {self.currency}. New balance: {self.balance:.2f} {self.currency}")
    
    def reset_monthly_withdrawals(self):
        """Reset the monthly withdrawal counter"""
        self.withdrawal_count = 0
        print(f"✅ Monthly withdrawal count reset for {self.owner_name}")
    
    def _display_additional_info(self):
        """Display savings-specific information"""
        print(f"📈 Interest Rate: {self.interest_rate * 100:.1f}%")
        print(f"💰 Minimum Balance: {self.minimum_balance:.2f} {self.currency}")
        print(f"📊 Withdrawals this month: {self.withdrawal_count}/{self.monthly_withdrawal_limit}")
        print(f"📅 Last Interest: {self.last_interest_date.strftime('%Y-%m-%d')}")


class CheckingAccount(Account):
    """
    Checking account with overdraft protection.
    """
    
    def __init__(self, account_number, owner_name, initial_balance=0, 
                 overdraft_limit=200, monthly_fee=10, currency="ETB"):
        """
        Initialize a checking account.
        
        Args:
            account_number (str): The account number
            owner_name (str): The name of the account owner
            initial_balance (float): Starting balance
            overdraft_limit (float): Maximum overdraft allowed (default 200 ETB)
            monthly_fee (float): Monthly maintenance fee (default 10 ETB)
            currency (str): Currency code
        """
        super().__init__(account_number, owner_name, initial_balance, currency)
        self.overdraft_limit = overdraft_limit
        self.monthly_fee = monthly_fee
        self.transaction_count = 0
        self.free_transactions = 10  # Free transactions per month
    
    def withdraw(self, amount):
        """
        Withdraw money from checking account with overdraft protection.
        
        Args:
            amount (float): The amount to withdraw
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_active:
            print(f"Account {self.account_number} is closed!")
            return False
            
        if amount <= 0:
            print("Withdrawal amount must be positive!")
            return False
            
        max_withdrawal = self.balance + self.overdraft_limit
        
        if amount > max_withdrawal:
            print(f"❌ Insufficient funds! Balance: {self.balance:.2f} {self.currency}, Overdraft limit: {self.overdraft_limit:.2f} {self.currency}")
            return False
            
        new_balance = self.balance - amount
        self.balance = new_balance
        
        # Charge overdraft fee if going negative
        if new_balance < 0:
            fee = 25  # Overdraft fee
            self.balance -= fee
            self._add_transaction(f"Overdraft: -{amount:.2f} {self.currency} (Fee: {fee:.2f} {self.currency})")
            print(f"⚠️ Overdraft! Withdrew {amount:.2f} {self.currency}. Fee charged: {fee:.2f} {self.currency}")
            print(f"   New balance: {self.balance:.2f} {self.currency}")
        else:
            self._add_transaction(f"Withdrawal: -{amount:.2f} {self.currency}")
            print(f"✅ Withdrew {amount:.2f} {self.currency}. New balance: {self.balance:.2f} {self.currency}")
        
        self.transaction_count += 1
        return True
    
    def apply_monthly_fee(self):
        """Apply the monthly maintenance fee"""
        if not self.is_active:
            return
            
        self.balance -= self.monthly_fee
        self._add_transaction(f"Monthly fee: -{self.monthly_fee:.2f} {self.currency}")
        print(f"💳 Monthly fee applied: {self.monthly_fee:.2f} {self.currency}")
        self.transaction_count = 0  # Reset transaction counter
    
    def _display_additional_info(self):
        """Display checking-specific information"""
        print(f"💳 Overdraft Limit: {self.overdraft_limit:.2f} {self.currency}")
        print(f"📊 Monthly Fee: {self.monthly_fee:.2f} {self.currency}")
        print(f"📊 Transactions: {self.transaction_count}/{self.free_transactions} free this month")


class FixedDepositAccount(Account):
    """
    Fixed deposit account with lock-in period and higher interest.
    """
    
    def __init__(self, account_number, owner_name, initial_balance=0, 
                 interest_rate=0.08, lock_period_months=12, currency="ETB"):
        """
        Initialize a fixed deposit account.
        
        Args:
            account_number (str): The account number
            owner_name (str): The name of the account owner
            initial_balance (float): Starting balance (min 1000 ETB recommended)
            interest_rate (float): Annual interest rate (default 8%)
            lock_period_months (int): Lock-in period in months (default 12)
            currency (str): Currency code
        """
        super().__init__(account_number, owner_name, initial_balance, currency)
        self.interest_rate = interest_rate
        self.lock_period_months = lock_period_months
        self.start_date = datetime.now()
        self.maturity_date = datetime.now().replace(
            month=datetime.now().month + lock_period_months
        )
        self.early_withdrawal_penalty = 0.02  # 2% penalty for early withdrawal
        self.is_matured = False
    
    def withdraw(self, amount):
        """
        Withdraw from fixed deposit with early withdrawal penalties.
        
        Args:
            amount (float): The amount to withdraw
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_active:
            print(f"Account {self.account_number} is closed!")
            return False
            
        if amount <= 0:
            print("Withdrawal amount must be positive!")
            return False
            
        if amount > self.balance:
            print(f"❌ Insufficient funds! Balance: {self.balance:.2f} {self.currency}")
            return False
            
        # Check if mature
        now = datetime.now()
        is_early = now < self.maturity_date
        
        if is_early:
            print(f"⚠️ Early withdrawal penalty of {self.early_withdrawal_penalty*100:.1f}% applies!")
            penalty = amount * self.early_withdrawal_penalty
            total_deduction = amount + penalty
            
            if total_deduction > self.balance:
                print(f"❌ Insufficient funds after penalty! Need: {total_deduction:.2f} {self.currency}")
                return False
            
            self.balance -= total_deduction
            self._add_transaction(f"Early withdrawal: -{amount:.2f} {self.currency} (Penalty: {penalty:.2f} {self.currency})")
            print(f"✅ Withdrew {amount:.2f} {self.currency} (Early). Penalty: {penalty:.2f} {self.currency}")
        else:
            self.balance -= amount
            self._add_transaction(f"Withdrawal: -{amount:.2f} {self.currency}")
            print(f"✅ Withdrew {amount:.2f} {self.currency}. New balance: {self.balance:.2f} {self.currency}")
        
        print(f"   New balance: {self.balance:.2f} {self.currency}")
        return True
    
    def add_interest(self):
        """Add interest to the fixed deposit"""
        if not self.is_active:
            return
            
        interest = self.balance * self.interest_rate
        self.balance += interest
        self._add_transaction(f"Interest: +{interest:.2f} {self.currency} ({self.interest_rate*100:.1f}%)")
        print(f"💰 Added interest: {interest:.2f} {self.currency}. New balance: {self.balance:.2f} {self.currency}")
    
    def check_maturity(self):
        """Check if the deposit has matured"""
        if datetime.now() >= self.maturity_date and not self.is_matured:
            self.is_matured = True
            # Apply bonus interest for maturity
            bonus = self.balance * 0.01  # 1% maturity bonus
            self.balance += bonus
            self._add_transaction(f"Maturity bonus: +{bonus:.2f} {self.currency}")
            print(f"🎉 Fixed deposit has matured! Bonus interest: {bonus:.2f} {self.currency}")
            return True
        return False
    
    def _display_additional_info(self):
        """Display fixed deposit-specific information"""
        print(f"📈 Interest Rate: {self.interest_rate * 100:.1f}%")
        print(f"🔒 Lock Period: {self.lock_period_months} months")
        print(f"📅 Start Date: {self.start_date.strftime('%Y-%m-%d')}")
        print(f"📅 Maturity Date: {self.maturity_date.strftime('%Y-%m-%d')}")
        print(f"📊 Status: {'Matured' if self.is_matured else 'Locked'}")
        print(f"⚠️ Early Withdrawal Penalty: {self.early_withdrawal_penalty*100:.1f}%")


class Bank:
    """
    Bank class to manage multiple accounts.
    """
    
    def __init__(self, name):
        self.name = name
        self.accounts = {}
        self.total_transactions = 0
    
    def add_account(self, account):
        """Add an account to the bank"""
        if account.account_number in self.accounts:
            print(f"Account {account.account_number} already exists!")
            return False
        
        self.accounts[account.account_number] = account
        print(f"✅ Account {account.account_number} added to {self.name}")
        return True
    
    def get_account(self, account_number):
        """Get an account by number"""
        return self.accounts.get(account_number)
    
    def display_all_accounts(self):
        """Display all accounts"""
        if not self.accounts:
            print("No accounts in the bank.")
            return
        
        print(f"\n🏛️ {self.name} - All Accounts")
        print("=" * 60)
        total_balance = 0
        for account in self.accounts.values():
            print(f"  {account}")
            total_balance += account.balance
        print("-" * 60)
        print(f"Total Balance: {total_balance:.2f} ETB")
        print(f"Total Accounts: {len(self.accounts)}")
    
    def save_to_file(self, filename="bank_data.json"):
        """Save all account data to a JSON file"""
        data = {
            "bank_name": self.name,
            "accounts": []
        }
        
        for account in self.accounts.values():
            account_data = {
                "type": account.__class__.__name__,
                "account_number": account.account_number,
                "owner_name": account.owner_name,
                "balance": account.balance,
                "currency": account.currency,
                "is_active": account.is_active,
                "created_at": account.created_at.isoformat(),
                "transaction_history": account.transaction_history
            }
            
            # Add type-specific data
            if isinstance(account, SavingsAccount):
                account_data.update({
                    "interest_rate": account.interest_rate,
                    "minimum_balance": account.minimum_balance,
                    "withdrawal_count": account.withdrawal_count
                })
            elif isinstance(account, CheckingAccount):
                account_data.update({
                    "overdraft_limit": account.overdraft_limit,
                    "monthly_fee": account.monthly_fee,
                    "transaction_count": account.transaction_count
                })
            elif isinstance(account, FixedDepositAccount):
                account_data.update({
                    "interest_rate": account.interest_rate,
                    "lock_period_months": account.lock_period_months,
                    "start_date": account.start_date.isoformat(),
                    "maturity_date": account.maturity_date.isoformat(),
                    "is_matured": account.is_matured
                })
            
            data["accounts"].append(account_data)
        
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        
        print(f"💾 Data saved to {filename}")
    
    def load_from_file(self, filename="bank_data.json"):
        """Load account data from a JSON file"""
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            
            self.name = data["bank_name"]
            self.accounts = {}
            
            for acc_data in data["accounts"]:
                account_type = acc_data["type"]
                if account_type == "SavingsAccount":
                    account = SavingsAccount(
                        acc_data["account_number"],
                        acc_data["owner_name"],
                        acc_data["balance"],
                        acc_data.get("interest_rate", 0.05),
                        acc_data.get("minimum_balance", 100),
                        acc_data.get("currency", "ETB")
                    )
                    account.withdrawal_count = acc_data.get("withdrawal_count", 0)
                elif account_type == "CheckingAccount":
                    account = CheckingAccount(
                        acc_data["account_number"],
                        acc_data["owner_name"],
                        acc_data["balance"],
                        acc_data.get("overdraft_limit", 200),
                        acc_data.get("monthly_fee", 10),
                        acc_data.get("currency", "ETB")
                    )
                    account.transaction_count = acc_data.get("transaction_count", 0)
                elif account_type == "FixedDepositAccount":
                    account = FixedDepositAccount(
                        acc_data["account_number"],
                        acc_data["owner_name"],
                        acc_data["balance"],
                        acc_data.get("interest_rate", 0.08),
                        acc_data.get("lock_period_months", 12),
                        acc_data.get("currency", "ETB")
                    )
                    account.is_matured = acc_data.get("is_matured", False)
                else:
                    continue
                
                account.is_active = acc_data.get("is_active", True)
                account.transaction_history = acc_data.get("transaction_history", [])
                self.accounts[account.account_number] = account
            
            print(f"📂 Data loaded from {filename}")
            return True
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return False
        except json.JSONDecodeError:
            print(f"Error reading {filename}. File may be corrupted.")
            return False


# Test the banking system
if __name__ == "__main__":
    print("🏦 Welcome to the Account Family Banking System")
    print("=" * 70)
    
    # Create a bank
    bank = Bank("Ethiopian National Bank")
    
    # Create different account types
    savings = SavingsAccount("SAV001", "Alem Tesfaye", 1000, 0.05, 100)
    checking = CheckingAccount("CHK001", "Bekele Hailu", 500, 200)
    fixed = FixedDepositAccount("FIX001", "Chaltu Abebe", 5000, 0.08, 12)
    
    # Add accounts to bank
    bank.add_account(savings)
    bank.add_account(checking)
    bank.add_account(fixed)
    
    # Test savings account
    print("\n📊 SAVINGS ACCOUNT TEST")
    print("-" * 40)
    savings.display_info()
    savings.deposit(200)
    savings.withdraw(50)
    savings.withdraw(1000)  # Should fail (minimum balance)
    savings.add_interest()
    savings.display_transactions()
    
    # Test checking account
    print("\n📊 CHECKING ACCOUNT TEST")
    print("-" * 40)
    checking.display_info()
    checking.deposit(100)
    checking.withdraw(700)  # Should use overdraft
    checking.withdraw(100)  # Should fail
    checking.apply_monthly_fee()
    checking.display_transactions()
    
    # Test fixed deposit account
    print("\n📊 FIXED DEPOSIT ACCOUNT TEST")
    print("-" * 40)
    fixed.display_info()
    fixed.deposit(1000)
    fixed.add_interest()
    fixed.withdraw(2000)  # Early withdrawal with penalty
    fixed.display_transactions()
    
    # Test transfers
    print("\n💸 TRANSFER TEST")
    print("-" * 40)
    savings.transfer(checking, 100)
    checking.transfer(savings, 50)
    
    # Display all accounts
    bank.display_all_accounts()
    
    # Demonstrate polymorphism
    print("\n🎯 POLYMORPHISM DEMONSTRATION")
    print("-" * 40)
    accounts = [savings, checking, fixed]
    for account in accounts:
        print(f"\nAccount Type: {account.__class__.__name__}")
        print(f"Owner: {account.owner_name}")
        print(f"Balance: {account.balance:.2f} {account.currency}")
        account.withdraw(50)  # Each type handles withdrawal differently
        print("-" * 40)
    
    # Save data
    print("\n💾 SAVE/LOAD DEMONSTRATION")
    print("-" * 40)
    bank.save_to_file("bank_data.json")
    
    # Create a new bank and load data
    new_bank = Bank("New Bank")
    new_bank.load_from_file("bank_data.json")
    new_bank.display_all_accounts()
    
    print("\n✨ Account Family V2 complete! Ready for SOLID principles and design patterns!")