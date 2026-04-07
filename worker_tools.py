import os
from typing import Callable
from costs import Expense
from custom_exceptions import CommandException


class Command:
    def __init__(self, name: str, usage: str, func: Callable[..., None], min_args_number: int, max_args_number: int) -> None:
        self.name = name
        self.usage = usage
        self.func = func
        self.min_args_number = min_args_number
        self.max_args_number = max_args_number

    def __call__(self, instance, arguments: list[str]) -> None:
        if not self.min_args_number <= len(arguments) <= self.max_args_number:
            raise CommandException(f"недопустимое использование команды '{self.name}'. Правильное использование: '{self.usage}'.")

        self.func(instance, arguments)


class WorkerData:
    def __init__(self, expenses_filepath: str, categories_filepath: str) -> None:
        self.expenses_filepath = expenses_filepath
        self.categories_filepath = categories_filepath

        self.__prepare_storage()

    def __prepare_storage(self) -> None:
        os.makedirs(os.path.dirname(self.categories_filepath), exist_ok=True)

        open(self.expenses_filepath, "a", encoding="utf-8").close()
        open(self.categories_filepath, "a", encoding="utf-8").close()

    def get_categories(self) -> list[str]:
        with open(self.categories_filepath, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines()]

    def category_exists(self, category_name: str) -> bool:
        return category_name in self.get_categories()

    def save_category(self, category_name: str) -> None:
        with open(self.categories_filepath, "a", encoding="utf-8") as file:
            file.write(category_name + "\n")

    def get_expenses(self) -> list[Expense]:
        with open(self.expenses_filepath, "r", encoding="utf-8") as file:
            return [Expense(*line.strip().split(";")) for line in file.readlines()]

    def save_expense(self, expense: Expense) -> None:
        with open(self.expenses_filepath, "a", encoding="utf-8") as file:
            file.write(expense.to_csv() + "\n")


class WorkerMeta(type):
    def __new__(mcs, name, base, attrs):
        commands = {}
        for name, value in attrs.items():
            name: str
            value: Callable
            if hasattr(value, "_register_metadata"):
                command_name = value._register_metadata["name"]
                usage = value._register_metadata["usage"]
                min_args_number = value._register_metadata["min_args_number"]
                max_args_number = value._register_metadata["max_args_number"]
                commands[command_name] = Command(command_name, usage, value, min_args_number, max_args_number)

        attrs["commands"] = commands
        return super().__new__(mcs, name, base, attrs)

    @staticmethod
    def register(name: str, usage: str, min_args_number: int, max_args_number: int):
        def decorator(func):
            func._register_metadata = {
                "name": name,
                "usage": usage,
                "min_args_number": min_args_number,
                "max_args_number": max_args_number,
            }
            return func
        return decorator
