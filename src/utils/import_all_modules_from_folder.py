import os

from settings.logger import logger


def import_all_modules_from_folder(directory: str) -> list:

    logger.info(f"Importing all modules from folder '{directory}'")

    current_file_dir = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.dirname(current_file_dir)
    directory_path = os.path.join(root_dir, directory)
    list_directory = os.listdir(directory_path)

    modules = []
    for filename in list_directory:
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]  # Elimina la extensión ".py" del nombre del archivo
            modules.append(module_name)
    return modules
