"""
Паттерн Фасад для упрощения работы с подсистемами учета финансов.

"""

from decimal import Decimal
from datetime import date
from typing import List, Optional
from repositories.interfaces import IBankAccountRepository, ICategoryRepository, IOperationRepository
from patterns.factory import DomainFactory
from domain import BankAccount, Category, Operation, OperationType


class BankAccountFacade:
    """
    Фасад для работы с банковскими счетами.

    Предоставляет упрощенный интерфейс для операций со счетами:
    создание, получение, обновление, удаление и пересчет балансов.
    Инкапсулирует сложность взаимодействия с репозиториями и фабриками.
    """

    def __init__(self, account_repo: IBankAccountRepository, operation_repo: IOperationRepository):
        """
        Инициализация фасада счетов.

        """
        self._account_repo = account_repo
        self._operation_repo = operation_repo
        self._factory = DomainFactory()  # Фабрика для создания объектов

    def create_account(self, name: str, initial_balance: Decimal = Decimal('0')) -> BankAccount:
        """
        Создание нового банковского счета.

        """
        # Генерация уникального ID для нового счета
        account_id = self._account_repo.get_next_id()

        # Использование фабрики для создания объекта с валидацией
        account = self._factory.create_bank_account(account_id, name, initial_balance)

        # Сохранение счета в репозитории
        self._account_repo.add(account)

        # Создание начальной операции для отражения начального баланса
        # Это обеспечивает полную аудируемость всех изменений баланса
        if initial_balance > Decimal('0'):
            from datetime import date
            operation_id = self._operation_repo.get_next_id()
            initial_operation = Operation(
                operation_id,
                OperationType.INCOME,
                account_id,
                initial_balance,
                date.today(),
                "Начальный баланс"
            )
            self._operation_repo.add(initial_operation)

        return account

    def get_account(self, account_id: int) -> Optional[BankAccount]:
        """
        Получение счета по ID.

        """
        return self._account_repo.get_by_id(account_id)

    def update_account(self, account_id: int, name: str) -> BankAccount:
        """
        Обновление информации о счете.

        """
        account = self._account_repo.get_by_id(account_id)
        if not account:
            raise ValueError(f"Счет с ID {account_id} не найден")

        # Создание обновленной версии счета
        updated_account = BankAccount(account.id, name, account.balance)
        self._account_repo.update(updated_account)
        return updated_account

    def delete_account(self, account_id: int) -> None:
        """
        Удаление счета.

        """
        # Проверка наличия операций, связанных со счетом
        # Это предотвращает потерю исторических данных
        account_operations = self._operation_repo.get_by_account_id(account_id)
        if account_operations:
            raise ValueError("Нельзя удалить счет с привязанными операциями")

        self._account_repo.delete(account_id)

    def get_all_accounts(self) -> List[BankAccount]:
        """
        Получение всех счетов системы.

        """
        return self._account_repo.get_all()

    def recalculate_balance(self, account_id: int) -> Decimal:
        """
        Пересчет баланса счета на основе всех связанных операций.

        """
        account = self._account_repo.get_by_id(account_id)
        if not account:
            raise ValueError(f"Счет с ID {account_id} не найден")

        # Получение всех операций по счету
        operations = self._operation_repo.get_by_account_id(account_id)
        new_balance = Decimal('0')

        # Расчет баланса на основе операций
        for operation in operations:
            if operation.type == OperationType.INCOME:
                new_balance += operation.amount
            else:
                new_balance -= operation.amount

        # Обновление баланса счета
        account.balance = new_balance
        self._account_repo.update(account)
        return new_balance


class CategoryFacade:
    """
    Фасад для работы с категориями операций.

    """

    def __init__(self, category_repo: ICategoryRepository):
        """
        Инициализация фасада категорий.

        """
        self._category_repo = category_repo
        self._factory = DomainFactory()

    def create_category(self, name: str, category_type: OperationType) -> Category:
        """
        Создание новой категории.

        """
        category_id = self._category_repo.get_next_id()
        category = self._factory.create_category(category_id, category_type, name)
        self._category_repo.add(category)
        return category

    def get_category(self, category_id: int) -> Optional[Category]:
        """
        Получение категории по ID.

        """
        return self._category_repo.get_by_id(category_id)

    def update_category(self, category_id: int, name: str, category_type: OperationType) -> Category:
        """
        Обновление информации о категории.

        """
        category = self._category_repo.get_by_id(category_id)
        if not category:
            raise ValueError(f"Категория с ID {category_id} не найдена")

        updated_category = Category(category.id, category_type, name)
        self._category_repo.update(updated_category)
        return updated_category

    def delete_category(self, category_id: int) -> None:
        """
        Удаление категории.

        """
        self._category_repo.delete(category_id)

    def get_all_categories(self) -> List[Category]:
        """
        Получение всех категорий системы.

        """
        return self._category_repo.get_all()

    def get_categories_by_type(self, category_type: OperationType) -> List[Category]:
        """
        Получение категорий определенного типа.

        """
        return self._category_repo.get_by_type(category_type)


