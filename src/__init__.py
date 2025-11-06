"""
Паттерны проектирования
"""

from .factory import DomainFactory
from .facade import BankAccountFacade, CategoryFacade, OperationFacade
from .command import ICommand, CreateAccountCommand, CreateOperationCommand, RecalculateBalanceCommand
from .decorator import TimedCommandDecorator
from .visitor import IExportVisitor, JSONExportVisitor, CSVExportVisitor, YAMLExportVisitor
from .template_method import DataImporter, JSONDataImporter, CSVDataImporter, YAMLDataImporter
from .strategy import IAnalyticsStrategy, PeriodBalanceStrategy, CategoryAnalysisStrategy
from .di_container import DIContainer

__all__ = [
    'DomainFactory',
    'BankAccountFacade', 'CategoryFacade', 'OperationFacade',
    'ICommand', 'CreateAccountCommand', 'CreateOperationCommand', 'RecalculateBalanceCommand',
    'TimedCommandDecorator',
    'IExportVisitor', 'JSONExportVisitor', 'CSVExportVisitor', 'YAMLExportVisitor',
    'DataImporter', 'JSONDataImporter', 'CSVDataImporter', 'YAMLDataImporter',
    'IAnalyticsStrategy', 'PeriodBalanceStrategy', 'CategoryAnalysisStrategy',
    'DIContainer'
]