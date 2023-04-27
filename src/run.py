from argparse import ArgumentParser as argparse_ArgumentParser
from re import match as re_match
from sys import exit as sys_exit
from sys import stderr as sys_stderr
from traceback import format_exc

from inquirer import Text as inquirer_Text
from inquirer import prompt as inquirer_prompt
from settings.logger import logger
from utils.import_all_modules_from_folder import import_all_modules_from_folder
from utils.import_module_dynamically import import_module_dynamically

# argparse
# https://docs.python.org/3/library/argparse.html
# https://docs.python.org/3/library/argparse.html#the-add-argument-method

# inquirer
# https://github.com/magmax/python-inquirer


class CustomArgumentParser(argparse_ArgumentParser):
    def error(self, message):
        sys_stderr.write(f"Error: {message}\n")
        self.print_help()
        sys_exit(2)


def main():
    parser = CustomArgumentParser(
        description="Ejemplo de captura de variables por comandos",
    )

    parser.add_argument(
        "-c",
        "--command",
        required=True,
        help="Comando a ejecutar",
    )

    try:
        args = parser.parse_args()
    except SystemExit as e:
        # En este punto, puedes manejar el error de la forma que desees.
        # Por ejemplo, puedes registrar el error o enviar una notificación.
        print("Se encontró un error al procesar los argumentos.")
        sys_exit(e.code)

    path_commands = "commands"

    modules = import_all_modules_from_folder(directory=path_commands)

    command = args.command

    if command not in modules:
        logger.info(f"El comando '{command}' no existe.")
        sys_exit(1)

    path_command = path_commands.replace("/", ".") + f".{command}"
    command_imported = import_module_dynamically(path_command)

    if command_imported is None:
        logger.error(f"El módulo '{command}' no existe.")
        sys_exit(1)

    command_pascal_case = command.capitalize()
    imported_class = getattr(command_imported, f"{command_pascal_case}Controller")
    instancia_de_clase = imported_class(args=vars(args))
    execute = getattr(instancia_de_clase, "execute")
    execute()

    # questions = [
    #     inquirer_Text(
    #         "name",
    #         message="What's your name",
    #     ),
    #     inquirer_Text("surname", message="What's your surname"),
    #     inquirer_Text(
    #         "phone",
    #         message="What's your phone number",
    #         validate=lambda _, x: re_match("\+?\d[\d ]+\d", x),
    #     ),
    # ]
    # answers = inquirer_prompt(questions)
    # print(answers)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Saliendo...")
        sys_exit(0)
    except Exception:
        logger.error('Se encontró un error:', extra=format_exc())
        sys_exit(1)
