from pathlib import Path
from costs import Category, Expense
from custom_exceptions import CategoryException


class WorkerData:
    SERIALIZERS = {
        Category: lambda obj: f"{obj.name}",
        Expense: lambda obj: f"{obj.cost};{obj.category};{obj.name}"
    }

    DESERIALIZERS = {
        Expense: lambda string: Expense((data := string.split(";"))[0], Category(data[1]), data[2]),
        Category: lambda string: Category(string)  # <- Пока что нет смысла в использовании
    }

    def __init__(self, expenses_filepath: str, categories_filepath: str) -> None:
        self.expenses_filepath = expenses_filepath  # Путь к файлу, в котором хранится информация о расходах
        self.categories_filepath = categories_filepath  # Путь к файлу, в котором хранится информация о категориях

        self.__prepare_storage()  # Подготовка хранилища к работе

    def __prepare_storage(self) -> None:
        """Создаёт файлы, если они не существуют, и директории, в которых они находятся, если они указаны в пути"""
        for filepath in (self.expenses_filepath, self.categories_filepath):
            path = Path(filepath)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch(exist_ok=True)

    def get_categories_names(self) -> list[str]:
        """Возвращает список названий имеющихся категорий"""
        with open(self.categories_filepath, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines()]

    def category_exists(self, category_name: str) -> bool:
        """Проверят, существует ли указанная категория"""
        return category_name.strip() in self.get_categories_names()

    def save_category(self, category: Category) -> None:
        """Записывает название категории в файл"""
        if self.category_exists(category.name):
            raise CategoryException(f"такая категория уже существует -> '{category}'.")

        with open(self.categories_filepath, "a", encoding="utf-8") as file:
            file.write(self.serialize(category) + "\n")

    def create_category(self, category_name: str) -> Category:
        """Возвращает экземпляр класса Category"""
        return Category(category_name)

    def get_category(self, category_name: str) -> Category:
        """Возвращает экземпляр класса Category, если категория с таким именем существует"""
        if not self.category_exists(category_name):
            raise CategoryException(f"категория не существует -> '{category_name}'.")

        return Category(category_name)

    def create_expense(self, cost: str, category: Category, name: str) -> Expense:
        """Создаёт экземпляр класса Expense"""
        return Expense(cost, category, name)

    def get_expenses(self) -> list[Expense]:
        """Возвращает информацию о расходах в виде списка, состоящего из экземпляров класса Expense"""
        with open(self.expenses_filepath, "r", encoding="utf-8") as file:
            return [self.deserialize(line.strip(), Expense) for line in file.readlines()]

    def save_expense(self, expense: Expense) -> None:
        """Записывает информацию о расходе в файл"""
        with open(self.expenses_filepath, "a", encoding="utf-8") as file:
            file.write(self.serialize(expense) + "\n")

    def serialize(self, obj: Category | Expense) -> str:
        """Сериализирует передаваемый объект"""
        return self.SERIALIZERS[type(obj)](obj)

    def deserialize(self, data: str, obj_type) -> Category | Expense:
        """Десериализирует передаваемую строку данных в соответствии с указанным типом объекта"""
        return self.DESERIALIZERS[obj_type](data)
