from tools import ExpenseException


class Expense:
    def __init__(self, name: str, cost: str, category_name: str):
        try:
            cost = float(cost)
        except ValueError:
            raise ExpenseException(f"Недопустимая стоимость: '{cost}'. (Стоимость должна быть положительным числом)")

        if cost <= 0:
            raise ExpenseException(f"Недопустимая стоимость: '{cost}'. (Стоимость должна быть положительным числом)")

        self.name = name
        self.cost = cost
        self.category_name = category_name

    def to_csv(self):
        return f"{self.name};{self.cost};{self.category_name}"
