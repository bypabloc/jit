from settings.logger import logger


class GitHubController:
    args = None

    def __init__(self, args: dict):
        self.args = args

    def execute(self):
        logger.info("Ejecutando comando 'github'.")
        logger.info(f"Argumentos: {self.args}")
        logger.info("Fin de la ejecución del comando 'github'.")
