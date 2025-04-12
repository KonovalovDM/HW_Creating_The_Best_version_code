import math
import random
from dataclasses import dataclass


@dataclass
class CustomerInfo:
    """Отдельный класс для данных клиента (повышение абстракции)."""
    name: str
    address: str


class Account:
    def __init__(self, account_number: int, customer_info: CustomerInfo, balance: float):
        self.account_number = account_number
        self.customer_info = customer_info  # Делегирование хранения данных
        self._balance = balance  # Инкапсуляция баланса

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount

    @property
    def balance(self) -> float:
        return self._balance


class Bank:
    def __init__(self):
        self._accounts: dict[int, Account] = {}  # Инкапсуляция хранилища

    def create_account(self, customer_info: CustomerInfo, initial_balance: float) -> Account:
        account_number = self._generate_account_number()
        account = Account(account_number, customer_info, initial_balance)
        self._accounts[account_number] = account
        return account

    def get_account(self, account_number: int) -> Account:
        if account_number not in self._accounts:
            raise ValueError("Account not found")
        return self._accounts[account_number]

    def _generate_account_number(self) -> int:
        return math.floor(random.random() * 1000000)


class Customer:
    def __init__(self, info: CustomerInfo, bank: Bank):
        self.info = info
        self.bank = bank

    def open_account(self, initial_balance: float) -> Account:
        return self.bank.create_account(self.info, initial_balance)


def banking_scenario():
    bank = Bank()
    alice_info = CustomerInfo("Alice", "Moscow, Stremyannyi per, 1")
    bob_info = CustomerInfo("Bob", "Vorkuta, ul. Lenina, 5")

    customer1 = Customer(alice_info, bank)
    customer2 = Customer(bob_info, bank)

    alice_account = customer1.open_account(initial_balance=500.0)
    alice_account.deposit(100.0)
    print(f"Alice's balance: {alice_account.balance}")

    bob_account = customer2.open_account(initial_balance=1000.0)
    bob_account.deposit(500.0)
    print(f"Bob's balance: {bob_account.balance}")

    alice_account.withdraw(300.0)
    print(f"Alice's balance: {alice_account.balance}")

    try:
        alice_account.withdraw(500.0)
    except ValueError as e:
        print(e)

    retrieved_account = bank.get_account(alice_account.account_number)
    print(
        f"Account {retrieved_account.account_number} by {retrieved_account.customer_info.name}, "
        f"balance {retrieved_account.balance}"
    )


if __name__ == "__main__":
    banking_scenario()