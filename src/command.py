"""
Паттерн Команда для инкапсуляции пользовательских сценариев
"""

from abc import ABC, abstractmethod
from typing import Any
from decimal import Decimal
from datetime import date
from domain import BankAccount, Category, Operation, OperationType


class ICommand(ABC):
    """
    Абстрактный интерфейс команды.
    Каждая команда инкапсулирует определенное действие пользователя
    """

    @abstractmethod
    def execute(self) -> Any:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass


class CreateAccountCommand(ICommand):
    """
    Команда создания нового банковского счета.

    Инкапсулирует логику создания счета, включая валидацию данных
    и взаимодействие с соответствующим фасадом.
    """

    def __init__(self, account_facade, name: str, initial_balance: Decimal = Decimal('0')):
        """
        Инициализация команды создания счета.

        Args:
            account_facade: Фасад для работы со счетами
            name (str): Название создаваемого счета
            initial_balance (Decimal): Начальный баланс счета
        """
        self._account_facade = account_facade
        self._name = name
        self._initial_balance = initial_balance

    def execute(self) -> BankAccount:

        return self._account_facade.create_account(self._name, self._initial_balance)

    def get_description(self) -> str:
        return f"Создание счета: {self._name}"


class CreateOperationCommand(ICommand):
    """
    Команда создания финансовой операции.
    """

    def __init__(self, operation_facade, operation_type: OperationType,
                 account_id: int, amount: Decimal, operation_date: date,
                 description: str = None, category_id: int = None):
        """
        Инициализация команды создания операции.

        Args:
            operation_facade: Фасад для работы с операциями
            operation_type (OperationType): Тип операции (доход/расход)
            account_id (int): ID счета для операции
            amount (Decimal): Сумма операции
            operation_date (date): Дата операции
            description (str, optional): Описание операции
            category_id (int, optional): ID категории операции
        """
        self._operation_facade = operation_facade
        self._operation_type = operation_type
        self._account_id = account_id
        self._amount = amount
        self._operation_date = operation_date
        self._description = description
        self._category_id = category_id

    def execute(self) -> Operation:
        """
        Выполнение команды создания операции.
        """
        return self._operation_facade.create_operation(
            self._operation_type, self._account_id, self._amount,
            self._operation_date, self._description, self._category_id
        )

    def get_description(self) -> str:
        return f"Создание операции: {self._operation_type.value} на сумму {self._amount}"


class RecalculateBalanceCommand(ICommand):
    """
    Команда пересчета баланса счета.

    Инкапсулирует логику пересчета баланса счета на основе
    всех связанных с ним операций.
    """

    def __init__(self, account_facade, account_id: int):
        """
        Инициализация команды пересчета баланса.

        Args:
            account_facade: Фасад для работы со счетами
            account_id (int): ID счета для пересчета
        """
        self._account_facade = account_facade
        self._account_id = account_id

    def execute(self) -> Decimal:
        """
        Выполнение команды пересчета баланса.

        """
        return self._account_facade.recalculate_balance(self._account_id)

    def get_description(self) -> str:
        return f"Пересчет баланса для счета ID: {self._account_id}"