from abc import ABC, abstractmethod
from datetime import datetime
import json
from typing import List, Optional, Dict, Any
from enum import Enum

# ============================================
# Part 1: SOLID Principles Implementation
# ============================================

# --- Single Responsibility Principle (SRP) ---
# Each class has one clear responsibility

class Transaction:
    """SRP: Responsible for representing a single transaction"""
    def __init__(self, amount: float, description: str, transaction_type: str, balance_after: float):
        self.timestamp = datetime.now()
        self.amount = amount
        self.description = description
        self.transaction_type = transaction_type
        self.balance_after = balance_after
    
    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "amount": self.amount,
            "description": self.description,
            "type": self.transaction_type,
            "balance_after": self.balance_after
        }
    
    def __str__(self) -> str:
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | {self.description} | Balance: {self.balance_after:.2f}"


class TransactionHistory:
    """SRP: Responsible for managing transaction records"""
    def __init__(self):
        self._transactions: List[Transaction] = []
    
    def add(self, amount: float, description: str, transaction_type: str, balance_after: float):
        transaction = Transaction(amount, description, transaction_type, balance_after)
        self._transactions.append(transaction)
    
    def get_all(self) -> List[Transaction]:
        return self._transactions.copy()
    
    def get_recent(self, count: int = 10) -> List[Transaction]:
        return self._transactions[-count:]
    
    def get_by_type(self, transaction_type: str) -> List[Transaction]:
        return [t for t in self._transactions if t.transaction_type == transaction_type]
    
    def clear(self):
        self._transactions.clear()
    
    def to_dict(self) -> List[Dict]:
        return [t.to_dict() for t in self._transactions]
    
    def __len__(self) -> int:
        return len(self._transactions)


