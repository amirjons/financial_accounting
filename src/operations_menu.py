from datetime import date
from decimal import Decimal
from patterns.command import CreateOperationCommand
from patterns.decorator import TimedCommandDecorator
from domain import OperationType


def _show_operations_menu(self):
    """
    Меню управления финансовыми операциями.

    Предоставляет интерфейс для создания и просмотра операций
    доходов и расходов.
    """
    while True:
        print("\n--- УПРАВЛЕНИЕ ОПЕРАЦИЯМИ ---")
        print("1. Просмотр всех операций")
        print("2. Создать операцию")
        print("3. Создать новый счет")
        print("0. Назад")

        choice = input("Выберите пункт меню: ").strip()

        if choice == "1":
            self._list_operations()
        elif choice == "2":
            self._create_operation()
        elif choice == "3":
            self._create_account()
        elif choice == "0":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def _list_operations(self):
    """
    Отображение списка всех операций системы.
    Показывает ID, тип, сумму и дату каждой операции.
    """
    operations = self.operation_facade._operation_repo.get_all()
    if not operations:
        print("Операции не найдены.")
        return
    print("\n--- СПИСОК ОПЕРАЦИЙ ---")
    for operation in operations:
        type_str = "Доход" if operation.type == OperationType.INCOME else "Расход"
        print(f"ID: {operation.id}, Тип: {type_str}, Сумма: {operation.amount}, Дата: {operation.date}")


def _create_operation(self):
    """
    Создание новой финансовой операции.

    Запрашивает у пользователя данные об операции: тип, счет, сумму,
    описание и категорию. Использует паттерн Команда и Декоратор
    для выполнения операции с измерением времени.
    """
    try:
        # Сначала покажем доступные счета
        print("\n--- ДОСТУПНЫЕ СЧЕТА ---")
        accounts = self.account_facade.get_all_accounts()

        if not accounts:
            print("❌ Нет доступных счетов.")
            create_new = input("Хотите создать новый счет? (y/n): ").strip().lower()
            if create_new == 'y':
                self._create_account()
                # После создания счета покажем обновленный список
                print("\n--- ОБНОВЛЕННЫЙ СПИСОК СЧЕТОВ ---")
                self._list_accounts()
            else:
                return

        self._list_accounts()

        print("\nТип операции:")
        print("1. Доход")
        print("2. Расход")
        type_choice = input("Выберите тип: ").strip()

        if type_choice == "1":
            operation_type = OperationType.INCOME
        elif type_choice == "2":
            operation_type = OperationType.EXPENSE
        else:
            print("❌ Неверный выбор типа.")
            return

        # Запрос ID счета с проверкой существования
        while True:
            try:
                account_id = int(input("Введите ID счета: ").strip())

                # Проверяем существование счета
                account = self.account_facade.get_account(account_id)
                if not account:
                    print(f"❌ Ошибка: Счет с ID {account_id} не найден.")
                    print("Доступные ID счетов:", [acc.id for acc in accounts])
                    retry = input("Повторить ввод? (y/n): ").strip().lower()
                    if retry != 'y':
                        return
                    continue
                break
            except ValueError:
                print("❌ Ошибка: Введите корректный числовой ID счета.")

        # Запрос суммы с валидацией
        while True:
            try:
                amount_str = input("Введите сумму: ").strip()
                amount = Decimal(amount_str)
                if amount <= Decimal('0'):
                    print("❌ Ошибка: Сумма должна быть положительной.")
                    continue
                break
            except Exception:
                print("❌ Ошибка: Введите корректную сумму.")

        description = input("Введите описание (необязательно): ").strip() or None

        # Для простоты используем текущую дату
        operation_date = date.today()

        # Использование паттерна Команда для создания операции
        command = CreateOperationCommand(
            self.operation_facade, operation_type, account_id, amount,
            operation_date, description
        )

        # Использование паттерна Декоратор для измерения времени
        timed_command = TimedCommandDecorator(command)

        operation = timed_command.execute()

        type_str = "Доход" if operation_type == OperationType.INCOME else "Расход"
        print(f"✅ Операция создана: {type_str} на сумму {operation.amount}")
        print(f"⏱️ Время выполнения: {timed_command.get_execution_time():.3f} сек")

        # Покажем обновленный баланс счета
        updated_account = self.account_facade.get_account(account_id)
        print(f"💰 Обновленный баланс счета: {updated_account.balance}")

    except ValueError as e:
        print(f"❌ Ошибка ввода данных: {e}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")