import json
from datetime import datetime
from typing import Dict, Optional, List, Set, Tuple
from collections import deque

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
        self.branch = None  # Which branch this account belongs to
        
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
    
    def transfer_to(self, target_account, amount: float):
        """Transfer money to another account"""
        if amount <= 0:
            print("Amount must be positive!")
            return False
        
        if not self.is_active or not target_account.is_active:
            print("One or both accounts are closed!")
            return False
        
        if amount > self._balance:
            print(f"Insufficient funds! Balance: {self._balance:.2f}")
            return False
        
        # Withdraw from this account
        self._balance -= amount
        self._add_transaction(amount, f"Transfer to {target_account.owner_name}: -{amount:.2f}")
        
        # Deposit to target account
        target_account._balance += amount
        target_account._add_transaction(amount, f"Transfer from {self.owner_name}: +{amount:.2f}")
        
        print(f"🔄 Transferred {amount:.2f} from {self.owner_name} to {target_account.owner_name}")
        return True
    
    def _add_transaction(self, amount: float, description: str):
        transaction = Transaction(amount, description, self._balance)
        self.transactions.append(transaction)
    
    def close(self):
        self.is_active = False
        print(f"🔒 Account {self.account_number} closed")
    
    def display_info(self):
        print("=" * 50)
        print(f"Account: {self.account_number}")
        print(f"Owner: {self.owner_name}")
        print(f"Balance: {self._balance:.2f} ETB")
        print(f"Branch: {self.branch if self.branch else 'None'}")
        print(f"Status: {'Active' if self.is_active else 'Closed'}")
        print(f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"Transactions: {len(self.transactions)}")
        print("=" * 50)
    
    def __str__(self):
        return f"{self.account_number} - {self.owner_name}: {self._balance:.2f} ETB"

# ============================================
# Branch Tree (Hierarchical Structure)
# ============================================

class Branch:
    """Branch node in the bank's organizational tree"""
    
    def __init__(self, name: str, parent=None):
        self.name = name
        self.parent = parent
        self.children = []  # Sub-branches
        self.accounts = []  # Accounts in this branch
    
    def add_child(self, branch_name: str):
        """Add a sub-branch"""
        child = Branch(branch_name, self)
        self.children.append(child)
        return child
    
    def add_account(self, account: Account):
        """Add an account to this branch"""
        self.accounts.append(account)
        account.branch = self.name
    
    def get_total_balance(self) -> float:
        """
        Recursively calculate total balance of this branch and all sub-branches
        """
        total = sum(acc.balance for acc in self.accounts)
        
        # Recursively add balances from sub-branches
        for child in self.children:
            total += child.get_total_balance()
        
        return total
    
    def display_tree(self, level: int = 0):
        """Display branch tree structure"""
        indent = "  " * level
        print(f"{indent}🏛️ {self.name} (Balance: {self.get_total_balance():.2f} ETB)")
        print(f"{indent}   Accounts: {len(self.accounts)}")
        
        for child in self.children:
            child.display_tree(level + 1)
    
    def find_account(self, account_number: str) -> Optional[Account]:
        """Search for an account in this branch and sub-branches"""
        # Check accounts in this branch
        for account in self.accounts:
            if account.account_number == account_number:
                return account
        
        # Recursively check sub-branches
        for child in self.children:
            result = child.find_account(account_number)
            if result:
                return result
        
        return None
    
    def get_all_accounts(self) -> List[Account]:
        """Get all accounts in this branch and sub-branches (recursive)"""
        all_accounts = self.accounts.copy()
        
        for child in self.children:
            all_accounts.extend(child.get_all_accounts())
        
        return all_accounts

# ============================================
# Transfer Graph (Network Structure)
# ============================================

