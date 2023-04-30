from inquirer import Text as inquirer_Text
from inquirer import prompt as inquirer_prompt
from settings.logger import logger
from utils.object_validator import ObjectValidator


class GithubController:
    args = None

    def __init__(self, args: dict):
        self.args = args

    def execute(self):
        """
        ssh-keygen -t ed25519 -C "your_email@example.com" -f ~/.ssh/id_ed25519_github

        ? What account do you want to log into? GitHub.com
        ? You're already logged into github.com. Do you want to re-authenticate? Yes
        ? What is your preferred protocol for Git operations? SSH
        ? Upload your SSH public key to your GitHub account? /home/bypabloc/.ssh/id_ed25520.pub
        ? Title for your SSH key: pablo-destacame
        ? How would you like to authenticate GitHub CLI? Paste an authentication token
        Tip: you can generate a Personal Access Token here https://github.com/settings/tokens
        The minimum required scopes are 'repo', 'read:org', 'admin:public_key'.
        ? Paste your authentication token: *****************************************************
        ✓ Submitted
        """

        questions = [
            inquirer_Text(
                "email",
                message="What's your email?",
            ),
            inquirer_Text(
                "filename",
                message="Name of the file",
            ),
            inquirer_Text(
                "title",
                message="Title",
            ),
        ]
        answers = inquirer_prompt(questions)
        print(answers)

        validator = ObjectValidator({
            "email": {
                "required": True,
                "type": "str",
                "min_length": 2,
                "max_length": 100,
            },
        })
        data_validated = validator.validate(answers)
        if not data_validated:
            logger.error("Data not validated", extra=data_validated)
            # trow error
            
            return

        logger.info("Ejecutando comando 'github'.")
        logger.info(f"Argumentos: {self.args}")
        logger.info("Fin de la ejecución del comando 'github'.")

# ssh-keygen -t ed25519 -C "pacg1991@gmail.com"
