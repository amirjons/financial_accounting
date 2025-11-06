"""
Паттерн Стратегия
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from domain import BankAccount, Category, Operation, OperationType

class IAnalyticsStrategy(ABC):
    """Стратегия аналитики"""

    @abstractmethod
    def analyze(self, operations: List[Operation], **kwargs) -> Dict[str, Any]:
        pass


class PeriodBalanceStrategy(IAnalyticsStrategy):
    """Стратегия анализа баланса за период"""

    def analyze(self, operations: List[Operation], **kwargs) -> Dict[str, Any]:
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')

        period_operations = [
            op for op in operations
            if start_date <= op.date <= end_date
        ]

        total_income = sum(op.amount for op in period_operations if op.type == OperationType.INCOME)
        total_expense = sum(op.amount for op in period_operations if op.type == OperationType.EXPENSE)
        balance = total_income - total_expense

        return {
            "total_income": float(total_income),
            "total_expense": float(total_expense),
            "balance": float(balance),
            "period_operations_count": len(period_operations)
        }


class CategoryAnalysisStrategy(IAnalyticsStrategy):
    """Стратегия анализа по категориям"""

    def analyze(self, operations: List[Operation], **kwargs) -> Dict[str, Any]:
        categories = kwargs.get('categories', [])

        result = {
            "income_by_category": {},
            "expense_by_category": {},
            "uncategorized_operations": 0
        }

        for operation in operations:
            if operation.category_id:
                category = next((cat for cat in categories if cat.id == operation.category_id), None)
                if category:
                    if operation.type == OperationType.INCOME:
                        category_name = category.name
                        result["income_by_category"][category_name] = result["income_by_category"].get(category_name,
                                                                                                       0) + float(
                            operation.amount)
                    else:
                        category_name = category.name
                        result["expense_by_category"][category_name] = result["expense_by_category"].get(category_name,
                                                                                                         0) + float(
                            operation.amount)
            else:
                result["uncategorized_operations"] += 1

        return result