class AccountValidator:
    """SRP: Responsible for validating account operations"""
    
    @staticmethod
    def validate_positive_amount(amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return True
    
    @staticmethod
    def validate_sufficient_balance(balance: float, amount: float) -> bool:
        if amount > balance:
            raise ValueError(f"Insufficient funds. Balance: {balance:.2f}")
        return True
    
    @staticmethod
    def validate_minimum_balance(balance: float, minimum: float) -> bool:
        if balance < minimum:
            raise ValueError(f"Balance {balance:.2f} is below minimum {minimum:.2f}")
        return True
    
    @staticmethod
    def validate_account_active(is_active: bool) -> bool:
        if not is_active:
            raise ValueError("Account is closed")
        return True


# --- Open/Closed Principle (OCP) ---
# Classes are open for extension but closed for modification

class InterestCalculator(ABC):
    """OCP: Base class for interest calculation strategies"""
    @abstractmethod
    def calculate(self, balance: float, **kwargs) -> float:
        pass


class SimpleInterestCalculator(InterestCalculator):
    """Extension: Simple interest calculation"""
    def calculate(self, balance: float, rate: float = 0.05, **kwargs) -> float:
        return balance * rate


class CompoundInterestCalculator(InterestCalculator):
    """Extension: Compound interest calculation"""
    def calculate(self, balance: float, rate: float = 0.05, frequency: int = 12, **kwargs) -> float:
        # Monthly compounding
        return balance * (1 + rate/frequency) - balance


class LoyaltyInterestCalculator(InterestCalculator):
    """Extension: Loyalty bonus interest"""
    def calculate(self, balance: float, rate: float = 0.05, **kwargs) -> float:
        bonus = 0.005  # 0.5% bonus for loyal customers
        return balance * (rate + bonus)


class WithdrawalPolicy(ABC):
    """OCP: Base class for withdrawal policies"""
    @abstractmethod
    def can_withdraw(self, account: 'Account', amount: float) -> bool:
        pass
    
    @abstractmethod
    def get_failure_message(self) -> str:
        pass


class MinimumBalancePolicy(WithdrawalPolicy):
    """Extension: Minimum balance check"""
    def __init__(self, minimum_balance: float):
        self.minimum_balance = minimum_balance
        self._failure_message = ""
    
    def can_withdraw(self, account: 'Account', amount: float) -> bool:
        try:
            new_balance = account.balance - amount
            AccountValidator.validate_minimum_balance(new_balance, self.minimum_balance)
            return True
        except ValueError as e:
            self._failure_message = str(e)
            return False
    
    def get_failure_message(self) -> str:
        return self._failure_message


class OverdraftPolicy(WithdrawalPolicy):
    """Extension: Overdraft protection"""
    def __init__(self, overdraft_limit: float):
        self.overdraft_limit = overdraft_limit
        self._failure_message = ""
    
    def can_withdraw(self, account: 'Account', amount: float) -> bool:
        max_withdrawal = account.balance + self.overdraft_limit
        if amount > max_withdrawal:
            self._failure_message = f"Overdraft limit exceeded. Max: {max_withdrawal:.2f}"
            return False
        return True
    
    def get_failure_message(self) -> str:
        return self._failure_message


class WithdrawalLimitPolicy(WithdrawalPolicy):
    """Extension: Monthly withdrawal limit"""
    def __init__(self, max_withdrawals: int):
        self.max_withdrawals = max_withdrawals
        self._failure_message = ""
    
    def can_withdraw(self, account: 'Account', amount: float) -> bool:
        if hasattr(account, 'withdrawal_count') and account.withdrawal_count >= self.max_withdrawals:
            self._failure_message = f"Monthly withdrawal limit ({self.max_withdrawals}) exceeded"
            return False
        return True
    
    def get_failure_message(self) -> str:
        return self._failure_message


# --- Liskov Substitution Principle (LSP) ---
# Subtypes must be substitutable for their base types

class Account(ABC):
    """Base class following LSP - all accounts can be used interchangeably"""
    
    def __init__(self, account_number: str, owner_name: str, initial_balance: float = 0, currency: str = "ETB"):
        self.account_number = account_number
        self.owner_name = owner_name
        self.currency = currency
        self._balance = max(0, initial_balance)
        self.created_at = datetime.now()
        self.is_active = True
        self._history = TransactionHistory()
        self._validator = AccountValidator()
        self._withdrawal_policies: List[WithdrawalPolicy] = []
        
        if initial_balance > 0:
            self._history.add(initial_balance, "Initial deposit", "DEPOSIT", self._balance)
    
    @property
    def balance(self) -> float:
        return self._balance
    
    @balance.setter
    def balance(self, value: float):
        if value < 0:
            raise ValueError("Balance cannot be negative!")
        self._balance = value
    
    @property
    def history(self) -> TransactionHistory:
        return self._history
    
    def add_withdrawal_policy(self, policy: WithdrawalPolicy):
        """Add a withdrawal policy (Open/Closed Principle)"""
        self._withdrawal_policies.append(policy)
    
    def deposit(self, amount: float) -> bool:
        try:
            self._validator.validate_positive_amount(amount)
            self._validator.validate_account_active(self.is_active)
            
            self.balance += amount
            self._history.add(amount, f"Deposit: +{amount:.2f}", "DEPOSIT", self.balance)
            print(f"✅ Deposited {amount:.2f} {self.currency}. New balance: {self.balance:.2f} {self.currency}")
            return True
        except ValueError as e:
            print(f"❌ {e}")
            return False
    
    @abstractmethod
    def withdraw(self, amount: float) -> bool:
        """Abstract method following LSP - all accounts must implement"""
        pass
    
    def _check_withdrawal_policies(self, amount: float) -> bool:
        """Check all withdrawal policies"""
        for policy in self._withdrawal_policies:
            if not policy.can_withdraw(self, amount):
                print(f"❌ {policy.get_failure_message()}")
                return False
        return True
    
    def transfer(self, target_account: 'Account', amount: float) -> bool:
        try:
            self._validator.validate_account_active(self.is_active)
            self._validator.validate_account_active(target_account.is_active)
            self._validator.validate_positive_amount(amount)
            
            if self.withdraw(amount):
                target_account.deposit(amount)
                print(f"🔄 Transferred {amount:.2f} {self.currency} to {target_account.owner_name}")
                return True
            return False
        except ValueError as e:
            print(f"❌ {e}")
            return False
    
    def close_account(self):
        self.is_active = False
        self._history.add(0, "Account closed", "CLOSE", self.balance)
        print(f"🔒 Account {self.account_number} has been closed.")
    
    def display_info(self):
        print("=" * 60)
        print(f"🏦 Account Type: {self.__class__.__name__}")
        print(f"📋 Account Number: {self.account_number}")
        print(f"👤 Owner: {self.owner_name}")
        print(f"💰 Balance: {self.balance:.2f} {self.currency}")
        print(f"📅 Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 Status: {'Active' if self.is_active else 'Closed'}")
        print(f"📝 Transactions: {len(self._history)}")
        self._display_additional_info()
        print("=" * 60)
    
    def _display_additional_info(self):
        """Hook for subclasses"""
        pass
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.account_number}) - {self.owner_name}: {self.balance:.2f} {self.currency}"
    
    def to_dict(self) -> Dict:
        return {
            "type": self.__class__.__name__,
            "account_number": self.account_number,
            "owner_name": self.owner_name,
            "balance": self.balance,
            "currency": self.currency,
            "created_at": self.created_at.isoformat(),
            "is_active": self.is_active,
            "history": self._history.to_dict()
        }


