import math
from custom_exceptions import ExpenseException


class Expense:
    def __init__(self, cost: str, category_name: str, name: str) -> None:
        if not all(char.isalnum() or char.isspace() for char in name):
            raise ExpenseException(f"недопустимое название расхода -> '{name}'."
                                   f" Название расхода должно содержать только буквы, цифры и пробелы.")

        try:
            f_cost = float(cost)
        except ValueError:
            raise ExpenseException(f"недопустимая стоимость расхода -> '{cost}'."
                                   f" Стоимость расхода должна быть положительным числом.")

        if f_cost <= 0 or not math.isfinite(f_cost):
            raise ExpenseException(f"недопустимая стоимость расхода -> '{cost}'."
                                   f" Стоимость расхода должна быть положительным числом.")

        self.name = name
        self.cost = round(f_cost, 2)
        self.category_name = category_name

    def to_csv(self) -> str:
        return f"{self.cost};{self.category_name};{self.name}"

    def __str__(self) -> str:
        return f"{self.name}\n  ├─ Категория: {self.category_name}\n  └─ Стоимость: {self.cost:.2f}"
