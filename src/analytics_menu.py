from datetime import date
from domain import OperationType

def _show_analytics_menu(self):
    """
    Меню аналитики и отчетов.
    Предоставляет доступ к различным аналитическим функциям:
    баланс за период, анализ по категориям, общая статистика.
    """
    while True:
        print("\n--- АНАЛИТИКА И ОТЧЕТЫ ---")
        print("1. Баланс за период")
        print("2. Анализ по категориям")
        print("3. Общая статистика")
        print("0. Назад")
        choice = input("Выберите пункт меню: ").strip()
        if choice == "1":
            self._show_period_balance()
        elif choice == "2":
            self._show_category_analysis()
        elif choice == "3":
            self._show_general_statistics()
        elif choice == "0":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def _show_period_balance(self):
    """
    Анализ баланса за указанный период.
    Рассчитывает и отображает общий доход, расход и баланс
    за выбранный временной период.
    """
    try:
        start_date_str = input("Введите начальную дату (ГГГГ-ММ-ДД): ").strip()
        end_date_str = input("Введите конечную дату (ГГГГ-ММ-ДД): ").strip()
        # Попробуем разные форматы дат
        for date_str in [start_date_str, end_date_str]:
            if '.' in date_str:
                raise ValueError("Используйте формат ГГГГ-ММ-ДД (например: 2025-06-12)")
        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)
        if start_date > end_date:
            raise ValueError("Начальная дата не может быть больше конечной")
        # Использование фасада аналитики для расчета баланса за период
        result = self.analytics_facade.analyze_period_balance(start_date, end_date)
        print(f"\n--- БАЛАНС ЗА ПЕРИОД {start_date} - {end_date} ---")
        print(f"Общий доход: {result['total_income']:.2f}")
        print(f"Общий расход: {result['total_expense']:.2f}")
        print(f"Баланс: {result['balance']:.2f}")
        print(f"Количество операций: {result['period_operations_count']}")
    except ValueError as e:
        print(f"Ошибка ввода даты: {e}")
        print("Правильный формат: ГГГГ-ММ-ДД (например: 2025-06-12)")
    except Exception as e:
        print(f"Ошибка: {e}")

def _show_category_analysis(self):
    """
    Анализ операций по категориям.
    Группирует доходы и расходы по категориям и показывает
    операции без категорий.
    """
    try:
        # Использование фасада аналитики для анализа по категориям
        result = self.analytics_facade.analyze_categories()
        print("\n--- АНАЛИЗ ПО КАТЕГОРИЯМ ---")
        print("Доходы по категориям:")
        for category, amount in result['income_by_category'].items():
            print(f" {category}: {amount}")
        print("\nРасходы по категориям:")
        for category, amount in result['expense_by_category'].items():
            print(f" {category}: {amount}")
        print(f"\nОпераций без категории: {result['uncategorized_operations']}")
    except Exception as e:
        print(f"Ошибка: {e}")

def _show_general_statistics(self):
    """
    Отображение общей статистики операций.
    Показывает общее количество операций, распределение по типам,
    суммы доходов/расходов и средние значения.
    """
    try:
        # Использование фасада аналитики для получения общей статистики
        stats = self.analytics_facade.get_operations_statistics()
        print("\n--- ОБЩАЯ СТАТИСТИКА ---")
        print(f"Всего операций: {stats['total_operations']}")
        print(f"Операций дохода: {stats['income_operations']}")
        print(f"Операций расхода: {stats['expense_operations']}")
        print(f"Общий доход: {stats['total_income']:.2f}")
        print(f"Общий расход: {stats['total_expense']:.2f}")
        print(f"Средний доход: {stats['average_income']:.2f}")
        print(f"Средний расход: {stats['average_expense']:.2f}")
    except Exception as e:
        print(f"Ошибка: {e}")