from src.utils.import_utils import import_models

models = import_models('src.db.models') + import_models('src.db.models.students')

for model in models:
    print(f"Found model: {model.__name__}")
