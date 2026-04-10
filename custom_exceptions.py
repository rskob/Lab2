class MainException(Exception):
    default_message = "Ошибка: "

    def __init__(self, message) -> None:
        """
        Инициализация ошибки

        Добавляет в начало передаваемого сообщения значение default_message.
        """
        message = f"{self.default_message}{message}"
        super().__init__(message)


class WorkerException(MainException):
    pass


class ExpenseException(MainException):
    pass


class CategoryException(MainException):
    pass


class CommandException(MainException):
    default_message = "Ошибка эксплуатации: "
