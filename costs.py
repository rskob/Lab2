import math
from tools import ExpenseException


class Expense:
    def __init__(self, cost: str, category_name: str, name: str):
        try:
            f_cost = float(cost)
        except ValueError:
            raise ExpenseException(f"Недопустимая стоимость: '{cost}'. (Стоимость должна быть положительным числом)")

        if f_cost <= 0 or not math.isfinite(f_cost):
            raise ExpenseException(f"Недопустимая стоимость: '{cost}'. (Стоимость должна быть положительным числом)")

        self.name = name
        self.cost = round(f_cost, 2)
        self.category_name = category_name

    def to_csv(self):
        return f"{self.cost};{self.category_name};{self.name}"

    def __str__(self):
        return f"{self.name}\n  ├─ Категория: {self.category_name}\n  └─ Стоимость: {self.cost:.2f}"

