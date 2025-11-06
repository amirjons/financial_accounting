"""
Репозитории для работы с данными
"""

from .interfaces import IRepository, IBankAccountRepository, ICategoryRepository, IOperationRepository
from .implementations import BankAccountRepository, CategoryRepository, OperationRepository
from .proxies import BankAccountRepositoryProxy

__all__ = [
    'IRepository', 'IBankAccountRepository', 'ICategoryRepository', 'IOperationRepository',
    'BankAccountRepository', 'CategoryRepository', 'OperationRepository',
    'BankAccountRepositoryProxy'
]
