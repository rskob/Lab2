from tools import ExpenseException


class Expense:
    def __init__(self, cost: str, category_name: str, name: str):
        try:
            cost = float(cost)
        except ValueError:
            raise ExpenseException(f"Недопустимая стоимость: '{cost}'. (Стоимость должна быть положительным числом)")

        if cost <= 0:
            raise ExpenseException(f"Недопустимая стоимость: '{cost}'. (Стоимость должна быть положительным числом)")

        self.name = name
        self.cost = round(cost, 2)
        self.category_name = category_name

    def to_csv(self):
        return f"{self.cost};{self.category_name};{self.name}"

    def __str__(self):
        return f"{self.name}\n  ├─ Категория: {self.category_name}\n  └─ Стоимость: {self.cost}"

