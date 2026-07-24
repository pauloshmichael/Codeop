import json
from datetime import datetime
from typing import Dict, Optional, List, Tuple

# ============================================
# Transaction Class
# ============================================

class Transaction:
    """Simple transaction record"""
    def __init__(self, amount: float, description: str, balance_after: float):
        self.timestamp = datetime.now()
        self.amount = amount
        self.description = description
        self.balance_after = balance_after
    
    def __str__(self):
        return f"{self.timestamp.strftime('%H:%M:%S')} | {self.description} | Balance: {self.balance_after:.2f}"

# ============================================
# Account Class
# ============================================

class Account:
    """Account with transaction history"""
    
    def __init__(self, account_number: str, owner_name: str, initial_balance: float = 0):
        self.account_number = account_number
        self.owner_name = owner_name
        self._balance = max(0, initial_balance)
        self.is_active = True
        self.created_at = datetime.now()
        self.transactions = []
        
        if initial_balance > 0:
            self._add_transaction(initial_balance, "Initial deposit")
    
    @property
    def balance(self):
        return self._balance
    
    def deposit(self, amount: float):
        if amount <= 0:
            print("Amount must be positive!")
            return False
        
        if not self.is_active:
            print("Account is closed!")
            return False
        
        self._balance += amount
        self._add_transaction(amount, f"Deposit: +{amount:.2f}")
        print(f"✅ Deposited {amount:.2f}. New balance: {self._balance:.2f}")
        return True
    
    def withdraw(self, amount: float):
        if amount <= 0:
            print("Amount must be positive!")
            return False
        
        if not self.is_active:
            print("Account is closed!")
            return False
        
        if amount > self._balance:
            print(f"Insufficient funds! Balance: {self._balance:.2f}")
            return False
        
        self._balance -= amount
        self._add_transaction(amount, f"Withdrawal: -{amount:.2f}")
        print(f"✅ Withdrew {amount:.2f}. New balance: {self._balance:.2f}")
        return True
    
    def _add_transaction(self, amount: float, description: str):
        transaction = Transaction(amount, description, self._balance)
        self.transactions.append(transaction)
    
    def get_recent_transactions(self, count: int = 5):
        if not self.transactions:
            return []
        return self.transactions[-count:]
    
    def close(self):
        self.is_active = False
        print(f"🔒 Account {self.account_number} closed")
    
    def display_info(self):
        print("=" * 50)
        print(f"Account: {self.account_number}")
        print(f"Owner: {self.owner_name}")
        print(f"Balance: {self._balance:.2f} ETB")
        print(f"Status: {'Active' if self.is_active else 'Closed'}")
        print(f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"Transactions: {len(self.transactions)}")
        print("=" * 50)
    
    def __str__(self):
        return f"{self.account_number} - {self.owner_name}: {self._balance:.2f} ETB"

# ============================================
# Account Registry with Search & Sort
# ============================================

