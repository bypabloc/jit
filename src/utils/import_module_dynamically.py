import importlib


def import_module_dynamically(module_name):
    try:
        module = importlib.import_module(module_name)
        print(f"El módulo '{module_name}' se ha importado correctamente.")
        return module
    except ImportError:
        print(f"Error al importar el módulo '{module_name}'.")
        return None
