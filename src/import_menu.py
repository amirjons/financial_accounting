
import os
import traceback
from patterns.template_method import JSONDataImporter, CSVDataImporter, YAMLDataImporter
from domain import OperationType

def _show_import_menu(self):
    """
    Меню импорта данных из внешних файлов.
    Реализует функциональность импорта данных из различных форматов
    с использованием паттерна Шаблонный метод.
    """
    while True:
        print("\n--- ИМПОРТ ДАННЫХ ---")
        print("1. Импорт из JSON")
        print("2. Импорт из CSV")
        print("3. Импорт из YAML")
        print("4. Показать текущие данные")
        print("0. Назад")
        choice = input("Выберите пункт меню: ").strip()
        if choice == "1":
            self._import_data("json")
        elif choice == "2":
            self._import_data("csv")
        elif choice == "3":
            self._import_data("yaml")
        elif choice == "4":
            self._show_current_data()
        elif choice == "0":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def _import_data(self, format_type: str):
    """
    Основной метод импорта данных из файла.
    Реализует полный цикл импорта: чтение файла, парсинг данных,
    валидацию и сохранение в систему с обработкой ошибок.
    Args:
        format_type (str): Тип формата файла ('json', 'csv', 'yaml')
    """
    try:
        # Запрос пути к файлу
        file_path = input(f"Введите путь к файлу {format_type.upper()}: ").strip()
        # Проверка существования файла
        if not os.path.exists(file_path):
            print(f"❌ Файл {file_path} не найден.")
            return
        # Выбор соответствующего импортера на основе формата (паттерн Шаблонный метод)
        if format_type == "json":
            importer = JSONDataImporter()
        elif format_type == "csv":
            importer = CSVDataImporter()
        elif format_type == "yaml":
            importer = YAMLDataImporter()
        else:
            print("❌ Неверный формат файла.")
            return
        print("🔄 Импорт данных...")
        # Использование импортера для чтения и преобразования данных
        imported_data = importer.import_data(file_path)
        # Статистика найденных данных в файле
        accounts_count = len(imported_data.get('accounts', []))
        categories_count = len(imported_data.get('categories', []))
        operations_count = len(imported_data.get('operations', []))
        print(f"📊 Найдено в файле: {accounts_count} счетов, {categories_count} категорий, {operations_count} операций")
        # Импорт счетов с проверкой на дубликаты
        imported_accounts = 0
        for account in imported_data.get('accounts', []):
            try:
                # Проверяем, существует ли счет с таким ID (защита от дубликатов)
                existing_account = self.account_facade.get_account(account.id)
                if existing_account:
                    print(f"⚠️ Счет с ID {account.id} уже существует, пропускаем")
                    continue
                # Сохраняем счет в репозиторий
                self.account_facade._account_repo.add(account)
                imported_accounts += 1
            except Exception as e:
                print(f"❌ Ошибка импорта счета {account.id}: {e}")
        # Импорт категорий с проверкой на дубликаты
        imported_categories = 0
        for category in imported_data.get('categories', []):
            try:
                # Проверяем существование категории с таким ID
                existing_category = self.category_facade.get_category(category.id)
                if existing_category:
                    print(f"⚠️ Категория с ID {category.id} уже существует, пропускаем")
                    continue
                # Сохраняем категорию в репозиторий
                self.category_facade._category_repo.add(category)
                imported_categories += 1
            except Exception as e:
                print(f"❌ Ошибка импорта категории {category.id}: {e}")
        # Импорт операций с проверкой связей и обновлением балансов
        imported_operations = 0
        for operation in imported_data.get('operations', []):
            try:
                # Проверяем существование операции с таким ID
                existing_operation = self.operation_facade.get_operation(operation.id)
                if existing_operation:
                    print(f"⚠️ Операция с ID {operation.id} уже существует, пропускаем")
                    continue
                # Проверяем существование связанного счета
                account = self.account_facade.get_account(operation.bank_account_id)
                if not account:
                    print(f"⚠️ Счет с ID {operation.bank_account_id} не найден, пропускаем операцию {operation.id}")
                    continue
                # Проверяем существование категории если она указана
                if operation.category_id:
                    category = self.category_facade.get_category(operation.category_id)
                    if not category:
                        print(f"⚠️ Категория с ID {operation.category_id} не найдена, пропускаем операцию {operation.id}")
                        continue
                # Сохраняем операцию в репозиторий
                self.operation_facade._operation_repo.add(operation)
                # Обновляем баланс счета на основе импортированной операции
                account.update_balance(operation.amount, operation.type)
                self.account_facade._account_repo.update(account)
                imported_operations += 1
            except Exception as e:
                print(f"❌ Ошибка импорта операции {operation.id}: {e}")
        # Вывод итоговой статистики
        print(f"\n✅ Импорт завершен:")
        print(f" 📈 Счетов импортировано: {imported_accounts}/{accounts_count}")
        print(f" 📊 Категорий импортировано: {imported_categories}/{categories_count}")
        print(f" 💰 Операций импортировано: {imported_operations}/{operations_count}")
    except Exception as e:
        print(f"❌ Ошибка при импорте данных: {e}")
        traceback.print_exc()

def _show_current_data(self):
    """
    Отображение текущего состояния данных системы.
    Показывает все счета, категории и операции, находящиеся в системе
    в данный момент. Полезно для проверки состояния до и после импорта.
    """
    print("\n--- ТЕКУЩИЕ ДАННЫЕ СИСТЕМЫ ---")
    # Отображение счетов
    accounts = self.account_facade.get_all_accounts()
    print(f"\n📈 Счетов: {len(accounts)}")
    for acc in accounts:
        print(f" ID: {acc.id}, Название: {acc.name}, Баланс: {acc.balance}")
    # Отображение категорий
    categories = self.category_facade.get_all_categories()
    print(f"\n📊 Категорий: {len(categories)}")
    for cat in categories:
        type_str = "Доход" if cat.type == OperationType.INCOME else "Расход"
        print(f" ID: {cat.id}, Название: {cat.name}, Тип: {type_str}")
    # Отображение операций
    operations = self.operation_facade._operation_repo.get_all()
    print(f"\n💰 Операций: {len(operations)}")
    for op in operations:
        type_str = "Доход" if op.type == OperationType.INCOME else "Расход"
        print(f" ID: {op.id}, Тип: {type_str}, Сумма: {op.amount}, Дата: {op.date}")