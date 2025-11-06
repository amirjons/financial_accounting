"""
Доменные классы
"""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional
from .enums import OperationType


@dataclass
class BankAccount:
    """Доменный класс: Банковский счет"""
    id: int
    name: str
    balance: Decimal

    def update_balance(self, amount: Decimal, operation_type: OperationType):
        """Обновление баланса счета"""
        if operation_type == OperationType.INCOME:
            self.balance += amount
        else:
            self.balance -= amount


@dataclass
class Category:
    """Доменный класс: Категория операций"""
    id: int
    type: OperationType
    name: str


@dataclass
class Operation:
    """Доменный класс: Финансовая операция"""
    id: int
    type: OperationType
    bank_account_id: int
    amount: Decimal
    date: date
    description: Optional[str] = None
    category_id: Optional[int] = None