class TransferGraph:
    """
    Graph representing transfers between accounts
    Vertices = accounts, Edges = transfers
    """
    
    def __init__(self):
        self.transfers = {}  # account_number -> set of connected account_numbers
    
    def add_transfer(self, from_account: Account, to_account: Account, amount: float):
        """
        Record a transfer in the graph
        Creates bidirectional edges
        """
        from_num = from_account.account_number
        to_num = to_account.account_number
        
        # Add edge from -> to
        if from_num not in self.transfers:
            self.transfers[from_num] = set()
        self.transfers[from_num].add(to_num)
        
        # Add edge to -> from (for undirected traversal)
        if to_num not in self.transfers:
            self.transfers[to_num] = set()
        self.transfers[to_num].add(from_num)
        
        print(f"  📊 Graph edge: {from_num} <-> {to_num}")
    
    def bfs(self, start_account: Account) -> Set[str]:
        """
        BFS traversal to find all accounts reachable through transfers
        """
        if start_account.account_number not in self.transfers:
            return {start_account.account_number}
        
        visited = set()
        queue = deque([start_account.account_number])
        visited.add(start_account.account_number)
        
        print(f"\nBFS traversal from {start_account.account_number}:")
        step = 1
        while queue:
            current = queue.popleft()
            print(f"  Step {step}: visiting {current}")
            step += 1
            
            # Visit all neighbors
            for neighbor in self.transfers.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return visited
    
    def dfs(self, start_account: Account) -> Set[str]:
        """
        DFS traversal to find all accounts reachable through transfers
        """
        visited = set()
        
        def dfs_recursive(account_num: str):
            visited.add(account_num)
            print(f"  Visiting: {account_num}")
            
            for neighbor in self.transfers.get(account_num, []):
                if neighbor not in visited:
                    dfs_recursive(neighbor)
        
        print(f"\nDFS traversal from {start_account.account_number}:")
        dfs_recursive(start_account.account_number)
        return visited
    
    def find_path(self, start: str, target: str) -> Optional[List[str]]:
        """
        BFS to find shortest path between two accounts
        """
        if start not in self.transfers or target not in self.transfers:
            return None
        
        visited = {start}
        queue = deque([(start, [start])])
        
        while queue:
            current, path = queue.popleft()
            
            if current == target:
                return path
            
            for neighbor in self.transfers.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def display_graph(self):
        """Display the transfer graph"""
        print("\nTransfer Graph:")
        print("-" * 40)
        if not self.transfers:
            print("No transfers yet")
            return
        
        for account, connections in self.transfers.items():
            print(f"  {account} -> {', '.join(connections)}")
        print("-" * 40)
    
    def get_reachable_accounts(self, account_number: str) -> Set[str]:
        """Get all accounts reachable through transfers (BFS)"""
        if account_number not in self.transfers:
            return {account_number}
        
        visited = set()
        queue = deque([account_number])
        visited.add(account_number)
        
        while queue:
            current = queue.popleft()
            for neighbor in self.transfers.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return visited

# ============================================
# Account Registry (Updated)
# ============================================

