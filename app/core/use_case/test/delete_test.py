from app.ports.driven.database.postgres.test_repository_abc import TestRepositoryInterface
from app.ports.driving.handler_interface import HandlerInterface


class DeleteTestByIdHandler(HandlerInterface):
    def __init__(self, test_repository: TestRepositoryInterface) -> None:
        self._test_repository: TestRepositoryInterface=test_repository

    def execute(self, id: int) -> None:
        # Executes all business logic for the task
        # May involve multiple repository calls, data transformations, etc.
        # This use case is used by the endpoint (or any application output port)
        return self._test_repository.delete(id)
