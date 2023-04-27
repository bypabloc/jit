from argparse import ArgumentParser as argparse_ArgumentParser
from inquirer import Text as inquirer_Text
from inquirer import prompt as inquirer_prompt
import re

# argparse
# https://docs.python.org/3/library/argparse.html
# https://docs.python.org/3/library/argparse.html#the-add-argument-method

# inquirer
# https://github.com/magmax/python-inquirer


def main():
    parser = argparse_ArgumentParser(description="Ejemplo de captura de variables por comandos")

    parser.add_argument("-N", "--name", required=True, help="Nombre de la persona")
    parser.add_argument("-L", "--lastname", required=True, help="Apellido de la persona")

    args = parser.parse_args()

    print(f"Nombre: {args.name}")
    print(f"Apellido: {args.lastname}")

    questions = [
        inquirer_Text('name', message="What's your name"),
        inquirer_Text('surname', message="What's your surname"),
        inquirer_Text('phone', message="What's your phone number", validate=lambda _, x: re.match('\+?\d[\d ]+\d', x),)
    ]
    answers = inquirer_prompt(questions)
    print(answers)


if __name__ == "__main__":
    main()