# --- Interface Segregation Principle (ISP) ---
# Use interfaces (abstract classes) with focused responsibilities

class InterestBearing(ABC):
    """Interface for accounts that earn interest"""
    @abstractmethod
    def add_interest(self):
        pass
    
    @abstractmethod
    def get_interest_rate(self) -> float:
        pass


class FeeBearing(ABC):
    """Interface for accounts with fees"""
    @abstractmethod
    def apply_fee(self):
        pass
    
    @abstractmethod
    def get_fee_amount(self) -> float:
        pass


class TimeLimited(ABC):
    """Interface for accounts with time constraints"""
    @abstractmethod
    def check_maturity(self) -> bool:
        pass
    
    @abstractmethod
    def get_maturity_date(self) -> datetime:
        pass


# --- Dependency Inversion Principle (DIP) ---
# Depend on abstractions, not concretions

class InterestService:
    """DIP: Depends on InterestCalculator abstraction"""
    def __init__(self, calculator: InterestCalculator):
        self.calculator = calculator
    
    def calculate_interest(self, balance: float, **kwargs) -> float:
        return self.calculator.calculate(balance, **kwargs)


# ============================================
# Part 2: Design Patterns Implementation
# ============================================

# Pattern 1: Factory Pattern
class AccountFactory:
    """Factory Pattern: Creates account objects without exposing creation logic"""
    
    @staticmethod
    def create_account(account_type: str, **kwargs) -> Account:
        if account_type == "SAVINGS":
            return SavingsAccount(
                kwargs.get("account_number", "SAV" + datetime.now().strftime("%Y%m%d%H%M%S")),
                kwargs.get("owner_name", "Unknown"),
                kwargs.get("initial_balance", 0),
                kwargs.get("minimum_balance", 100),
                kwargs.get("interest_calculator", SimpleInterestCalculator()),
                kwargs.get("currency", "ETB")
            )
        elif account_type == "CHECKING":
            return CheckingAccount(
                kwargs.get("account_number", "CHK" + datetime.now().strftime("%Y%m%d%H%M%S")),
                kwargs.get("owner_name", "Unknown"),
                kwargs.get("initial_balance", 0),
                kwargs.get("overdraft_limit", 200),
                kwargs.get("monthly_fee", 10),
                kwargs.get("currency", "ETB")
            )
        elif account_type == "FIXED_DEPOSIT":
            return FixedDepositAccount(
                kwargs.get("account_number", "FIX" + datetime.now().strftime("%Y%m%d%H%M%S")),
                kwargs.get("owner_name", "Unknown"),
                kwargs.get("initial_balance", 0),
                kwargs.get("interest_calculator", CompoundInterestCalculator()),
                kwargs.get("lock_period_months", 12),
                kwargs.get("currency", "ETB")
            )
        else:
            raise ValueError(f"Unknown account type: {account_type}")


