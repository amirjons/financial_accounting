"""
DI-контейнер
"""


class DIContainer:
    """Простой DI-контейнер"""

    def __init__(self):
        self._dependencies = {}

    def register(self, interface, implementation):
        self._dependencies[interface] = implementation

    def resolve(self, interface):
        if interface not in self._dependencies:
            raise ValueError(f"Зависимость {interface} не зарегистрирована")
        return self._dependencies[interface]

    def create_facades(self):
        """Создание фасадов с зависимостями"""
        from repositories.implementations import BankAccountRepository, CategoryRepository, \
            OperationRepository
        from repositories.proxies import BankAccountRepositoryProxy
        from patterns.facade import BankAccountFacade, CategoryFacade, OperationFacade
        from services.analytics import AnalyticsFacade

        # Создаем репозитории
        account_repo = BankAccountRepository()
        category_repo = CategoryRepository()
        operation_repo = OperationRepository()

        # Создаем прокси для репозиториев
        account_repo_proxy = BankAccountRepositoryProxy(account_repo)

        # Создаем фасады
        account_facade = BankAccountFacade(account_repo_proxy, operation_repo)
        category_facade = CategoryFacade(category_repo)
        operation_facade = OperationFacade(operation_repo, account_repo_proxy, category_repo)
        analytics_facade = AnalyticsFacade(operation_repo, category_repo)

        return account_facade, category_facade, operation_facade, analytics_facade
