import subprocess

from app.utils.custom_exception import CustomException
from app.settings.config import logger


def execute_bash_command(command: str) -> None:
    """Execute bash command"""
    process = subprocess.Popen(
        command.split(),
        stdout=subprocess.PIPE,
        text=True,
    )
    output, error = process.communicate()
    if error:
        logger.error('Error', extra={'error': error})
        raise CustomException(
            message='ERROR',
            message_type='ERROR',
            status_code=500,
        )
    return output