class AccountRegistry:
    """Registry with search and sort capabilities"""
    
    def __init__(self):
        self.accounts: Dict[str, Account] = {}
        self.next_account_number = 1001
    
    def create_account(self, owner_name: str, initial_balance: float = 0) -> Account:
        """Create a new account"""
        account_number = f"ACC{self.next_account_number}"
        self.next_account_number += 1
        
        account = Account(account_number, owner_name, initial_balance)
        self.accounts[account_number] = account
        print(f"✅ Account {account_number} created for {owner_name}")
        return account
    
    def get_account(self, account_number: str) -> Optional[Account]:
        """O(1) dictionary lookup"""
        return self.accounts.get(account_number)
    
    def get_all_accounts(self) -> List[Account]:
        """Get all accounts"""
        return list(self.accounts.values())
    
    # ============================================
    # NEW: Binary Search by Account Number
    # ============================================
    
    def binary_search_account(self, target_number: str) -> Optional[Account]:
        """
        Binary search for account by number
        Requires sorted list of account numbers
        O(log n) time complexity
        """
        # Get sorted account numbers
        sorted_numbers = sorted(self.accounts.keys())
        
        left = 0
        right = len(sorted_numbers) - 1
        
        while left <= right:
            mid = (left + right) // 2
            mid_number = sorted_numbers[mid]
            
            if mid_number == target_number:
                return self.accounts[mid_number]
            elif mid_number < target_number:
                left = mid + 1
            else:
                right = mid - 1
        
        return None
    
    # ============================================
    # NEW: Recursive Transaction Total
    # ============================================
    
    def recursive_transaction_total(self, account_number: str) -> float:
        """
        Recursively calculate total of all transactions for an account
        O(n) time complexity
        """
        account = self.get_account(account_number)
        if not account:
            print(f"Account {account_number} not found")
            return 0
        
        # Use recursive helper
        return self._recursive_sum(account.transactions, 0)
    
    def _recursive_sum(self, transactions, index: int) -> float:
        """Helper function for recursive sum"""
        # Base case: reached end of list
        if index >= len(transactions):
            return 0
        
        # Recursive case: current transaction amount + sum of rest
        return transactions[index].amount + self._recursive_sum(transactions, index + 1)
    
    # ============================================
    # NEW: Balance Leaderboard
    # ============================================
    
    def get_balance_leaderboard(self, ascending: bool = False) -> List[Tuple[str, float]]:
        """
        Get accounts sorted by balance
        O(n log n) time complexity
        """
        # Create list of (owner_name, balance)
        balances = [(acc.owner_name, acc.balance) for acc in self.accounts.values()]
        
        # Sort by balance
        return sorted(balances, key=lambda x: x[1], reverse=not ascending)
    
    def display_leaderboard(self, top_n: int = None):
        """Display balance leaderboard"""
        leaderboard = self.get_balance_leaderboard(ascending=False)
        
        if top_n:
            leaderboard = leaderboard[:top_n]
        
        print("\n" + "=" * 50)
        print("BALANCE LEADERBOARD (Highest to Lowest)")
        print("=" * 50)
        
        if not leaderboard:
            print("No accounts found")
            return
        
        rank = 1
        for name, balance in leaderboard:
            print(f"  #{rank:2d} {name:20s} {balance:10.2f} ETB")
            rank += 1
        print("=" * 50)
    
    # ============================================
    # NEW: Recursive Search by Owner Name
    # ============================================
    
    def recursive_find_by_owner(self, owner_name: str, index: int = 0) -> List[Account]:
        """
        Recursively find accounts by owner name
        O(n) time complexity
        """
        accounts_list = list(self.accounts.values())
        
        # Base case: reached end of list
        if index >= len(accounts_list):
            return []
        
        # Check current account
        result = []
        if owner_name.lower() in accounts_list[index].owner_name.lower():
            result.append(accounts_list[index])
        
        # Recursive case: check rest of list
        result.extend(self.recursive_find_by_owner(owner_name, index + 1))
        
        return result
    
    # ============================================
    # Utility Methods
    # ============================================
    
    def get_total_balance(self) -> float:
        """Calculate total balance of all accounts"""
        return sum(account.balance for account in self.accounts.values())
    
    def display_all(self):
        """Display all accounts"""
        if not self.accounts:
            print("No accounts in registry")
            return
        
        print("\n" + "=" * 60)
        print(f"ACCOUNT REGISTRY - Total: {len(self.accounts)} accounts")
        print("=" * 60)
        for account in self.accounts.values():
            print(f"  {account}")
        print("-" * 60)
        print(f"Total Balance: {self.get_total_balance():.2f} ETB")
        print("=" * 60)
    
    def save_to_file(self, filename: str = "accounts.json"):
        """Save accounts to JSON"""
        data = {
            "next_account_number": self.next_account_number,
            "accounts": []
        }
        
        for account in self.accounts.values():
            account_data = {
                "account_number": account.account_number,
                "owner_name": account.owner_name,
                "balance": account.balance,
                "is_active": account.is_active,
                "created_at": account.created_at.isoformat(),
                "transactions": [
                    {
                        "amount": t.amount,
                        "description": t.description,
                        "balance_after": t.balance_after,
                        "timestamp": t.timestamp.isoformat()
                    }
                    for t in account.transactions
                ]
            }
            data["accounts"].append(account_data)
        
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"💾 Data saved to {filename}")
    
    def load_from_file(self, filename: str = "accounts.json"):
        """Load accounts from JSON"""
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            
            self.accounts = {}
            self.next_account_number = data.get("next_account_number", 1001)
            
            for acc_data in data["accounts"]:
                account = Account(
                    acc_data["account_number"],
                    acc_data["owner_name"],
                    acc_data["balance"]
                )
                account.is_active = acc_data.get("is_active", True)
                account.created_at = datetime.fromisoformat(acc_data["created_at"])
                
                for t_data in acc_data.get("transactions", []):
                    transaction = Transaction(
                        t_data["amount"],
                        t_data["description"],
                        t_data["balance_after"]
                    )
                    transaction.timestamp = datetime.fromisoformat(t_data["timestamp"])
                    account.transactions.append(transaction)
                
                self.accounts[account.account_number] = account
            
            print(f"📂 Loaded {len(self.accounts)} accounts from {filename}")
            return True
        except FileNotFoundError:
            print(f"File {filename} not found")
            return False
        except Exception as e:
            print(f"Error loading: {e}")
            return False

# ============================================
# Demo
# ============================================

