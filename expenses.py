import sys
from worker import Worker, WorkerData
from custom_exceptions import MainException
from settings import *


if __name__ == "__main__":
    storage = WorkerData(EXPENSES_FILE_PATH, CATEGORIES_FILE_PATH)
    worker = Worker(storage)

    try:
        worker.execute(sys.argv)
    except MainException as exception:
        print(*exception.args)
