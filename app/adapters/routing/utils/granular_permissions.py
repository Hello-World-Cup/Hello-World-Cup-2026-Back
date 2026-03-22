
from typing import Callable

from app.domain.dtos.user_dto import UserDTO
from app.domain.enums import UserStatus


class GranularFunctions:
    def get_granular_function(self, key: str) -> Callable[[UserDTO], bool] | None:
        granular_functions_dict: dict[str, Callable[[UserDTO], bool]] = {
            "check_if_user_is_active": self._check_if_user_is_active,
        }

        return granular_functions_dict.get(key)

    @staticmethod
    def _check_if_user_is_active(user: UserDTO) -> bool:
        return user.status == UserStatus.ACTIVE