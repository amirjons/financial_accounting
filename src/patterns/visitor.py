"""
Паттерн Посетитель
"""

from abc import ABC, abstractmethod
from typing import List
import json
import csv
import yaml
from decimal import Decimal
from domain import BankAccount, Category, Operation

class IExportVisitor(ABC):
    """Интерфейс посетителя для экспорта"""

    @abstractmethod
    def visit_accounts(self, accounts: List[BankAccount]) -> str:
        pass

    @abstractmethod
    def visit_categories(self, categories: List[Category]) -> str:
        pass

    @abstractmethod
    def visit_operations(self, operations: List[Operation]) -> str:
        pass

class JSONExportVisitor(IExportVisitor):
    """Посетитель для экспорта в JSON"""

    def visit_accounts(self, accounts: List[BankAccount]) -> str:
        data = [
            {
                "id": acc.id,
                "name": acc.name,
                "balance": float(acc.balance)
            }
            for acc in accounts
        ]
        return json.dumps(data, ensure_ascii=False, indent=2)

    def visit_categories(self, categories: List[Category]) -> str:
        data = [
            {
                "id": cat.id,
                "type": cat.type.value,
                "name": cat.name
            }
            for cat in categories
        ]
        return json.dumps(data, ensure_ascii=False, indent=2)

    def visit_operations(self, operations: List[Operation]) -> str:
        data = [
            {
                "id": op.id,
                "type": op.type.value,
                "bank_account_id": op.bank_account_id,
                "amount": float(op.amount),
                "date": op.date.isoformat(),
                "description": op.description,
                "category_id": op.category_id
            }
            for op in operations
        ]
        return json.dumps(data, ensure_ascii=False, indent=2)

class CSVExportVisitor(IExportVisitor):
    """Посетитель для экспорта в CSV"""

    def visit_accounts(self, accounts: List[BankAccount]) -> str:
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["=== ACCOUNTS ==="])
        writer.writerow(["id", "name", "balance"])
        for acc in accounts:
            writer.writerow([acc.id, acc.name, float(acc.balance)])
        return output.getvalue()

    def visit_categories(self, categories: List[Category]) -> str:
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["=== CATEGORIES ==="])
        writer.writerow(["id", "type", "name"])
        for cat in categories:
            writer.writerow([cat.id, cat.type.value, cat.name])
        return output.getvalue()

    def visit_operations(self, operations: List[Operation]) -> str:
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["=== OPERATIONS ==="])
        writer.writerow(["id", "type", "bank_account_id", "amount", "date", "description", "category_id"])
        for op in operations:
            writer.writerow([
                op.id, op.type.value, op.bank_account_id, float(op.amount),
                op.date.isoformat(), op.description or "", op.category_id or ""
            ])
        return output.getvalue()

class YAMLExportVisitor(IExportVisitor):
    """Посетитель для экспорта в YAML"""

    def visit_accounts(self, accounts: List[BankAccount]) -> str:
        data = [
            {
                "id": acc.id,
                "name": acc.name,
                "balance": float(acc.balance)
            }
            for acc in accounts
        ]
        return yaml.dump(data, allow_unicode=True)

    def visit_categories(self, categories: List[Category]) -> str:
        data = [
            {
                "id": cat.id,
                "type": cat.type.value,
                "name": cat.name
            }
            for cat in categories
        ]
        return yaml.dump(data, allow_unicode=True)

    def visit_operations(self, operations: List[Operation]) -> str:
        data = [
            {
                "id": op.id,
                "type": op.type.value,
                "bank_account_id": op.bank_account_id,
                "amount": float(op.amount),
                "date": op.date.isoformat(),
                "description": op.description,
                "category_id": op.category_id
            }
            for op in operations
        ]
        return yaml.dump(data, allow_unicode=True)