# Pattern 2: Observer Pattern
class Observer(ABC):
    """Observer interface"""
    @abstractmethod
    def update(self, subject, event_type: str, data: Any):
        pass


class Observable:
    """Subject/observable class"""
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event_type: str, data: Any):
        for observer in self._observers:
            observer.update(self, event_type, data)


class EmailNotifier(Observer):
    """Concrete Observer: Sends email notifications"""
    def update(self, subject, event_type: str, data: Any):
        if hasattr(subject, 'owner_name') and hasattr(subject, 'account_number'):
            print(f"📧 Email to {subject.owner_name}: {event_type} - {data}")
            print(f"   Account: {subject.account_number}")


class AuditLogger(Observer):
    """Concrete Observer: Logs all events for auditing"""
    def __init__(self):
        self.logs = []
    
    def update(self, subject, event_type: str, data: Any):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event_type,
            "data": str(data),
            "account": subject.account_number if hasattr(subject, 'account_number') else "Unknown"
        }
        self.logs.append(log_entry)
        print(f"📝 AUDIT: {event_type} - {data}")
    
    def get_logs(self):
        return self.logs


# Pattern 3: Strategy Pattern
class TransactionStrategy(ABC):
    """Strategy Pattern: Encapsulates transaction behavior"""
    @abstractmethod
    def execute(self, account: Account, amount: float) -> bool:
        pass


class StandardDepositStrategy(TransactionStrategy):
    def execute(self, account: Account, amount: float) -> bool:
        return account.deposit(amount)


class StandardWithdrawalStrategy(TransactionStrategy):
    def execute(self, account: Account, amount: float) -> bool:
        return account.withdraw(amount)


class TransferStrategy(TransactionStrategy):
    def __init__(self, target_account: Account):
        self.target_account = target_account
    
    def execute(self, account: Account, amount: float) -> bool:
        return account.transfer(self.target_account, amount)


class TransactionProcessor:
    """Context that uses the strategy"""
    def __init__(self, strategy: TransactionStrategy):
        self.strategy = strategy
    
    def set_strategy(self, strategy: TransactionStrategy):
        self.strategy = strategy
    
    def process(self, account: Account, amount: float) -> bool:
        return self.strategy.execute(account, amount)


# ============================================
# Part 3: Account Implementations
# ============================================

class SavingsAccount(Account, InterestBearing):
    def __init__(self, account_number: str, owner_name: str, initial_balance: float = 0,
                 minimum_balance: float = 100, 
                 interest_calculator: InterestCalculator = SimpleInterestCalculator(),
                 currency: str = "ETB"):
        super().__init__(account_number, owner_name, initial_balance, currency)
        self.minimum_balance = minimum_balance
        self.interest_calculator = interest_calculator
        self.interest_rate = 0.05
        self.withdrawal_count = 0
        self.monthly_withdrawal_limit = 3
        
        # Add policies
        self.add_withdrawal_policy(MinimumBalancePolicy(minimum_balance))
        self.add_withdrawal_policy(WithdrawalLimitPolicy(self.monthly_withdrawal_limit))
    
    def withdraw(self, amount: float) -> bool:
        try:
            self._validator.validate_positive_amount(amount)
            self._validator.validate_account_active(self.is_active)
            
            if not self._check_withdrawal_policies(amount):
                return False
            
            self.balance -= amount
            self.withdrawal_count += 1
            self._history.add(amount, f"Withdrawal: -{amount:.2f}", "WITHDRAWAL", self.balance)
            print(f"✅ Withdrew {amount:.2f} {self.currency}. New balance: {self.balance:.2f} {self.currency}")
            return True
        except ValueError as e:
            print(f"❌ {e}")
            return False
    
    def add_interest(self):
        if not self.is_active:
            print("Account is closed")
            return
        
        interest = self.interest_calculator.calculate(self.balance, rate=self.interest_rate)
        self.balance += interest
        self._history.add(interest, f"Interest: +{interest:.2f}", "INTEREST", self.balance)
        print(f"💰 Added interest: {interest:.2f} {self.currency}. New balance: {self.balance:.2f} {self.currency}")
    
    def get_interest_rate(self) -> float:
        return self.interest_rate
    
    def reset_monthly_withdrawals(self):
        self.withdrawal_count = 0
    
    def _display_additional_info(self):
        print(f"📈 Interest Rate: {self.interest_rate * 100:.1f}%")
        print(f"💰 Minimum Balance: {self.minimum_balance:.2f} {self.currency}")
        print(f"📊 Withdrawals: {self.withdrawal_count}/{self.monthly_withdrawal_limit}")


