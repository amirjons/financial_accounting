"""
Реализации репозиториев

"""

from typing import List, Dict, Optional
from datetime import date
from repositories.interfaces import IBankAccountRepository, ICategoryRepository, IOperationRepository
from domain import BankAccount, Category, Operation, OperationType

# Примечание: в этом модуле не используется logging, но в реальном приложении
# рекомендуется логировать важные события (добавление/удаление/ошибки).


class BankAccountRepository(IBankAccountRepository):
    """Реализация репозитория для счетов.

    Хранение: self._accounts — словарь {id: BankAccount}.
    self._next_id — следующий свободный идентификатор (помогает при создании новых записей).

    """

    def __init__(self):
        # id -> BankAccount
        self._accounts: Dict[int, BankAccount] = {}
        # _next_id используется как подсказка для генерации новых id
        self._next_id = 1

    def get_by_id(self, id: int) -> Optional[BankAccount]:
        """Вернуть счёт по его id или None, если не найден.
        """
        return self._accounts.get(id)

    def get_all(self) -> List[BankAccount]:
        """Вернуть список всех счетов.
        """
        return list(self._accounts.values())

    def add(self, account: BankAccount) -> None:
        """Добавить новый счёт в репозиторий.

        """
        if account.id in self._accounts:
            raise ValueError(f"Счет с ID {account.id} уже существует")
        self._accounts[account.id] = account
        # Обновляем подсказку следующего id
        self._next_id = max(self._next_id, account.id + 1)

    def update(self, account: BankAccount) -> None:
        """Обновить существующий счёт
        """
        if account.id not in self._accounts:
            raise ValueError(f"Счет с ID {account.id} не найден")
        self._accounts[account.id] = account

    def delete(self, id: int) -> None:
        """Удалить счёт по id.
        """
        if id not in self._accounts:
            raise ValueError(f"Счет с ID {id} не найден")
        del self._accounts[id]

    def get_next_id(self) -> int:
        """Вернуть подсказку следующего id.
        """
        return self._next_id


class CategoryRepository(ICategoryRepository):
    """Реализация репозитория для категорий.

    Аналогична BankAccountRepository. Добавлен метод get_by_type для удобства.
    """

    def __init__(self):
        self._categories: Dict[int, Category] = {}
        self._next_id = 1

    def get_by_id(self, id: int) -> Optional[Category]:
        """Вернуть категорию по id."""
        return self._categories.get(id)

    def get_all(self) -> List[Category]:
        """Вернуть список всех категорий."""
        return list(self._categories.values())

    def add(self, category: Category) -> None:
        """Добавить новую категорию.
        """
        if category.id in self._categories:
            raise ValueError(f"Категория с ID {category.id} уже существует")
        self._categories[category.id] = category
        self._next_id = max(self._next_id, category.id + 1)

    def update(self, category: Category) -> None:
        """Обновить существующую категорию."""
        if category.id not in self._categories:
            raise ValueError(f"Категория с ID {category.id} не найдена")
        self._categories[category.id] = category

    def delete(self, id: int) -> None:
        """Удалить категорию по id."""
        if id not in self._categories:
            raise ValueError(f"Категория с ID {id} не найдена")
        del self._categories[id]

    def get_by_type(self, category_type: OperationType) -> List[Category]:
        """Вернуть категории по типу (Expense/Income и т.д.)."""
        return [cat for cat in self._categories.values() if cat.type == category_type]

    def get_next_id(self) -> int:
        """Подсказка следующего id для создания новой категории."""
        return self._next_id


class OperationRepository(IOperationRepository):
    """Реализация репозитория для операций.
    """

    def __init__(self):
        self._operations: Dict[int, Operation] = {}
        self._next_id = 1

    def get_by_id(self, id: int) -> Optional[Operation]:
        """Вернуть операцию по id."""
        return self._operations.get(id)

    def get_all(self) -> List[Operation]:
        """Вернуть список всех операций."""
        return list(self._operations.values())

    def add(self, operation: Operation) -> None:
        """Добавить операцию.

        Проверяет уникальность id на уровне репозитория.
        """
        if operation.id in self._operations:
            raise ValueError(f"Операция с ID {operation.id} уже существует")
        self._operations[operation.id] = operation
        self._next_id = max(self._next_id, operation.id + 1)

    def update(self, operation: Operation) -> None:
        """Обновить существующую операцию."""
        if operation.id not in self._operations:
            raise ValueError(f"Операция с ID {operation.id} не найдена")
        self._operations[operation.id] = operation

    def delete(self, id: int) -> None:
        """Удалить операцию по id."""
        if id not in self._operations:
            raise ValueError(f"Операция с ID {id} не найдена")
        del self._operations[id]

    def get_by_account_id(self, account_id: int) -> List[Operation]:
        """Вернуть операции, принадлежащие заданному счёту."""
        return [op for op in self._operations.values() if op.bank_account_id == account_id]

    def get_by_date_range(self, start_date: date, end_date: date) -> List[Operation]:
        """Вернуть операции в заданном диапазоне дат (включительно)."""
        return [op for op in self._operations.values() if start_date <= op.date <= end_date]

    def get_by_category_id(self, category_id: int) -> List[Operation]:
        """Вернуть операции по идентификатору категории."""
        return [op for op in self._operations.values() if op.category_id == category_id]

    def get_next_id(self) -> int:
        """Подсказка следующего id для операции."""
        return self._next_id
