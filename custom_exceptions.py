class MainException(Exception):
    default_message = "Ошибка: "

    def __init__(self, message: str) -> None:
        """
        Инициализация ошибки

        Добавляет в начало передаваемого сообщения значение default_message.
        """
        if not message.endswith("."):
            message += "."

        message = f"{self.default_message}{message}"
        super().__init__(message)


class WorkerException(MainException):
    default_message = "Ошибка выполнения: "


class ExpenseException(MainException):
    default_message = "Некорректные данные расхода: "


class CategoryException(MainException):
    default_message = "Некорректные данные категории: "


class CommandException(MainException):
    default_message = "Ошибка эксплуатации: "
