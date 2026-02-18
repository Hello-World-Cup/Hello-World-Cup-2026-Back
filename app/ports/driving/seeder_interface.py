from abc import ABC, abstractmethod


class SeederInterface(ABC):
    @abstractmethod
    def run(clear_existing) -> None:
        raise NotImplementedError("Run method not implemented for seeder.")
