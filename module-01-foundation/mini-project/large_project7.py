import json
from datetime import datetime
from typing import Dict, Optional, List

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
    """Simple account with transaction history"""
    
    def __init__(self, account_number: str, owner_name: str, initial_balance: float = 0):
        self.account_number = account_number
        self.owner_name = owner_name
        self._balance = max(0, initial_balance)
        self.is_active = True
        self.created_at = datetime.now()
        self.transactions = []  # Stack (list) for transaction history
        
        # Record initial deposit if any
        if initial_balance > 0:
            self._add_transaction(initial_balance, "Initial deposit")
    
    @property
    def balance(self):
        return self._balance
    
    def deposit(self, amount: float):
        """Deposit money"""
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
        """Withdraw money"""
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
        """Add transaction to history (stack)"""
        transaction = Transaction(amount, description, self._balance)
        self.transactions.append(transaction)  # Push onto stack
    
    def get_recent_transactions(self, count: int = 5):
        """Get recent transactions (pop from stack)"""
        if not self.transactions:
            print("No transactions yet")
            return []
        
        # Get most recent transactions (LIFO)
        recent = self.transactions[-count:] if count > 0 else []
        return recent
    
    def undo_last_transaction(self):
        """Undo last transaction - demonstrates stack functionality"""
        if not self.transactions:
            print("No transactions to undo")
            return False
        
        # Pop the last transaction
        last = self.transactions.pop()
        print(f"↩️ Undoing: {last.description}")
        
        # Reverse the transaction
        if "Deposit" in last.description:
            self._balance -= last.amount
        elif "Withdrawal" in last.description:
            self._balance += last.amount
        
        print(f"Balance restored to: {self._balance:.2f}")
        return True
    
    def close(self):
        """Close the account"""
        self.is_active = False
        print(f"🔒 Account {self.account_number} closed")
    
    def display_info(self):
        """Display account information"""
        print("=" * 50)
        print(f"Account: {self.account_number}")
        print(f"Owner: {self.owner_name}")
        print(f"Balance: {self._balance:.2f} ETB")
        print(f"Status: {'Active' if self.is_active else 'Closed'}")
        print(f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"Transactions: {len(self.transactions)}")
        print("=" * 50)
    
    def display_transactions(self, count: int = 5):
        """Display recent transactions"""
        if not self.transactions:
            print("No transactions yet")
            return
        
        print(f"\nLast {min(count, len(self.transactions))} transactions (most recent first):")
        print("-" * 40)
        # Show most recent first (stack behavior)
        for transaction in reversed(self.transactions[-count:]):
            print(f"  {transaction}")
        print("-" * 40)
    
    def __str__(self):
        return f"{self.account_number} - {self.owner_name}: {self._balance:.2f} ETB"

# ============================================
# Account Registry - Uses Dictionary for O(1) Lookup
# ============================================

class AccountRegistry:
    """
    Registry that stores accounts in a dictionary for O(1) access
    """
    
    def __init__(self):
        self.accounts: Dict[str, Account] = {}  # O(1) lookup by account number
        self.next_account_number = 1001
    
    def create_account(self, owner_name: str, initial_balance: float = 0) -> Account:
        """
        Create a new account with auto-generated account number
        O(1) - dictionary insertion
        """
        account_number = f"ACC{self.next_account_number}"
        self.next_account_number += 1
        
        account = Account(account_number, owner_name, initial_balance)
        self.accounts[account_number] = account  # O(1)
        print(f"✅ Account {account_number} created for {owner_name}")
        return account
    
    def get_account(self, account_number: str) -> Optional[Account]:
        """
        Get account by number - O(1) dictionary lookup
        """
        return self.accounts.get(account_number)
    
    def delete_account(self, account_number: str):
        """
        Delete account - O(1) dictionary deletion
        """
        if account_number in self.accounts:
            self.accounts[account_number].close()
            del self.accounts[account_number]  # O(1)
            print(f"🗑️ Account {account_number} removed from registry")
        else:
            print(f"Account {account_number} not found")
    
    def get_all_accounts(self) -> List[Account]:
        """
        Get all accounts - O(n)
        """
        return list(self.accounts.values())
    
    def get_total_balance(self) -> float:
        """
        Calculate total balance of all accounts - O(n)
        """
        total = sum(account.balance for account in self.accounts.values())
        return total
    
    def find_by_owner(self, owner_name: str) -> List[Account]:
        """
        Find accounts by owner name - O(n)
        """
        return [acc for acc in self.accounts.values() if acc.owner_name.lower() == owner_name.lower()]
    
    def display_all(self):
        """
        Display all accounts in the registry
        """
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
        """
        Save all accounts to a JSON file
        """
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
        """
        Load accounts from a JSON file
        """
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
                
                # Restore transaction history
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
    print("=" * 60)
    print("ACCOUNT REGISTRY - O(1) Lookup with Transaction Stacks")
    print("=" * 60)
    
    # Create registry
    registry = AccountRegistry()
    print("\n1. Creating accounts:")
    print("-" * 40)
    
    # Create accounts
    acc1 = registry.create_account("Alem Tesfaye", 1000)
    acc2 = registry.create_account("Bekele Hailu", 500)
    acc3 = registry.create_account("Chaltu Abebe", 2000)
    
    # Perform transactions
    print("\n2. Performing transactions:")
    print("-" * 40)
    acc1.deposit(200)
    acc1.withdraw(50)
    acc1.withdraw(100)
    
    acc2.deposit(300)
    acc2.withdraw(100)
    
    acc3.deposit(500)
    
    # Show account details
    print("\n3. Account details with transaction history:")
    print("-" * 40)
    for account in registry.get_all_accounts():
        account.display_info()
        account.display_transactions(3)
        print()
    
    # Demonstrate O(1) lookup
    print("\n4. O(1) Lookup Demonstration:")
    print("-" * 40)
    
    # Fast lookup by account number
    search_number = "ACC1001"
    print(f"Looking up account {search_number}...")
    start = datetime.now()
    found_account = registry.get_account(search_number)  # O(1)
    lookup_time = (datetime.now() - start).microseconds
    print(f"Found: {found_account}")
    print(f"Lookup time: {lookup_time} microseconds")
    print("✓ Dictionary provides O(1) lookup!")
    
    # Show transaction stack
    print("\n5. Transaction Stack (LIFO) Demonstration:")
    print("-" * 40)
    print("Most recent transactions (showing stack behavior):")
    acc1.display_transactions(5)
    
    # Undo last transaction (stack pop)
    print("\n6. Undoing last transaction (stack pop):")
    print("-" * 40)
    acc1.undo_last_transaction()
    acc1.undo_last_transaction()
    
    print("\n7. Final state:")
    print("-" * 40)
    registry.display_all()
    
    # Save and load
    print("\n8. Save and Load:")
    print("-" * 40)
    registry.save_to_file("accounts.json")
    
    # Create new registry and load
    new_registry = AccountRegistry()
    new_registry.load_from_file("accounts.json")
    new_registry.display_all()
    
    print("\n" + "=" * 60)
    print("✅ Account Registry Demo Complete!")
    print("Key Features:")
    print("  ✓ O(1) lookup using dictionary")
    print("  ✓ Transaction history as a stack")
    print("  ✓ Undo last transaction (pop from stack)")
    print("  ✓ Save/Load to JSON")
    print("=" * 60)

if __name__ == "__main__":
    demo()