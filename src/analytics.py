"""
Сервис аналитики
"""

from typing import Dict, Any
from datetime import date
from repositories.interfaces import IOperationRepository, ICategoryRepository
from patterns import IAnalyticsStrategy, PeriodBalanceStrategy, CategoryAnalysisStrategy
from domain.models import Operation, Category
from domain.enums import OperationType


class AnalyticsFacade:
    """Фасад аналитики.

    Обеспечивает единый вход для выполнения различных аналитических задач.
    """

    def __init__(self, operation_repo: IOperationRepository, category_repo: ICategoryRepository):
        """
        :param operation_repo: репозиторий операций
        :param category_repo: репозиторий категорий
        """
        self._operation_repo = operation_repo
        self._category_repo = category_repo

        # Регистрация доступных стратегий
        self._strategies: Dict[str, IAnalyticsStrategy] = {
            'period_balance': PeriodBalanceStrategy(),
            'category_analysis': CategoryAnalysisStrategy()
        }

    def analyze_period_balance(self, start_date: date, end_date: date) -> Dict[str, Any]:
        """Анализ баланса за заданный период.
        """
        operations = self._operation_repo.get_by_date_range(start_date, end_date)
        strategy = self._strategies['period_balance']
        return strategy.analyze(operations, start_date=start_date, end_date=end_date)

    def analyze_categories(self, start_date: date = None, end_date: date = None) -> Dict[str, Any]:
        """Анализ распределения по категориям.

        Если задан диапазон дат — анализ ограничивается им,
        иначе — анализируются все операции в базе.
        """
        if start_date and end_date:
            operations = self._operation_repo.get_by_date_range(start_date, end_date)
        else:
            operations = self._operation_repo.get_all()

        categories = self._category_repo.get_all()
        strategy = self._strategies['category_analysis']
        return strategy.analyze(operations, categories=categories)

    def get_operations_statistics(self) -> Dict[str, Any]:
        """Быстрая сводная статистика по всем операциям.
        """
        operations = self._operation_repo.get_all()

        if not operations:
            #  Если операций нет — возвращаем пустую статистику
            return {"total_operations": 0}

        #  Разделяем операции по типам
        income_operations = [op for op in operations if op.type == OperationType.INCOME]
        expense_operations = [op for op in operations if op.type == OperationType.EXPENSE]

        #  Вычисляем агрегаты
        total_income = sum(op.amount for op in income_operations)
        total_expense = sum(op.amount for op in expense_operations)

        # Формируем отчёт
        return {
            "total_operations": len(operations),
            "income_operations": len(income_operations),
            "expense_operations": len(expense_operations),
            "total_income": float(total_income),
            "total_expense": float(total_expense),
            "average_income": float(total_income / len(income_operations)) if income_operations else 0,
            "average_expense": float(total_expense / len(expense_operations)) if expense_operations else 0
        }
