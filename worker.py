import os
from tools import WorkerException
from costs import Expense


class WorkerData:
    def __init__(self, expenses_filepath, categories_filepath):
        self.expenses_filepath = expenses_filepath
        self.categories_filepath = categories_filepath

        self.__prepare_storage()

    def __prepare_storage(self):
        os.makedirs(os.path.dirname(self.categories_filepath), exist_ok=True)

        open(self.expenses_filepath, "a").close()
        open(self.categories_filepath, "a").close()

    def get_categories(self):
        with open(self.categories_filepath, "r") as file:
            return [line.strip() for line in file.readlines()]

    def save_category(self, category_name):
        with open(self.categories_filepath, "a") as file:
            file.write(category_name + "\n")

    def get_expenses(self):
        with open(self.expenses_filepath, "r") as file:
            return [Expense(*line.strip().split(";")) for line in file.readlines()]

    def save_expense(self, expense: Expense):
        with open(self.expenses_filepath, "a") as file:
            file.write(expense.to_csv() + "\n")


class Worker:
    commands = {
        "add-category": "add_category",
        "add": "add_expense",
        "list": "list_expenses",
        "total": "get_total",
    }

    def __init__(self, storage):
        self.storage = storage

    def __resolve(self, method_name: str) -> str:
        return {m_name: c_name for c_name, m_name in self.commands.items()}[method_name]

    def execute(self, arguments):
        command_name = self.commands.get(arguments[1])
        method = getattr(self, command_name, None)
        if method:
            return method(arguments[2:])
        else:
            raise WorkerException("Нет такой команды")

    def add_category(self, arguments):
        if (amount := len(arguments)) != 1:
            raise WorkerException(f"Команда add-category принимает один аргумент. (Было передано {amount})")

        category_name = arguments[0]
        available_categories = self.storage.get_categories()
        if category_name in available_categories:
            raise WorkerException(f"Такая категория уже существует: '{category_name}'")
        else:
            self.storage.save_category(category_name)

    def add_expense(self, arguments):
        if (amount := len(arguments)) != 3:
            raise WorkerException(f"Команда 'add' принимает на вход 3 аргумента. (Было передано: {amount})")

        cost, category_name, name = arguments

        if category_name not in self.storage.get_categories():
            raise WorkerException(f"Категория '{category_name}' не существует")

        expense = Expense(cost=cost, category_name=category_name, name=name)
        self.storage.save_expense(expense)

    def list_expenses(self, arguments):
        if (amount := len(arguments)) > 1:
            raise WorkerException(f"Команда 'list' принимает на вход 1 опциональный аргумент. (Было передано: {amount})")

        expenses = self.storage.get_expenses()
        category_string = ""
        if amount:
            category_name = arguments[0]
            if category_name not in self.storage.get_categories():
                raise WorkerException(f"Категория '{category_name}' не существует")

            expenses = list(filter(lambda ex: ex.category_name == category_name, expenses))
            category_string = f"(Категория: '{category_name}') "

        print(f"========== РАСХОДЫ {category_string}===========")
        for number, ex in enumerate(expenses, start=1):
            print(f"  [{number}] {ex}")

    def get_total(self, arguments):
        if (amount := len(arguments)) > 1:
            raise WorkerException(f"Команда 'total' принимает на вход 1 опциональный аргумент. (Было передано: {amount})")

        expenses = self.storage.get_expenses()
        category_string = ""
        if amount:
            category_name = arguments[0]
            if category_name not in self.storage.get_categories():
                raise WorkerException(f"Категория '{category_name}' не существует")

            expenses = list(filter(lambda ex: ex.category_name == category_name, expenses))
            category_string = f" (Категория: '{category_name}')"

        total = sum(ex.cost for ex in expenses)
        print(f"Суммарная стоимость расходов{category_string}: {total}")

