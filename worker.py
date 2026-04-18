from custom_exceptions import WorkerException
from worker_constructor import WorkerMeta, Command, register
from worker_data import WorkerData
from worker_presence import InfoWorker


class Worker(metaclass=WorkerMeta):
    """Класс, отвечающий за весь функционал приложения."""
    COMMANDS: dict[str, Command]  # Формируется перед созданием самого класса Worker при помощи WorkerMeta

    def __init__(self, storage: WorkerData) -> None:
        """Инициализация работника"""
        self.storage = storage  # Объект класса WorkerData, который непосредственно работает с информацией

    def execute(self, arguments: list[str]) -> None:
        """
        Анализирует введённые аргументы командной строки и вызывает соответствующий метод

        Аргументы:
            arguments -- список строк из sys.argv, аргументы командной строки, введённые через пробел
            (начинаются с названия исполняемого файла).

        Возвращаемое значение:
            None: методы, которые являются реализацией команд приложения, ничего не возвращают.

        Исключения:
            WorkerException:
                1) Не было передано никаких аргументов
                2) Введённая команда не существует
        """
        if len(arguments) < 2:
            raise WorkerException(f"недопустимое использование -> 'python {arguments[0]}'."
                                  f" Правильное использование: 'python {arguments[0]} <command> [arguments]'.")

        command_name = arguments[1]  # Введённая команда
        if self.command_exists(command_name):
            command = self.COMMANDS[command_name]
            command(self, arguments[2:])
        else:
            raise WorkerException(f"команда '{arguments[1]}' не существует.")

    @register("add-category", "python expenses.py add-category <категория>", 1, 1)
    def add_category(self, arguments: list[str]) -> None:
        """
        Реализация команды 'add-category'. Добавляет категорию в файл (CATEGORIES_FILEPATH), указанный в файле настроек.

        Аргументы:
            arguments -- список строк из sys.argv, аргументы командной строки, введённые через пробел
            (начинаются с первого аргумента, переданного после названия исполняемого файла).

        Возвращаемое значение:
            None: метод ничего не возвращает

        Исключения:
            CategoryException:
                1) Категория уже существует
                2) Недопустимое название категории
            CommandException:
                1) Неверное количество аргументов (допустимое количество: 1)
        """
        category_name = arguments[0]
        category = self.storage.create_category(category_name)
        self.storage.save_category(category)

    def command_exists(self, command_name: str) -> bool:
        """Проверяет, существует ли указанная команда"""
        return command_name in self.COMMANDS

    @register("add", "python expenses.py add <стоимость> <категория> <название>", 3, 3)
    def add_expense(self, arguments: list[str]) -> None:
        """
        Реализация команды 'add'. Записывает информацию о расходе (<стоимость>;<категория>;<название>)
        в файл (EXPENSES_FILEPATH), указанный в файле настроек.

        Аргументы:
            arguments -- список строк из sys.argv, аргументы командной строки, введённые через пробел
            (начинаются с первого аргумента, переданного после названия исполняемого файла).

        Возвращаемое значение:
            None: метод ничего не возвращает

        Исключения:
            CategoryException:
                1) Категория не существует
            CommandException:
                1) Неверное количество аргументов (допустимое количество: 3)
            ExpenseException:
                1) Введена некорректная стоимость (не положительное число)
                2) Введено некорректное название (не только буквы, цифры, пробелы и символы нижнего подчёркивания)
        """
        cost, category_name, name = arguments
        category = self.storage.get_category(category_name)
        expense = self.storage.create_expense(cost=cost, category=category, name=name)
        self.storage.save_expense(expense)

    @register("list", "python expenses.py list [категория]", 0, 1)
    def list_expenses(self, arguments: list[str]) -> None:
        """
        Реализация команды 'list'. Выводит информацию о расходах по категории, если категория указана.
        В противном случае выводится информация о всех расходах.

        Аргументы:
            arguments -- список строк из sys.argv, аргументы командной строки, введённые через пробел
            (начинаются с первого аргумента, переданного после названия исполняемого файла).

        Возвращаемое значение:
            None: метод ничего не возвращает

        Исключения:
            CategoryException:
                1) Категория не существует
        """
        expenses = self.storage.get_expenses()
        category = None
        if len(arguments):
            category_name = arguments[0]
            category = self.storage.get_category(category_name)

        info = InfoWorker.get_expenses_info(expenses, category)
        print(info)

    @register("total", "python expenses.py total [категория]", 0, 1)
    def get_total(self, arguments: list[str]) -> None:
        """
        Реализация команды 'total'. Выводит сумму расходов по категории, если категория указана.
        В противном случае выводит сумму всех расходов.

        Аргументы:
            arguments -- список строк из sys.argv, аргументы командной строки, введённые через пробел
            (начинаются с первого аргумента, переданного после названия исполняемого файла).

        Возвращаемое значение:
            None: метод ничего не возвращает

        Исключения:
            CategoryException:
                1) Категория не существует
        """
        expenses = self.storage.get_expenses()
        category = None
        if len(arguments):
            category_name = arguments[0]
            category = self.storage.get_category(category_name)

        info = InfoWorker.get_total_info(expenses, category)
        print(info)
