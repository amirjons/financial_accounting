from datetime import datetime
from patterns.visitor import JSONExportVisitor, CSVExportVisitor, YAMLExportVisitor

def _show_export_menu(self):
    """
    Меню экспорта данных в файлы.
    Предоставляет возможность экспорта данных в различные форматы:
    JSON, CSV, YAML. Использует паттерн Посетитель для реализации
    экспорта в разные форматы.
    """
    while True:
        print("\n--- ЭКСПОРТ ДАННЫХ ---")
        print("1. Экспорт в JSON")
        print("2. Экспорт в CSV")
        print("3. Экспорт в YAML")
        print("0. Назад")
        choice = input("Выберите формат: ").strip()
        if choice in ["1", "2", "3"]:
            self._export_data(choice)
        elif choice == "0":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def _export_data(self, format_choice):
    """
    Экспорт данных в выбранном формате.
    Использует паттерн Посетитель для посещения различных типов данных
    и их экспорта в соответствующий формат.
    Args:
        format_choice (str): Выбранный формат экспорта ('1' - JSON, '2' - CSV, '3' - YAML)
    """
    try:
        # Выбор соответствующего посетителя на основе формата
        if format_choice == "1":
            visitor = JSONExportVisitor()
            extension = "json"
        elif format_choice == "2":
            visitor = CSVExportVisitor()
            extension = "csv"
        elif format_choice == "3":
            visitor = YAMLExportVisitor()
            extension = "yaml"

        # Собираем данные из системы
        accounts = self.account_facade.get_all_accounts()
        categories = self.category_facade.get_all_categories()
        operations = self.operation_facade._operation_repo.get_all()
        # Использование посетителя для экспорта данных (паттерн Посетитель)
        accounts_data = visitor.visit_accounts(accounts)
        categories_data = visitor.visit_categories(categories)
        operations_data = visitor.visit_operations(operations)
        # Сохраняем данные в файлы с временной меткой
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"accounts_{timestamp}.{extension}", 'w', encoding='utf-8') as f:
            f.write(accounts_data)
        with open(f"categories_{timestamp}.{extension}", 'w', encoding='utf-8') as f:
            f.write(categories_data)
        with open(f"operations_{timestamp}.{extension}", 'w', encoding='utf-8') as f:
            f.write(operations_data)
        print(f"Данные успешно экспортированы в файлы с префиксом {timestamp}")
    except Exception as e:
        print(f"Ошибка при экспорте: {e}")
