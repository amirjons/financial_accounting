from domain import OperationType

def _show_categories_menu(self):
    """
    Меню управления категориями операций.
    Предоставляет интерфейс для создания и просмотра категорий
    доходов и расходов.
    """
    while True:
        print("\n--- УПРАВЛЕНИЕ КАТЕГОРИЯМИ ---")
        print("1. Просмотр всех категорий")
        print("2. Создать категорию")
        print("0. Назад")
        choice = input("Выберите пункт меню: ").strip()
        if choice == "1":
            self._list_categories()
        elif choice == "2":
            self._create_category()
        elif choice == "0":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def _list_categories(self):
    """
    Отображение списка всех категорий системы.
    Показывает ID, название и тип (доход/расход) каждой категории.
    """
    categories = self.category_facade.get_all_categories()
    if not categories:
        print("Категории не найдены.")
        return
    print("\n--- СПИСОК КАТЕГОРИЙ ---")
    for category in categories:
        type_str = "Доход" if category.type == OperationType.INCOME else "Расход"
        print(f"ID: {category.id}, Название: {category.name}, Тип: {type_str}")

def _create_category(self):
    """
    Создание новой категории операций.
    Запрашивает у пользователя название и тип категории (доход/расход).
    """
    name = input("Введите название категории: ").strip()
    print("Тип категории:")
    print("1. Доход")
    print("2. Расход")
    type_choice = input("Выберите тип: ").strip()
    if type_choice == "1":
        category_type = OperationType.INCOME
    elif type_choice == "2":
        category_type = OperationType.EXPENSE
    else:
        print("Неверный выбор типа.")
        return
    try:
        category = self.category_facade.create_category(name, category_type)
        type_str = "Доход" if category_type == OperationType.INCOME else "Расход"
        print(f"Категория создана: {category.name} (Тип: {type_str}, ID: {category.id})")
    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")