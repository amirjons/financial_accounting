"""
Паттерн Фабрика
"""

from decimal import Decimal
from datetime import date
from typing import Optional
from domain import BankAccount, Category, Operation, OperationType



class DomainFactory:
    """Фабрика для создания доменных объектов с валидацией"""

    @staticmethod
    def create_bank_account(account_id: int, name: str, initial_balance: Decimal = Decimal('0')) -> BankAccount:
        if initial_balance < Decimal('0'):
            raise ValueError("Баланс не может быть отрицательным")
        if not name.strip():
            raise ValueError("Название счета не может быть пустым")
        return BankAccount(account_id, name, initial_balance)

    @staticmethod
    def create_category(category_id: int, category_type: OperationType, name: str) -> Category:
        if not name.strip():
            raise ValueError("Название категории не может быть пустым")
        return Category(category_id, category_type, name)

    @staticmethod
    def create_operation(operation_id: int, operation_type: OperationType,
                         bank_account_id: int, amount: Decimal, operation_date: date,
                         description: str = None, category_id: int = None) -> Operation:
        if amount <= Decimal('0'):
            raise ValueError("Сумма операции должна быть положительной")
        return Operation(operation_id, operation_type, bank_account_id, amount,
                         operation_date, description, category_id)