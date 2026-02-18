from app.domain.config import settings
from app.domain.enums import Environment

class FeatureFlags:
    @property
    def is_development(self) -> bool:
        return settings.ENVIRONMENT == Environment.DEVELOPMENT.value

    @property
    def is_production(self) -> bool:
        return settings.ENVIRONMENT == Environment.PRODUCTION.value
    
    @property
    def clear_existing_data_for_development(self) -> bool:
        return settings.CLEAR_EXISTING_DATA_FOR_DEVELOPMENT