class AccountRegistry:
    """Registry with branch tree and transfer graph"""
    
    def __init__(self):
        self.accounts: Dict[str, Account] = {}
        self.next_account_number = 1001
        self.root_branch = Branch("Head Office")
        self.transfer_graph = TransferGraph()
    
    def create_account(self, owner_name: str, initial_balance: float = 0, branch_name: str = "Head Office") -> Account:
        """Create a new account"""
        account_number = f"ACC{self.next_account_number}"
        self.next_account_number += 1
        
        account = Account(account_number, owner_name, initial_balance)
        self.accounts[account_number] = account
        
        # Add to branch tree
        self._add_account_to_branch(account, branch_name)
        
        print(f"✅ Account {account_number} created for {owner_name} at {branch_name}")
        return account
    
    def _add_account_to_branch(self, account: Account, branch_name: str):
        """Add account to branch tree"""
        # Find branch (create if needed)
        branch = self._find_or_create_branch(branch_name)
        branch.add_account(account)
    
    def _find_or_create_branch(self, branch_name: str) -> Branch:
        """Find branch by name, create if doesn't exist"""
        # Split path (e.g., "Main/Addis/Sub")
        parts = branch_name.split('/')
        
        current = self.root_branch
        for part in parts:
            # Find child
            found = None
            for child in current.children:
                if child.name == part:
                    found = child
                    break
            
            if found is None:
                # Create new branch
                found = current.add_child(part)
            
            current = found
        
        return current
    
    def get_account(self, account_number: str) -> Optional[Account]:
        """O(1) dictionary lookup"""
        return self.accounts.get(account_number)
    
    def get_all_accounts(self) -> List[Account]:
        """Get all accounts"""
        return list(self.accounts.values())
    
    def transfer_money(self, from_acc_num: str, to_acc_num: str, amount: float):
        """
        Transfer money between accounts and record in graph
        """
        from_account = self.get_account(from_acc_num)
        to_account = self.get_account(to_acc_num)
        
        if not from_account or not to_account:
            print("One or both accounts not found!")
            return False
        
        if from_account.transfer_to(to_account, amount):
            # Record in transfer graph
            self.transfer_graph.add_transfer(from_account, to_account, amount)
            return True
        
        return False
    
    def get_branch_total(self, branch_name: str) -> float:
        """Get total balance of a branch and all sub-branches"""
        branch = self._find_branch(branch_name)
        if branch:
            return branch.get_total_balance()
        print(f"Branch '{branch_name}' not found")
        return 0
    
    def _find_branch(self, branch_name: str) -> Optional[Branch]:
        """Find branch by name in tree"""
        parts = branch_name.split('/')
        current = self.root_branch
        
        for part in parts:
            found = None
            for child in current.children:
                if child.name == part:
                    found = child
                    break
            if found is None:
                return None
            current = found
        
        return current
    
    def display_branch_tree(self):
        """Display the entire branch hierarchy"""
        print("\n" + "=" * 60)
        print("BANK BRANCH HIERARCHY")
        print("=" * 60)
        self.root_branch.display_tree()
        print("=" * 60)
    
    def display_all(self):
        """Display all accounts"""
        if not self.accounts:
            print("No accounts in registry")
            return
        
        print("\n" + "=" * 60)
        print(f"ACCOUNT REGISTRY - Total: {len(self.accounts)} accounts")
        print("=" * 60)
        for account in self.accounts.values():
            print(f"  {account} (Branch: {account.branch})")
        print("-" * 60)
        print(f"Total Balance: {sum(acc.balance for acc in self.accounts.values()):.2f} ETB")
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
                "branch": account.branch,
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
                account.branch = acc_data.get("branch")
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
    print("ACCOUNT REGISTRY WITH BRANCH TREE & TRANSFER GRAPH")
    print("=" * 70)
    
    # Create registry
    registry = AccountRegistry()
    
    # Create branch hierarchy
    print("\n1. Creating Branch Hierarchy:")
    print("-" * 40)
    
    # Create accounts at different branches
    acc1 = registry.create_account("Alem Tesfaye", 1500, "Addis Ababa")
    acc2 = registry.create_account("Bekele Hailu", 800, "Addis Ababa")
    acc3 = registry.create_account("Chaltu Abebe", 2000, "Addis Ababa/Main")
    acc4 = registry.create_account("Dawit Mengistu", 1200, "Addis Ababa/Main")
    acc5 = registry.create_account("Eden Girma", 3000, "Addis Ababa/Main/Downtown")
    acc6 = registry.create_account("Fikir Tadesse", 500, "Gondar")
    acc7 = registry.create_account("Genet Assefa", 2500, "Gondar/North")
    acc8 = registry.create_account("Henok Desta", 1800, "Bahir Dar")
    
    # Display branch tree
    print("\n2. Branch Hierarchy Display:")
    print("-" * 40)
    registry.display_branch_tree()
    
    # Show recursive balance total
    print("\n3. Recursive Branch Balance Totals:")
    print("-" * 40)
    
    total = registry.root_branch.get_total_balance()
    print(f"Total bank balance: {total:.2f} ETB")
    
    branch = registry._find_branch("Addis Ababa")
    if branch:
        print(f"Addis Ababa total: {branch.get_total_balance():.2f} ETB")
    
    branch = registry._find_branch("Addis Ababa/Main")
    if branch:
        print(f"Main branch total: {branch.get_total_balance():.2f} ETB")
    
    branch = registry._find_branch("Gondar")
    if branch:
        print(f"Gondar total: {branch.get_total_balance():.2f} ETB")
    
    # Perform transfers (build graph)
    print("\n4. Performing Transfers (Building Graph):")
    print("-" * 40)
    
    registry.transfer_money("ACC1001", "ACC1003", 200)
    registry.transfer_money("ACC1003", "ACC1005", 150)
    registry.transfer_money("ACC1002", "ACC1004", 100)
    registry.transfer_money("ACC1005", "ACC1008", 300)
    registry.transfer_money("ACC1006", "ACC1007", 250)
    registry.transfer_money("ACC1004", "ACC1006", 180)
    
    # Display transfer graph
    print("\n5. Transfer Graph:")
    print("-" * 40)
    registry.transfer_graph.display_graph()
    
    # Graph traversal - BFS
    print("\n6. Graph BFS Traversal:")
    print("-" * 40)
    start_acc = registry.get_account("ACC1001")
    reachable = registry.transfer_graph.bfs(start_acc)
    print(f"\nReachable accounts from {start_acc.account_number}:")
    for acc_num in sorted(reachable):
        acc = registry.get_account(acc_num)
        if acc:
            print(f"  {acc}")
    
    # Graph traversal - DFS
    print("\n7. Graph DFS Traversal:")
    print("-" * 40)
    start_acc = registry.get_account("ACC1001")
    reachable_dfs = registry.transfer_graph.dfs(start_acc)
    print(f"\nReachable accounts from {start_acc.account_number}:")
    for acc_num in sorted(reachable_dfs):
        acc = registry.get_account(acc_num)
        if acc:
            print(f"  {acc}")
    
    # Find path between accounts
    print("\n8. Find Path Between Accounts:")
    print("-" * 40)
    
    path = registry.transfer_graph.find_path("ACC1001", "ACC1008")
    if path:
        print(f"Path from ACC1001 to ACC1008: {' -> '.join(path)}")
    else:
        print("No path found")
    
    path = registry.transfer_graph.find_path("ACC1001", "ACC1006")
    if path:
        print(f"Path from ACC1001 to ACC1006: {' -> '.join(path)}")
    else:
        print("No path found")
    
    # Reachable accounts
    print("\n9. Reachable Accounts from ACC1001:")
    print("-" * 40)
    reachable = registry.transfer_graph.get_reachable_accounts("ACC1001")
    for acc_num in sorted(reachable):
        acc = registry.get_account(acc_num)
        if acc:
            print(f"  {acc}")
    
    # Display all accounts
    print("\n10. All Accounts:")
    print("-" * 40)
    registry.display_all()
    
    # Save and load
    print("\n11. Save and Load:")
    print("-" * 40)
    registry.save_to_file("accounts.json")
    
    new_registry = AccountRegistry()
    new_registry.load_from_file("accounts.json")
    new_registry.display_branch_tree()
    
    print("\n" + "=" * 70)
    print("✅ Account Registry with Tree & Graph Complete!")
    print("New Features Added:")
    print("  ✓ Branch Tree (hierarchical structure)")
    print("  ✓ Recursive branch balance total")
    print("  ✓ Transfer Graph (network of transactions)")
    print("  ✓ BFS graph traversal (O(V + E))")
    print("  ✓ DFS graph traversal (O(V + E))")
    print("  ✓ Path finding between accounts")
    print("=" * 70)

if __name__ == "__main__":
    demo()