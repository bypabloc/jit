import os
import sys


def import_all_modules_from_folder(folder_path: str) -> list:
    sys.path.insert(0, folder_path)  # Agrega la carpeta al path de Python para que pueda encontrar los módulos

    modules = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]  # Elimina la extensión ".py" del nombre del archivo
            modules.append(module_name)
    return modules
