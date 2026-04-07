from custom_exceptions import WorkerException
from costs import Expense
from worker_tools import WorkerData, WorkerMeta, Command


class Worker(metaclass=WorkerMeta):
    commands: dict[str, Command]

    def __init__(self, storage: WorkerData) -> None:
        self.storage = storage

    def execute(self, arguments: list[str]) -> None:
        if len(arguments) < 2:
            raise WorkerException(f"недопустимое использование -> 'python {arguments[0]}'."
                                  f" Правильное использование: 'python {arguments[0]} <command> [arguments]'.")

        command_name = arguments[1]
        command = self.commands.get(command_name, None)
        if command:
            command(self, arguments[2:])
        else:
            raise WorkerException(f"команда '{arguments[1]}' не существует.")

    @WorkerMeta.register("add-category", "python expenses.py add-category <категория>", 1, 1)
    def add_category(self, arguments: list[str]) -> None:
        category_name = arguments[0]
        if self.storage.category_exists(category_name):
            raise WorkerException(f"такая категория уже существует -> '{category_name}'.")
        elif not all(char.isalnum() or char.isspace() or char == "_" for char in category_name):
            raise WorkerException(f"недопустимое название категории -> '{category_name}'."
                                  " Название категории может содержать только буквы, цифры,"
                                  " пробелы и нижние подчёркивания.")
        else:
            self.storage.save_category(category_name)

    @WorkerMeta.register("add", "python expenses.py add <стоимость> <категория> <название>", 3, 3)
    def add_expense(self, arguments: list[str]) -> None:
        cost, category_name, name = arguments

        if not self.storage.category_exists(category_name):
            raise WorkerException(f"категория не существует -> '{category_name}'")

        expense = Expense(cost=cost, category_name=category_name, name=name)
        self.storage.save_expense(expense)

    @WorkerMeta.register("list", "python expenses.py list [категория]", 0, 1)
    def list_expenses(self, arguments: list[str]) -> None:
        expenses = self.storage.get_expenses()
        category_string = ""
        if len(arguments):
            category_name = arguments[0]
            if not self.storage.category_exists(category_name):
                raise WorkerException(f"категория не существует -> '{category_name}'.")

            expenses = list(filter(lambda ex: ex.category_name == category_name, expenses))
            category_string = f"(Категория: '{category_name}') "

        print(f"========== РАСХОДЫ {category_string}===========")
        for number, ex in enumerate(expenses, start=1):
            print(f"  [{number}] {ex}")

    @WorkerMeta.register("total", "python expenses.py total [категория]", 0, 1)
    def get_total(self, arguments: list[str]) -> None:
        expenses = self.storage.get_expenses()
        category_string = ""
        if len(arguments):
            category_name = arguments[0]
            if not self.storage.category_exists(category_name):
                raise WorkerException(f"категория не существует -> '{category_name}'.")

            expenses = list(filter(lambda ex: ex.category_name == category_name, expenses))
            category_string = f" (Категория: '{category_name}')"

        total = sum(ex.cost for ex in expenses)
        print(f"Суммарная стоимость расходов{category_string}: {total:.2f}")
