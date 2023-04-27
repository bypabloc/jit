import importlib


def import_module_dynamically(module_name):
    try:
        return importlib.import_module(module_name)
    except ImportError:
        print(f"Error al importar el módulo '{module_name}'.")
        return None