class CheckingAccount(Account, FeeBearing):
    def __init__(self, account_number: str, owner_name: str, initial_balance: float = 0,
                 overdraft_limit: float = 200, monthly_fee: float = 10,
                 currency: str = "ETB"):
        super().__init__(account_number, owner_name, initial_balance, currency)
        self.overdraft_limit = overdraft_limit
        self.monthly_fee = monthly_fee
        self.transaction_count = 0
        
        # Add policies
        self.add_withdrawal_policy(OverdraftPolicy(overdraft_limit))
    
    def withdraw(self, amount: float) -> bool:
        try:
            self._validator.validate_positive_amount(amount)
            self._validator.validate_account_active(self.is_active)
            
            if not self._check_withdrawal_policies(amount):
                return False
            
            new_balance = self.balance - amount
            self.balance = new_balance
            
            # Charge overdraft fee
            if new_balance < 0:
                fee = 25
                self.balance -= fee
                self._history.add(amount, f"Overdraft: -{amount:.2f} (Fee: {fee:.2f})", "OVERDRAFT", self.balance)
                print(f"⚠️ Overdraft! Withdrew {amount:.2f}. Fee: {fee:.2f}")
            else:
                self._history.add(amount, f"Withdrawal: -{amount:.2f}", "WITHDRAWAL", self.balance)
                print(f"✅ Withdrew {amount:.2f} {self.currency}. New balance: {self.balance:.2f} {self.currency}")
            
            self.transaction_count += 1
            return True
        except ValueError as e:
            print(f"❌ {e}")
            return False
    
    def apply_fee(self):
        if not self.is_active:
            return
        self.balance -= self.monthly_fee
        self._history.add(self.monthly_fee, f"Monthly fee: -{self.monthly_fee:.2f}", "FEE", self.balance)
        self.transaction_count = 0
    
    def get_fee_amount(self) -> float:
        return self.monthly_fee
    
    def _display_additional_info(self):
        print(f"💳 Overdraft Limit: {self.overdraft_limit:.2f} {self.currency}")
        print(f"📊 Monthly Fee: {self.monthly_fee:.2f} {self.currency}")


