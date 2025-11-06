"""
Точка входа в приложение
"""

import sys
import traceback
from app.financial_app import FinancialAccountingApp


def main():
    """Основная функция запуска приложения"""
    try:
        print("\n🚀 Запуск системы учета финансов...")
        app = FinancialAccountingApp()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Программа завершена пользователем.")
    except Exception as e:
        print(f"💥 Критическая ошибка во время выполнения: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()