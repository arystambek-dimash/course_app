from src.utils.import_utils import import_routers

root_routers = []

root_routers.extend(import_routers('src.api.v1.endpoints'))
root_routers.extend(import_routers('src.api.v1.endpoints.teachers'))
root_routers.extend(import_routers('src.api.v1.endpoints.students'))
