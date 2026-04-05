import os
from custom_exceptions import WorkerException
from costs import Expense


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

    def save_category(self, category_name: str) -> None:
        with open(self.categories_filepath, "a", encoding="utf-8") as file:
            file.write(category_name + "\n")

    def get_expenses(self) -> list[Expense]:
        with open(self.expenses_filepath, "r", encoding="utf-8") as file:
            return [Expense(*line.strip().split(";")) for line in file.readlines()]

    def save_expense(self, expense: Expense) -> None:
        with open(self.expenses_filepath, "a", encoding="utf-8") as file:
            file.write(expense.to_csv() + "\n")


class Worker:
    commands = {
        "add-category": "add_category",
        "add": "add_expense",
        "list": "list_expenses",
        "total": "get_total",
    }

    def __init__(self, storage: WorkerData) -> None:
        self.storage = storage

    def execute(self, arguments: list[str]) -> None:
        if len(arguments) < 2:
            raise WorkerException(f"недопустимое использование -> 'python {arguments[0]}'."
                                  f" Правильное использование: 'python {arguments[0]} <command> [arguments]'.")

        command_name = self.commands.get(arguments[1], "")
        method = getattr(self, command_name, None)
        if method:
            method(command_name, arguments[2:])
        else:
            raise WorkerException(f"команда '{arguments[1]}' не существует.")

    def add_category(self, command_name: str, arguments: list[str]) -> None:
        if (amount := len(arguments)) != 1:
            raise WorkerException(f"команда '{command_name}' принимает на вход 1 аргумент."
                                  f" Было передано {amount} {tuple(arguments)}.")
        category_name = arguments[0]
        categories = self.storage.get_categories()
        if category_name in categories:
            raise WorkerException(f"такая категория уже существует -> '{category_name}'.")
        elif not all(char.isalnum() or char.isspace() for char in category_name):
            raise WorkerException(f"недопустимое название категории -> '{category_name}'."
                                  " Название категории может содержать только буквы, цифры и пробелы.")
        else:
            self.storage.save_category(category_name)

    def add_expense(self, command_name: str, arguments: list[str]) -> None:
        if (amount := len(arguments)) != 3:
            raise WorkerException(f"команда '{command_name}' принимает на вход 3 аргумента."
                                  f" Было передано: {amount} {tuple(arguments)}")

        cost, category_name, name = arguments

        if category_name not in self.storage.get_categories():
            raise WorkerException(f"категория не существует -> '{category_name}'")

        expense = Expense(cost=cost, category_name=category_name, name=name)
        self.storage.save_expense(expense)

    def list_expenses(self, command_name: str, arguments: list[str]) -> None:
        if (amount := len(arguments)) > 1:
            raise WorkerException(f"команда '{command_name}' принимает на вход 1 опциональный аргумент."
                                  f" Было передано: {amount} {tuple(arguments)}")

        expenses = self.storage.get_expenses()
        category_string = ""
        if amount:
            category_name = arguments[0]
            if category_name not in self.storage.get_categories():
                raise WorkerException(f"категория не существует -> ")

            expenses = list(filter(lambda ex: ex.category_name == category_name, expenses))
            category_string = f"(Категория: '{category_name}') "

        print(f"========== РАСХОДЫ {category_string}===========")
        for number, ex in enumerate(expenses, start=1):
            print(f"  [{number}] {ex}")

    def get_total(self, command_name: str, arguments: list[str]) -> None:
        if (amount := len(arguments)) > 1:
            raise WorkerException(f"команда '{command_name}' принимает на вход 1 опциональный аргумент."
                                  f" Было передано: {amount} {tuple(arguments)}")

        expenses = self.storage.get_expenses()
        category_string = ""
        if amount:
            category_name = arguments[0]
            if category_name not in self.storage.get_categories():
                raise WorkerException(f"категория не существует -> '{category_name}'")

            expenses = list(filter(lambda ex: ex.category_name == category_name, expenses))
            category_string = f" (Категория: '{category_name}')"

        total = sum(ex.cost for ex in expenses)
        print(f"Суммарная стоимость расходов{category_string}: {total:.2f}")
