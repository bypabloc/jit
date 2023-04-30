import subprocess

from settings.logger import logger


def execute_bash_command(params: dict):
    """Execute bash command"""
    logger.info("Ejecutando comando 'execute_bash_command'.")
    logger.info(f"Argumentos: {params}")

    args = []
    for key, value in params.items():
        args.append(f"-{key}")
        if value is not None:
            args.append(value)

    process = subprocess.run(["ssh-keygen", "-t", "ed25519", "-C", email, "-f", output_file], check=True)
    if not process:
        logger.error("Error al ejecutar el comando 'ssh-keygen'.")
        return
    return process
