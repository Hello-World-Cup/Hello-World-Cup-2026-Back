from enum import Enum


class Environment(str, Enum):
    DEVELOPMENT="development"
    PRODUCTION="production"

class CompanyType(str, Enum):
    TEST_COMPANY="Compañía de test"

class SocialMedia(str, Enum):
    TEST_SOCIAL_MEDIA="Red social de test"

class UserStatus(int, Enum):
    INACTIVE=-1
    PENDING=0
    ACTIVE=1

class TeamRequestStatus(int, Enum):
    DENIED=-1
    PENDING=0
    ACCEPTED=1

