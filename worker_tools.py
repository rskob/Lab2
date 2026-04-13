from pathlib import Path
from typing import Callable
from costs import Expense, Category
from custom_exceptions import CommandException, CategoryException


class Command:
    """Класс, отвечающий за предоставление информации о команде и проверку правильности использования команды."""

    def __init__(self, name: str, usage: str, func: Callable[..., None], min_args_number: int,
                 max_args_number: int) -> None:
        """Инициализация команды"""
        self.name = name  # Название команды
        self.usage = usage  # 'Инструкция' по использованию
        self.func = func  # Метод класса Worker
        self.min_args_number = min_args_number  # Минимальное количество аргументов
        self.max_args_number = max_args_number  # Максимальное количество аргументов

    def __call__(self, instance, arguments: list[str]) -> None:
        """
        Вызывает метод класса Worker

        Аргументы:
            instance -- экземпляр класса Worker. Нужен для того, чтобы вызвать метод класса Worker.
            arguments -- список строк из sys.argv, аргументы командной строки, введённые через пробел
            (начинаются с первого аргумента, переданного после названия исполняемого файла).

        Возвращаемое значение:
            None: метод ничего не возвращает

        Исключения:
            CommandException:
                1) Неверное количество аргументов
        """
        if not self.min_args_number <= len(arguments) <= self.max_args_number:
            raise CommandException(
                f"недопустимое использование команды '{self.name}'. Правильное использование: '{self.usage}'.")

        self.func(instance, arguments)


class WorkerData:
    def __init__(self, expenses_filepath: str, categories_filepath: str) -> None:
        self.expenses_filepath = expenses_filepath  # Путь к файлу, в котором хранится информация о расходах
        self.categories_filepath = categories_filepath  # Путь к файлу, в котором хранится информация о категориях

        self.__prepare_storage()  # Подготовка хранилища к работе

    def __prepare_storage(self) -> None:
        """Создаёт файлы, если они не существуют, и директории, в которых они находятся, если они указаны в пути"""
        for filepath in (self.expenses_filepath, self.categories_filepath):
            path = Path(filepath)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch(exist_ok=True)

    def get_categories_names(self) -> list[str]:
        """Возвращает список названий имеющихся категорий"""
        with open(self.categories_filepath, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines()]

    def category_exists(self, category_name: str) -> bool:
        """Проверят, существует ли указанная категория"""
        return category_name.strip() in self.get_categories_names()

    def save_category(self, category: Category) -> None:
        """Записывает название категории в файл"""
        if self.category_exists(category.name):
            raise CategoryException(f"такая категория уже существует -> '{category.name}'.")

        with open(self.categories_filepath, "a", encoding="utf-8") as file:
            file.write(self.serialize(category) + "\n")

    def create_category(self, category_name: str) -> Category:
        """Возвращает экземпляр класса Category"""
        return Category(category_name)

    def get_category(self, category_name: str) -> Category:
        """Возвращает экземпляр класса Category, если категория с таким именем существует"""
        if not self.category_exists(category_name):
            raise CategoryException(f"категория не существует -> '{category_name}'.")

        return Category(category_name)

    def create_expense(self, cost: str, category: Category, name: str) -> Expense:
        """Создаёт экземпляр класса Expense"""
        return Expense(cost, category, name)

    def get_expenses(self) -> list[Expense]:
        """Возвращает информацию о расходах в виде списка, состоящего из экземпляров класса Expense"""
        expenses = []
        with open(self.expenses_filepath, "r", encoding="utf-8") as file:
            for line in file.readlines():
                cost, category_name, name = line.strip().split(";")
                category = Category(category_name)
                expenses.append(Expense(cost=cost, category=category, name=name))
        return expenses

    def save_expense(self, expense: Expense) -> None:
        """Записывает информацию о расходе в файл"""
        with open(self.expenses_filepath, "a", encoding="utf-8") as file:
            file.write(self.serialize(expense) + "\n")

    def serialize(self, obj: Expense | Category) -> str:
        """Возвращает строку данных объекта"""
        if isinstance(obj, Expense):
            return f"{obj.cost};{obj.category};{obj.name}"
        return obj.name


class WorkerMeta(type):
    """
    Мета класс, добавляющий в создаваемый класс (Worker) словарь с информациями о методах,
    которые являются реализацией команд приложения.
    """

    def __new__(mcs, name, bases, attrs):
        commands = {}
        for attr_name, attr_value in attrs.items():
            attr_name: str
            attr_value: Callable

            if hasattr(attr_value, "_register_metadata"):
                command_name = attr_value._register_metadata["name"]
                usage = attr_value._register_metadata["usage"]
                min_args_number = attr_value._register_metadata["min_args_number"]
                max_args_number = attr_value._register_metadata["max_args_number"]
                commands[command_name] = Command(command_name, usage, attr_value, min_args_number, max_args_number)
                del attr_value._register_metadata

        attrs["commands"] = commands
        return super().__new__(mcs, name, bases, attrs)


class BeautyWorker:
    @staticmethod
    def print_expenses(expenses: list[Expense], category: Category | None = None) -> None:
        """Выводит на экран все расходы по категории, если она указана. В противном случае все расходы"""
        if category:
            expenses = filter(lambda exp: exp.category == category, expenses)
            head = f"========== РАСХОДЫ (Категория: '{category}') ==========="
        else:
            head = f"========== РАСХОДЫ ==========="

        print(head)
        for number, ex in enumerate(expenses, start=1):
            print(f"  [{number}] {ex}")

    @staticmethod
    def print_total(expenses: list[Expense], category: Category | None = None) -> None:
        """
        Выводит на экран сумму расходов по категории, если она указана.
        В противном случае суммарную стоимость всех расходов.
        """
        if category:
            category_string = f" (Категория: '{category}')"
            expenses = filter(lambda exp: exp.category == category, expenses)
        else:
            category_string = ""

        total = sum(map(lambda exp: exp.cost, expenses))
        print(f"Суммарная стоимость расходов{category_string}: {total:.2f}")


def register(name: str, usage: str, min_args_number: int, max_args_number: int):
    """
    Используется в качестве декоратора с параметрами для обёртывания методов класса Worker,
    являющихся реализацией команд приложения. Записывает данные команды в атрибут
    _register_metadata передаваемой функции.
    """

    def decorator(func):
        func._register_metadata = {
            "name": name,
            "usage": usage,
            "min_args_number": min_args_number,
            "max_args_number": max_args_number,
        }
        return func

    return decorator
