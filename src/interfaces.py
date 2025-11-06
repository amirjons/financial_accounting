"""
Интерфейсы репозиториев
"""

from abc import ABC, abstractmethod
from typing import List, Any
from datetime import date
from domain.enums import OperationType
from domain import BankAccount, Category, Operation


class IRepository(ABC):
    """Базовый интерфейс репозитория.
    """

    @abstractmethod
    def get_by_id(self, id: int) -> Any:
        """Получить объект по его уникальному идентификатору."""
        pass

    @abstractmethod
    def get_all(self) -> List[Any]:
        """Получить все объекты данного типа."""
        pass

    @abstractmethod
    def add(self, entity: Any) -> None:
        """Добавить новый объект в хранилище."""
        pass

    @abstractmethod
    def update(self, entity: Any) -> None:
        """Обновить существующий объект."""
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        """Удалить объект по его ID."""
        pass


class IBankAccountRepository(IRepository):
    """Интерфейс репозитория банковских счетов.
    """

    @abstractmethod
    def get_next_id(self) -> int:
        """Возвращает следующий доступный ID для нового счета."""
        pass


class ICategoryRepository(IRepository):
    """Интерфейс репозитория категорий операций.

    Категории делятся по типу операции (доход/расход).
    """

    @abstractmethod
    def get_by_type(self, category_type: OperationType) -> List[Category]:
        """Получить список категорий по типу операции."""
        pass

    @abstractmethod
    def get_next_id(self) -> int:
        """Вернуть следующий доступный ID для категории."""
        pass


class IOperationRepository(IRepository):
    """Интерфейс репозитория финансовых операций."""

    @abstractmethod
    def get_by_account_id(self, account_id: int) -> List[Operation]:
        """Получить все операции по ID банковского счета."""
        pass

    @abstractmethod
    def get_by_date_range(self, start_date: date, end_date: date) -> List[Operation]:
        """Получить операции за указанный период (включительно)."""
        pass

    @abstractmethod
    def get_by_category_id(self, category_id: int) -> List[Operation]:
        """Получить все операции, относящиеся к конкретной категории."""
        pass

    @abstractmethod
    def get_next_id(self) -> int:
        """Возвращает следующий ID для новой операции."""
        pass
