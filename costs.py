import math
from custom_exceptions import ExpenseException, CategoryException


class Category:
    def __init__(self, category_name: str) -> None:
        """Инициализация категории"""
        if not self.validate_name(category_name):
            raise CategoryException(f"недопустимое название категории -> '{category_name}'."
                                    " Название категории может содержать только буквы, цифры,"
                                    " пробелы и символы нижнего подчёркивания.\n"
                                    "Также оно не может быть пустой строкой и состоять только их пробелов.")

        self.name = category_name.strip()

    @staticmethod
    def validate_name(category_name: str):
        """Валидация названия категории"""
        return category_name and not all(char == " " for char in category_name) and \
               all(char.isalnum() or char in (" ", "_") for char in category_name)

    def to_csv(self):
        """Возвращает информацию об объекте в виде <название>. Метод реализован для масштабируемости."""
        return f"{self.name}"

    def __str__(self):
        """Метод, необходимый для корректной работы с данными. Представляет класс в виде строки '<название>'."""
        return self.name

    def __eq__(self, other):
        """Реализация логики сравнения двух категорий."""
        return self.name == other.name


class Expense:
    def __init__(self, cost: str, category: Category, name: str) -> None:
        """Инициализация расхода"""
        if not self.validate_name(name):
            raise ExpenseException(f"недопустимое название расхода -> '{name}'."
                                   f" Название расхода должно содержать только буквы, цифры,"
                                   f" пробелы и символы нижнего подчёркивания.\n"
                                   f"Также оно не может быть пустой строкой и состоять только их пробелов.")
        if not (f_cost := self.validate_cost(cost)):
            raise ExpenseException(f"недопустимая стоимость расхода -> '{cost}'."
                                f" Стоимость расхода должна быть положительным числом (0.01 <= стоимость <= 10 ^ 13).")

        # Нет смысла в валидации категории, так как некорректная категория не была бы добавлена в файл
        self.name = name.strip()  # Название расхода
        self.cost = math.trunc(f_cost * 100) / 100  # Стоимость расхода (Оставляем только 2 знака после запятой)
        self.category = category  # Экземпляр класса Category

    def to_csv(self) -> str:
        """Представляет информацию о расходе в виде строки '<стоимость>;<категория>;<название>"""
        return f"{self.cost};{self.category};{self.name}"

    def __str__(self) -> str:
        """Представляет расход в понятном виде"""
        return f"{self.name}\n  ├─ Категория: {self.category}\n  └─ Стоимость: {self.cost:.2f}"

    @staticmethod
    def validate_name(name: str) -> bool:
        """Валидация имени"""
        return name and not all(char == " " for char in name) and \
               all(char.isalnum() or char in (" ", "_") for char in name)

    @staticmethod
    def validate_cost(cost: str) -> bool | int:
        """Валидация цены"""
        try:
            f_cost = float(cost)
        except ValueError:
            return False

        return f_cost if math.isfinite(f_cost) and 0.01 <= f_cost <= 1e13 else False
