from app.settings.config import logger
from app.utils.execute_bash_command import execute_bash_command


def generate_virtual_env(path: str) -> None:
    """Generate virtual env"""
    command = f'python3.9 -m venv {path}/temp/.venv'
    logger.info('Generating virtual env', extra={'command': command})
    bashCommand = execute_bash_command(command=command)
    logger.info('Virtual env generated', extra={'bashCommand': bashCommand})
