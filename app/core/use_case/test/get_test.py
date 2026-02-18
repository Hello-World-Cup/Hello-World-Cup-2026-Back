from app.domain.dtos.test_dto import TestDTO
from app.ports.driven.database.postgres.test_repository_abc import TestRepositoryInterface
from app.ports.driving.handler_interface import HandlerInterface


class GetTestByIdHandler(HandlerInterface):
    def __init__(self, test_repository: TestRepositoryInterface) -> None:
        self._test_repository: TestRepositoryInterface=test_repository

    def execute(self, id: int) -> TestDTO | None:
        # Ejecuta toda la lógica de negocio asociada a la tarea
        # Pueden ser múltiples llamadas a repositorios, transformaciones de datos, etc
        # Este caso de uso es el que usa el endpoint (o cualquier puerto de salida de la aplicación)
        return self._test_repository.read(id)