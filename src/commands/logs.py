from settings.logger import logger


class LogsController:
    args = None

    def __init__(self, args: dict):
        self.args = args

    def execute(self):
        logger.print_logs()
