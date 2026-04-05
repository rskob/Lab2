class MainException(Exception):
    default_message = "Ошибка: "

    def __init__(self, message):
        message = f"{self.default_message}{message}"
        super().__init__(message)


class WorkerException(MainException):
    pass


class ExpenseException(MainException):
    pass
