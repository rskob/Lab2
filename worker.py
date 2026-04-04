class Worker:
    commands = {"add-category": "add_category"}

    def __init__(self):
        self.categories = []

    def execute_command(self, arguments: list):
        command_name = arguments[0]
        method = getattr(self, command_name, None)
        if method:
            return method(arguments[1:])
        else:
            raise AttributeError("Нет такой команды")

