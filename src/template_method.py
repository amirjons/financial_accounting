"""
Паттерн: Шаблонный метод (Template Method)

"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
import json
import csv
import yaml
from decimal import Decimal
from datetime import datetime
from domain import BankAccount, Category, Operation, OperationType


class DataImporter(ABC):
    """Абстрактный класс импортера данных.

    """

    def import_data(self, file_path: str) -> Dict[str, Any]:
        """Шаблонный метод импорта.

        """
        # 1) прочитать файл (формат-специфично)
        data = self._read_file(file_path)
        # 2) распарсить строковое содержимое в структурированные данные
        parsed_data = self._parse_data(data)
        # 3) выполнить базовую валидацию/нормализацию
        validated_data = self._validate_data(parsed_data)
        return validated_data

    @abstractmethod
    def _read_file(self, file_path: str) -> str:
        """Прочитать содержимое файла как строку.

        """
        pass

    @abstractmethod
    def _parse_data(self, data: str) -> Dict[str, Any]:
        """Преобразовать строку в структурированные данные.

        """
        pass

    def _validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Базовая валидация/нормализация данных.

        Если каких-то секций нет, создаются пустые списки — это упрощает
        последующую обработку.
        """
        required_sections = ['accounts', 'categories', 'operations']
        for section in required_sections:
            if section not in data:
                # Создаём пустую секцию, если её нет — это защитный приём
                data[section] = []
        return data

    def _convert_to_domain_objects(self, data: Dict[str, Any]) -> Dict[str, List]:
        """Конвертация сырых данных в доменные объекты.
        """
        domain_data = {
            'accounts': [],
            'categories': [],
            'operations': []
        }

        # --- Конвертация счетов ---
        for account_data in data.get('accounts', []):
            try:
                # Проверяем наличие ключей и конвертируем balance в Decimal
                account = BankAccount(
                    id=account_data['id'],
                    name=account_data['name'],
                    balance=Decimal(str(account_data['balance']))
                )
                domain_data['accounts'].append(account)
            except (KeyError, ValueError) as e:
                # В реальном приложении здесь лучше использовать logging.warning
                print(f"Ошибка конвертации счета: {e}")

        # --- Конвертация категорий ---
        for category_data in data.get('categories', []):
            try:
                # OperationType может быть Enum — преобразуем строку/значение
                category_type = OperationType(category_data['type'])
                category = Category(
                    id=category_data['id'],
                    type=category_type,
                    name=category_data['name']
                )
                domain_data['categories'].append(category)
            except (KeyError, ValueError) as e:
                print(f"Ошибка конвертации категории: {e}")

        # --- Конвертация операций ---
        for operation_data in data.get('operations', []):
            try:
                operation_type = OperationType(operation_data['type'])
                # Приведение суммы к Decimal для точности
                operation = Operation(
                    id=operation_data['id'],
                    type=operation_type,
                    bank_account_id=operation_data['bank_account_id'],
                    amount=Decimal(str(operation_data['amount'])),
                    date=datetime.strptime(operation_data['date'], '%Y-%m-%d').date(),
                    description=operation_data.get('description'),
                    category_id=operation_data.get('category_id')
                )
                domain_data['operations'].append(operation)
            except (KeyError, ValueError) as e:
                # Ошибка может означать некорректный формат даты, отсутствующие поля и т.п.
                print(f"Ошибка конвертации операции: {e}")

        return domain_data


class JSONDataImporter(DataImporter):
    """Импортер данных из JSON.

    Реализация предполагает, что JSON содержит корневой объект с
    секциями 'accounts', 'categories', 'operations'.
    """

    def _read_file(self, file_path: str) -> str:
        # Открываем файл в utf-8 — это стандарт для JSON-данных в большинстве случаев
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def _parse_data(self, data: str) -> Dict[str, Any]:
        # json.loads превратит строку в словари/списки Python
        return json.loads(data)

    def import_data(self, file_path: str) -> Dict[str, List]:
        """Переопределяем, чтобы возвращать набор доменных объектов.
        """
        raw_data = super().import_data(file_path)
        return self._convert_to_domain_objects(raw_data)


class CSVDataImporter(DataImporter):
    """Импортер данных из CSV.

    Ожидается, что CSV-файл разбит на секции, отделяемые строками
    '=== ACCOUNTS ===', '=== CATEGORIES ===', '=== OPERATIONS ==='.
    Каждая секция имеет свою строку-заголовок (например, 'id,name,balance').
    """

    def _read_file(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def _parse_data(self, data: str) -> Dict[str, Any]:
        # Для CSV используется простая секционная логика — строки разделяются по '\n'
        accounts = []
        categories = []
        operations = []

        # trim и разделение по строкам
        lines = data.strip().split('\n')
        current_section = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Определение секции по маркеру
            if line.startswith('=== ACCOUNTS ==='):
                current_section = 'accounts'
                continue
            elif line.startswith('=== CATEGORIES ==='):
                current_section = 'categories'
                continue
            elif line.startswith('=== OPERATIONS ==='):
                current_section = 'operations'
                continue
            elif line.startswith('id,'):
                # Пропускаем строку-заголовок
                continue

            # Разбиваем строку по запятым. Внимание: это простой подход и сломается,
            parts = line.split(',')

            if current_section == 'accounts' and not line.startswith('==='):
                if len(parts) >= 3:
                    accounts.append({
                        'id': int(parts[0]),
                        'name': parts[1],
                        'balance': float(parts[2])
                    })

            elif current_section == 'categories' and not line.startswith('==='):
                if len(parts) >= 3:
                    categories.append({
                        'id': int(parts[0]),
                        'type': parts[1],
                        'name': parts[2]
                    })

            elif current_section == 'operations' and not line.startswith('==='):
                # В операции ожидаем по крайней мере 6 полей: id,type,bank_account_id,amount,date,description[,category_id]
                if len(parts) >= 6:
                    operations.append({
                        'id': int(parts[0]),
                        'type': parts[1],
                        'bank_account_id': int(parts[2]),
                        'amount': float(parts[3]),
                        'date': parts[4],
                        'description': parts[5] if len(parts) > 5 else None,
                        'category_id': int(parts[6]) if len(parts) > 6 and parts[6] else None
                    })

        return {
            'accounts': accounts,
            'categories': categories,
            'operations': operations
        }

    def import_data(self, file_path: str) -> Dict[str, List]:
        raw_data = super().import_data(file_path)
        return self._convert_to_domain_objects(raw_data)


class YAMLDataImporter(DataImporter):
    """Импортер данных из YAML.
    """

    def _read_file(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def _parse_data(self, data: str) -> Dict[str, Any]:
        # yaml.safe_load возвращает Python-структуры (dict/list) из YAML
        return yaml.safe_load(data)

    def import_data(self, file_path: str) -> Dict[str, List]:
        raw_data = super().import_data(file_path)
        return self._convert_to_domain_objects(raw_data)
