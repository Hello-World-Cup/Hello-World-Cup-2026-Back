from enum import Enum, auto


class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"