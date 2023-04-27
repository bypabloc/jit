from argparse import ArgumentParser as argparse_ArgumentParser
from re import match as re_match
from sys import exit as sys_exit
from sys import stderr as sys_stderr

from inquirer import Text as inquirer_Text
from inquirer import prompt as inquirer_prompt

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

    print(f"command: {args.command}")

    questions = [
        inquirer_Text(
            "name",
            message="What's your name",
        ),
        inquirer_Text("surname", message="What's your surname"),
        inquirer_Text(
            "phone",
            message="What's your phone number",
            validate=lambda _, x: re_match("\+?\d[\d ]+\d", x),
        ),
    ]
    answers = inquirer_prompt(questions)
    print(answers)


if __name__ == "__main__":
    main()
