"""
Прокси для репозиториев
"""

from typing import List, Optional, Dict
from repositories.interfaces import IBankAccountRepository
from domain import BankAccount


class BankAccountRepositoryProxy(IBankAccountRepository):
    """Прокси-обёртка для репозитория счетов с in-memory кэшированием.
    """

    def __init__(self, real_repository: IBankAccountRepository):
        """экземпляр реального репозитория
        """
        self._real_repository = real_repository
        self._cache: Dict[int, BankAccount] = {}   # индивидуальный кеш по ID
        self._all_cache: Optional[List[BankAccount]] = None  # общий кеш для get_all()

    def get_by_id(self, id: int) -> Optional[BankAccount]:
        """Возвращает счёт по ID с использованием кеша."""
        if id in self._cache:
            # Если уже есть в кеше — возвращаем без обращения к реальному хранилищу
            return self._cache[id]

        # Иначе берём из репозитория и добавляем в кеш
        account = self._real_repository.get_by_id(id)
        if account:
            self._cache[id] = account
        return account

    def get_all(self) -> List[BankAccount]:
        """Возвращает все счета, кэшируя результат первого вызова."""
        if self._all_cache is not None:
            # Используем кеш, если он уже заполнен
            return self._all_cache

        # Иначе запрашиваем все счета и сохраняем в кеш
        accounts = self._real_repository.get_all()
        self._all_cache = accounts
        # создаём также индексированный кеш для get_by_id()
        self._cache = {acc.id: acc for acc in accounts}
        return accounts

    def add(self, account: BankAccount) -> None:
        """Добавление нового счёта — вызывает инвалидцию кеша."""
        self._real_repository.add(account)
        self._invalidate_cache()

    def update(self, account: BankAccount) -> None:
        """Обновление существующего счёта — также сбрасывает кеш."""
        self._real_repository.update(account)
        self._invalidate_cache()

    def delete(self, id: int) -> None:
        """Удаление счёта — сбрасывает кеш, чтобы избежать рассинхронизации."""
        self._real_repository.delete(id)
        self._invalidate_cache()

    def get_next_id(self) -> int:
        """Возвращает следующий ID для нового счёта (не кешируется)."""
        return self._real_repository.get_next_id()

    def _invalidate_cache(self):
        """Сброс кеша при любых изменениях данных.
        """
        self._cache.clear()
        self._all_cache = None