class FixedDepositAccount(Account, InterestBearing, TimeLimited):
    def __init__(self, account_number: str, owner_name: str, initial_balance: float = 0,
                 interest_calculator: InterestCalculator = CompoundInterestCalculator(),
                 lock_period_months: int = 12, currency: str = "ETB"):
        super().__init__(account_number, owner_name, initial_balance, currency)
        self.interest_calculator = interest_calculator
        self.interest_rate = 0.08
        self.lock_period_months = lock_period_months
        self.start_date = datetime.now()
        self.maturity_date = datetime.now().replace(
            month=datetime.now().month + lock_period_months
        )
        self.is_matured = False
        self.early_withdrawal_penalty = 0.02
    
    def withdraw(self, amount: float) -> bool:
        try:
            self._validator.validate_positive_amount(amount)
            self._validator.validate_account_active(self.is_active)
            
            if amount > self.balance:
                print(f"❌ Insufficient funds! Balance: {self.balance:.2f}")
                return False
            
            is_early = datetime.now() < self.maturity_date
            
            if is_early:
                penalty = amount * self.early_withdrawal_penalty
                total_deduction = amount + penalty
                
                if total_deduction > self.balance:
                    print(f"❌ Insufficient funds after penalty! Need: {total_deduction:.2f}")
                    return False
                
                self.balance -= total_deduction
                self._history.add(amount, f"Early withdrawal: -{amount:.2f} (Penalty: {penalty:.2f})", "EARLY_WITHDRAWAL", self.balance)
                print(f"⚠️ Early withdrawal! Penalty: {penalty:.2f}")
            else:
                self.balance -= amount
                self._history.add(amount, f"Withdrawal: -{amount:.2f}", "WITHDRAWAL", self.balance)
            
            print(f"✅ New balance: {self.balance:.2f} {self.currency}")
            return True
        except ValueError as e:
            print(f"❌ {e}")
            return False
    
    def add_interest(self):
        if not self.is_active:
            return
        interest = self.interest_calculator.calculate(self.balance, rate=self.interest_rate)
        self.balance += interest
        self._history.add(interest, f"Interest: +{interest:.2f}", "INTEREST", self.balance)
        print(f"💰 Added interest: {interest:.2f} {self.currency}")
    
    def get_interest_rate(self) -> float:
        return self.interest_rate
    
    def check_maturity(self) -> bool:
        if datetime.now() >= self.maturity_date and not self.is_matured:
            self.is_matured = True
            bonus = self.balance * 0.01
            self.balance += bonus
            self._history.add(bonus, f"Maturity bonus: +{bonus:.2f}", "BONUS", self.balance)
            print(f"🎉 Fixed deposit matured! Bonus: {bonus:.2f}")
            return True
        return False
    
    def get_maturity_date(self) -> datetime:
        return self.maturity_date
    
    def _display_additional_info(self):
        print(f"📈 Interest Rate: {self.interest_rate * 100:.1f}%")
        print(f"🔒 Lock Period: {self.lock_period_months} months")
        print(f"📅 Maturity: {self.maturity_date.strftime('%Y-%m-%d')}")
        print(f"📊 Status: {'Matured' if self.is_matured else 'Locked'}")
        print(f"⚠️ Early Withdrawal Penalty: {self.early_withdrawal_penalty*100:.1f}%")


# ============================================
# Part 4: Bank System with Patterns
# ============================================

