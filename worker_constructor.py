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
