import importlib
import pkgutil

from fastapi import APIRouter


def import_routers(package_name):
    routers = []
    package = importlib.import_module(package_name)
    prefix = package.__name__ + "."

    for _, module_name, _ in pkgutil.iter_modules(package.__path__, prefix):
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, 'router') and isinstance(module.router, APIRouter):
                routers.append(module.router)
        except Exception as e:
            print(f"Failed to import {module_name}, error: {e}")
    return routers


def import_models(package_name):
    from src.db.database import Base
    models = []
    package = importlib.import_module(package_name)

    print(f"Importing from package: {package_name}")

    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        full_module_name = f"{package_name}.{module_name}"
        try:
            print(f"Importing module: {full_module_name}")
            module = importlib.import_module(full_module_name)
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, Base) and attr is not Base:
                    print(f"Found model: {attr.__name__}")
                    models.append(attr)
        except Exception as e:
            print(f"Failed to import {full_module_name}, error: {e}")

    return models
