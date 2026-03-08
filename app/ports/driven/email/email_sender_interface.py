from abc import ABC, abstractmethod


class EmailSenderInterface(ABC):
    @abstractmethod
    def send_verification_email(self, to_email: str, user_name: str, verify_link: str) -> None:
        pass