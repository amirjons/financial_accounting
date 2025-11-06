"""
Паттерн Декоратор
"""

import time
from typing import Any

from patterns.command import ICommand


class TimedCommandDecorator(ICommand):
    """Декоратор для измерения времени выполнения команды"""

    def __init__(self, command: ICommand):
        self._command = command
        self._execution_time = 0.0

    def execute(self) -> Any:
        start_time = time.time()
        result = self._command.execute()
        end_time = time.time()
        self._execution_time = end_time - start_time
        return result

    def get_description(self) -> str:
        return self._command.get_description()

    def get_execution_time(self) -> float:
        return self._execution_time