class Bank(Observable):
    """Bank with observer pattern for notifications"""
    
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.accounts: Dict[str, Account] = {}
        self.factory = AccountFactory()
        
        # Attach default observers
        self.attach(EmailNotifier())
        self.attach(AuditLogger())
    
    def add_account(self, account: Account) -> bool:
        if account.account_number in self.accounts:
            print(f"Account {account.account_number} already exists!")
            return False
        
        self.accounts[account.account_number] = account
        self.notify("ACCOUNT_CREATED", f"Account {account.account_number} created for {account.owner_name}")
        print(f"✅ Account {account.account_number} added to {self.name}")
        return True
    
    def create_account(self, account_type: str, **kwargs) -> Optional[Account]:
        try:
            account = self.factory.create_account(account_type, **kwargs)
            self.add_account(account)
            return account
        except ValueError as e:
            print(f"❌ {e}")
            return None
    
    def get_account(self, account_number: str) -> Optional[Account]:
        return self.accounts.get(account_number)
    
    def delete_account(self, account_number: str):
        if account_number in self.accounts:
            self.accounts[account_number].close_account()
            del self.accounts[account_number]
            self.notify("ACCOUNT_DELETED", f"Account {account_number} deleted")
            print(f"🗑️ Account {account_number} deleted")
    
    def display_all_accounts(self):
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
    
    def save_to_file(self, filename: str = "bank_data.json"):
        data = {
            "bank_name": self.name,
            "accounts": [account.to_dict() for account in self.accounts.values()]
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        self.notify("DATA_SAVED", f"Data saved to {filename}")
        print(f"💾 Data saved to {filename}")
    
    def load_from_file(self, filename: str = "bank_data.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            
            self.name = data["bank_name"]
            self.accounts = {}
            
            for acc_data in data["accounts"]:
                account = self._reconstruct_account(acc_data)
                if account:
                    self.accounts[account.account_number] = account
            
            self.notify("DATA_LOADED", f"Data loaded from {filename}")
            print(f"📂 Data loaded from {filename}")
            return True
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return False
        except json.JSONDecodeError:
            print(f"Error reading {filename}.")
            return False
    
    def _reconstruct_account(self, acc_data: Dict) -> Optional[Account]:
        account_type = acc_data["type"]
        
        if account_type == "SavingsAccount":
            account = SavingsAccount(
                acc_data["account_number"],
                acc_data["owner_name"],
                acc_data["balance"],
                acc_data.get("minimum_balance", 100),
                SimpleInterestCalculator(),
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
                CompoundInterestCalculator(),
                acc_data.get("lock_period_months", 12),
                acc_data.get("currency", "ETB")
            )
            account.is_matured = acc_data.get("is_matured", False)
        else:
            return None
        
        account.is_active = acc_data.get("is_active", True)
        return account


# ============================================
# Part 5: Demo
# ============================================

def demo():
    print("🏦 SOLID + Design Patterns Demo")
    print("=" * 70)
    
    # 1. Factory Pattern - Creating accounts
    print("\n📋 Pattern 1: Factory Pattern")
    print("-" * 40)
    bank = Bank("Ethiopian National Bank")
    
    savings = bank.create_account(
        "SAVINGS",
        owner_name="Alem Tesfaye",
        initial_balance=1000,
        minimum_balance=100
    )
    
    checking = bank.create_account(
        "CHECKING",
        owner_name="Bekele Hailu",
        initial_balance=500,
        overdraft_limit=300
    )
    
    fixed = bank.create_account(
        "FIXED_DEPOSIT",
        owner_name="Chaltu Abebe",
        initial_balance=5000,
        lock_period_months=12
    )
    
    # 2. Strategy Pattern - Different transaction strategies
    print("\n📋 Pattern 2: Strategy Pattern")
    print("-" * 40)
    
    processor = TransactionProcessor(StandardDepositStrategy())
    processor.process(savings, 200)
    
    processor.set_strategy(StandardWithdrawalStrategy())
    processor.process(savings, 50)
    
    # Transfer using strategy
    processor.set_strategy(TransferStrategy(checking))
    processor.process(savings, 100)
    
    # 3. Observer Pattern - Notifications
    print("\n📋 Pattern 3: Observer Pattern")
    print("-" * 40)
    
    # The bank already has observers attached
    bank.notify("BULK_OPERATION", "Running end-of-day processes")
    
    # 4. SOLID Demonstrations
    print("\n📋 SOLID Principles in Action")
    print("-" * 40)
    
    # Single Responsibility: Each class has one job
    # Open/Closed: We can add new interest calculators without changing existing code
    print("🔹 Adding new loyalty interest calculator (OCP)")
    loyalty_calc = LoyaltyInterestCalculator()
    savings.interest_calculator = loyalty_calc
    savings.add_interest()
    
    # Liskov Substitution: All accounts can be used interchangeably
    print("\n🔹 Liskov Substitution - Processing all accounts uniformly")
    accounts = [savings, checking, fixed]
    for account in accounts:
        account.withdraw(50)
    
    # Interface Segregation: Focused interfaces
    print("\n🔹 Interface Segregation - Interest bearing accounts")
    interest_accounts = [acc for acc in accounts if isinstance(acc, InterestBearing)]
    for acc in interest_accounts:
        print(f"  {acc.owner_name} earns {acc.get_interest_rate()*100:.1f}% interest")
    
    # Dependency Inversion: Depend on abstractions
    print("\n🔹 Dependency Inversion - Using abstract calculators")
    interest_service = InterestService(CompoundInterestCalculator())
    result = interest_service.calculate_interest(1000, rate=0.08)
    print(f"  Compound interest on 1000: {result:.2f}")
    
    # Display final state
    bank.display_all_accounts()
    
    # 5. Save and Load
    print("\n📋 Save/Load with Patterns")
    print("-" * 40)
    bank.save_to_file("bank_data.json")
    
    new_bank = Bank("New Bank")
    new_bank.load_from_file("bank_data.json")
    new_bank.display_all_accounts()


if __name__ == "__main__":
    demo()