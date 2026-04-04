import os
from tools import WorkerException


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



class Worker:
    commands = {"add-category": "add_category"}

    def __init__(self, storage):
        self.categories = []
        self.storage = storage

    def execute(self, arguments):
        command_name = self.commands.get(arguments[1])
        method = getattr(self, command_name, None)
        if method:
            return method(arguments[2:])
        else:
            raise WorkerException("Нет такой команды")


    def add_category(self, arguments):
        if len(arguments) > 1:
            raise WorkerException("Команда add-category принимает лишь один аргумент")

        category_name = arguments[0]
        available_categories = self.storage.get_categories()
        if category_name in available_categories:
            raise WorkerException(f"Такая категория уже существует: '{category_name}'")
        else:
            self.storage.save_category(category_name)