class OperationFacade:
    """
    Фасад для работы с финансовыми операциями.

    """

    def __init__(self, operation_repo: IOperationRepository, account_repo: IBankAccountRepository,
                 category_repo: ICategoryRepository):
        """
        Инициализация фасада операций.

        Args:
            operation_repo (IOperationRepository): Репозиторий операций
            account_repo (IBankAccountRepository): Репозиторий счетов
            category_repo (ICategoryRepository): Репозиторий категорий
        """
        self._operation_repo = operation_repo
        self._account_repo = account_repo
        self._category_repo = category_repo
        self._factory = DomainFactory()

    def create_operation(self, operation_type: OperationType, account_id: int,
                         amount: Decimal, operation_date: date, description: str = None,
                         category_id: int = None) -> Operation:
        """
        Создание новой финансовой операции.

        Args:
            operation_type (OperationType): Тип операции (доход/расход)
            account_id (int): ID счета для операции
            amount (Decimal): Сумма операции
            operation_date (date): Дата операции
            description (str, optional): Описание операции
            category_id (int, optional): ID категории операции

        """
        # Проверка существования счета
        account = self._account_repo.get_by_id(account_id)
        if not account:
            raise ValueError(f"Счет с ID {account_id} не найден")

        # Проверка существования и соответствия категории если указана
        if category_id:
            category = self._category_repo.get_by_id(category_id)
            if not category:
                raise ValueError(f"Категория с ID {category_id} не найдена")
            if category.type != operation_type:
                raise ValueError("Тип категории не соответствует типу операции")

        # Создание операции через фабрику (с валидацией)
        operation_id = self._operation_repo.get_next_id()
        operation = self._factory.create_operation(
            operation_id, operation_type, account_id, amount,
            operation_date, description, category_id
        )

        # Автоматическое обновление баланса счета
        account.update_balance(amount, operation_type)
        self._account_repo.update(account)

        # Сохранение операции в репозитории
        self._operation_repo.add(operation)
        return operation

    def get_operation(self, operation_id: int) -> Optional[Operation]:
        """
        Получение операции по ID.

        """
        return self._operation_repo.get_by_id(operation_id)

    def update_operation(self, operation_id: int, operation_type: OperationType = None,
                         amount: Decimal = None, operation_date: date = None,
                         description: str = None, category_id: int = None) -> Operation:
        """
        Обновление информации об операции.

        Args:
            operation_id (int): ID обновляемой операции
            operation_type (OperationType, optional): Новый тип операции
            amount (Decimal, optional): Новая сумма операции
            operation_date (date, optional): Новая дата операции
            description (str, optional): Новое описание
            category_id (int, optional): Новая категория

        """
        operation = self._operation_repo.get_by_id(operation_id)
        if not operation:
            raise ValueError(f"Операция с ID {operation_id} не найдена")

        # Создание обновленной версии операции
        # Используются переданные значения или текущие если не указаны
        updated_operation = Operation(
            operation.id,
            operation_type if operation_type else operation.type,
            operation.bank_account_id,
            amount if amount else operation.amount,
            operation_date if operation_date else operation.date,
            description if description is not None else operation.description,
            category_id if category_id is not None else operation.category_id
        )

        self._operation_repo.update(updated_operation)
        return updated_operation

    def delete_operation(self, operation_id: int) -> None:
        """
        Удаление операции с коррекцией баланса счета.

        """
        operation = self._operation_repo.get_by_id(operation_id)
        if not operation:
            raise ValueError(f"Операция с ID {operation_id} не найдена")

        # Коррекция баланса счета при удалении операции
        account = self._account_repo.get_by_id(operation.bank_account_id)
        if account:
            if operation.type == OperationType.INCOME:
                account.balance -= operation.amount  # Уменьшаем баланс при удалении дохода
            else:
                account.balance += operation.amount  # Увеличиваем баланс при удалении расхода
            self._account_repo.update(account)

        self._operation_repo.delete(operation_id)

    def get_operations_by_account(self, account_id: int) -> List[Operation]:
        """
        Получение всех операций по конкретному счету.

        """
        return self._operation_repo.get_by_account_id(account_id)

    def get_operations_by_date_range(self, start_date: date, end_date: date) -> List[Operation]:
        """
        Получение операций за указанный период.

        """
        return self._operation_repo.get_by_date_range(start_date, end_date)
