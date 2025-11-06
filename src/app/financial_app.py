import sys
import os
from datetime import date, datetime
from decimal import Decimal

# Добавляем путь для импортов
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..'))

# Импортируем необходимые компоненты системы
from patterns.di_container import DIContainer
from patterns.command import CreateAccountCommand, CreateOperationCommand, RecalculateBalanceCommand
from patterns.decorator import TimedCommandDecorator
from patterns.visitor import JSONExportVisitor, CSVExportVisitor, YAMLExportVisitor
from patterns.template_method import JSONDataImporter, CSVDataImporter, YAMLDataImporter
from domain import OperationType

from .accounts_menu import _show_accounts_menu, _list_accounts, _create_account, _recalculate_balance
from .categories_menu import _show_categories_menu, _list_categories, _create_category
from .operations_menu import _show_operations_menu, _list_operations, _create_operation
from .analytics_menu import _show_analytics_menu, _show_period_balance, _show_category_analysis, _show_general_statistics
from .export_menu import _show_export_menu, _export_data
from .import_menu import _show_import_menu, _import_data, _show_current_data

class FinancialAccountingApp:
    """
    Главный класс консольного приложения для управления финансовым учетом.
    Реализует паттерн Фасад, предоставляя упрощенный интерфейс для работы
    со всей системой через консольное меню.
    """
    def __init__(self):
        """
        Инициализация приложения с использованием DI-контейнера.
        Создает все необходимые зависимости и инициализирует систему
        тестовыми данными для демонстрации.
        """
        # Используем DI-контейнер для управления зависимостями (паттерн DI Container)
        self.container = DIContainer()
        # Создаем фасады для работы с различными модулями системы (паттерн Facade)
        self.account_facade, self.category_facade, self.operation_facade, self.analytics_facade = self.container.create_facades()
        # Инициализация тестовых данных для демонстрации функциональности
        self._initialize_test_data()

    def _initialize_test_data(self):
        """
        Инициализация системы тестовыми данными.
        Создает примеры счетов, категорий и операций для демонстрации
        работы системы без необходимости ручного ввода данных.
        """
        try:
            # Создаем тестовые счета с начальными балансами
            self.account_facade.create_account("Основной счет", Decimal('1000'))
            self.account_facade.create_account("Резервный счет", Decimal('500'))
            # Создаем категории операций (доходы и расходы)
            self.category_facade.create_category("Зарплата", OperationType.INCOME)
            self.category_facade.create_category("Продукты", OperationType.EXPENSE)
            self.category_facade.create_category("Транспорт", OperationType.EXPENSE)
            self.category_facade.create_category("Развлечения", OperationType.EXPENSE)
            # Создаем тестовые финансовые операции
            today = date.today()
            self.operation_facade.create_operation(
                OperationType.INCOME, 1, Decimal('2000'), today, "Зарплата", 1
            )
            self.operation_facade.create_operation(
                OperationType.EXPENSE, 1, Decimal('500'), today, "Покупка продуктов", 2
            )
            self.operation_facade.create_operation(
                OperationType.EXPENSE, 1, Decimal('100'), today, "Такси", 3
            )
        except Exception as e:
            print(f"Ошибка при инициализации тестовых данных: {e}")

    def run(self):
        """
        Главный цикл работы приложения.
        Реализует бесконечный цикл меню, обрабатывающий пользовательский ввод
        и перенаправляющий на соответствующие функциональные модули.
        """
        print("=== СИСТЕМА УЧЕТА ФИНАНСОВ ===")
        while True:
            # Главное меню системы
            print("\n--- ГЛАВНОЕ МЕНЮ ---")
            print("1. Управление счетами")
            print("2. Управление категориями")
            print("3. Управление операциями")
            print("4. Аналитика и отчеты")
            print("5. Экспорт данных")
            print("6. Импорт данных")
            print("0. Выход")
            choice = input("Выберите пункт меню: ").strip()
            if choice == "1":
                self._show_accounts_menu()
            elif choice == "2":
                self._show_categories_menu()
            elif choice == "3":
                self._show_operations_menu()
            elif choice == "4":
                self._show_analytics_menu()
            elif choice == "5":
                self._show_export_menu()
            elif choice == "6":
                self._show_import_menu()
            elif choice == "0":
                print("Выход из программы...")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

    _show_accounts_menu = _show_accounts_menu
    _list_accounts = _list_accounts
    _create_account = _create_account
    _recalculate_balance = _recalculate_balance
    _show_categories_menu = _show_categories_menu
    _list_categories = _list_categories
    _create_category = _create_category
    _show_operations_menu = _show_operations_menu
    _list_operations = _list_operations
    _create_operation = _create_operation
    _show_analytics_menu = _show_analytics_menu
    _show_period_balance = _show_period_balance
    _show_category_analysis = _show_category_analysis
    _show_general_statistics = _show_general_statistics
    _show_export_menu = _show_export_menu
    _export_data = _export_data
    _show_import_menu = _show_import_menu
    _import_data = _import_data
    _show_current_data = _show_current_data