def demo():
    print("=" * 70)
    print("ACCOUNT REGISTRY WITH SEARCH & SORT")
    print("=" * 70)
    
    # Create registry
    registry = AccountRegistry()
    
    # Create accounts with various balances
    print("\n1. Creating accounts:")
    print("-" * 40)
    
    accounts_data = [
        ("Alem Tesfaye", 1500),
        ("Bekele Hailu", 800),
        ("Chaltu Abebe", 2000),
        ("Dawit Mengistu", 1200),
        ("Eden Girma", 3000),
        ("Fikir Tadesse", 500),
        ("Genet Assefa", 2500),
        ("Henok Desta", 1800)
    ]
    
    for name, balance in accounts_data:
        registry.create_account(name, balance)
    
    # Perform some transactions
    print("\n2. Performing transactions:")
    print("-" * 40)
    
    acc1 = registry.get_account("ACC1001")
    acc1.deposit(200)
    acc1.withdraw(50)
    acc1.withdraw(100)
    
    acc2 = registry.get_account("ACC1003")
    acc2.deposit(300)
    acc2.deposit(100)
    
    acc3 = registry.get_account("ACC1005")
    acc3.withdraw(150)
    
    # Display all accounts
    print("\n3. All accounts:")
    print("-" * 40)
    registry.display_all()
    
    # ============================================
    # NEW FEATURE 1: Balance Leaderboard
    # ============================================
    
    print("\n4. Balance Leaderboard:")
    print("-" * 40)
    registry.display_leaderboard(top_n=5)
    
    # ============================================
    # NEW FEATURE 2: Binary Search
    # ============================================
    
    print("\n5. Binary Search by Account Number:")
    print("-" * 40)
    
    # Test binary search
    test_numbers = ["ACC1001", "ACC1005", "ACC1010", "ACC1008"]
    
    for number in test_numbers:
        account = registry.binary_search_account(number)
        if account:
            print(f"✅ Found: {account}")
        else:
            print(f"❌ Account {number} not found")
    
    # Show O(log n) advantage
    print("\nBinary Search Performance:")
    print("  ✓ O(log n) - Much faster than linear search for large datasets")
    print("  ✓ Requires sorted list of account numbers")
    
    # ============================================
    # NEW FEATURE 3: Recursive Transaction Total
    # ============================================
    
    print("\n6. Recursive Transaction Total:")
    print("-" * 40)
    
    # Calculate total for each account
    for acc in registry.get_all_accounts():
        if len(acc.transactions) > 1:  # Only show accounts with transactions
            total = registry.recursive_transaction_total(acc.account_number)
            print(f"  {acc.owner_name}:")
            print(f"    Number of transactions: {len(acc.transactions)}")
            print(f"    Total transaction amount: {total:.2f} ETB")
    
    # ============================================
    # NEW FEATURE 4: Recursive Search by Owner
    # ============================================
    
    print("\n7. Recursive Search by Owner Name:")
    print("-" * 40)
    
    search_name = "Alem"
    found = registry.recursive_find_by_owner(search_name)
    print(f"Searching for accounts with '{search_name}':")
    if found:
        for acc in found:
            print(f"  ✅ {acc}")
    else:
        print("  No accounts found")
    
    search_name = "Abebe"
    found = registry.recursive_find_by_owner(search_name)
    print(f"\nSearching for accounts with '{search_name}':")
    if found:
        for acc in found:
            print(f"  ✅ {acc}")
    else:
        print("  No accounts found")
    
    # ============================================
    # Performance Comparison
    # ============================================
    
    print("\n8. Performance Comparison:")
    print("-" * 40)
    
    # O(1) vs O(log n) vs O(n)
    print("Lookup Methods:")
    print("  • Dictionary (O(1)): Immediate access")
    print("  • Binary Search (O(log n)): Fast for large datasets")
    print("  • Linear Search (O(n)): Slower for large datasets")
    
    print("\nSorting Methods:")
    print("  • Built-in sorted() (O(n log n)): Optimized")
    print("  • Balance Leaderboard: Uses sorted() with key")
    
    print("\nRecursive Methods:")
    print("  • Transaction Total: O(n) - visits each transaction")
    print("  • Search by Owner: O(n) - checks each account")
    
    # ============================================
    # Save and Load
    # ============================================
    
    print("\n9. Save and Load:")
    print("-" * 40)
    registry.save_to_file("accounts.json")
    
    new_registry = AccountRegistry()
    new_registry.load_from_file("accounts.json")
    print("\nLoaded registry:")
    new_registry.display_leaderboard()
    
    print("\n" + "=" * 70)
    print("✅ Account Registry with Search & Sort Complete!")
    print("New Features Added:")
    print("  ✓ Balance Leaderboard (sorted by balance)")
    print("  ✓ Binary Search by Account Number (O(log n))")
    print("  ✓ Recursive Transaction Total (O(n))")
    print("  ✓ Recursive Search by Owner Name (O(n))")
    print("=" * 70)

if __name__ == "__main__":
    demo()