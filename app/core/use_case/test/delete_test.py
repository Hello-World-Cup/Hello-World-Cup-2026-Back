from app.ports.driven.database.postgres.test_repository_abc import TestRepositoryABC
from app.ports.driving.handler_interface import HandlerInterfaceABC


class DeleteTestByIdHandler(HandlerInterfaceABC):
    def __init__(self, test_repository: TestRepositoryABC) -> None:
        self._test_repository: TestRepositoryABC = test_repository

    def execute(self, id: int) -> None:
        # Ejecuta toda la lógica de negocio asociada a la tarea
        # Pueden ser múltiples llamadas a repositorios, transformaciones de datos, etc
        # Este caso de uso es el que usa el endpoint (o cualquier puerto de salida de la aplicación)
        return self._test_repository.delete(id)
