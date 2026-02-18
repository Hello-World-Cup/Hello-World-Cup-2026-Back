from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from pydantic import BaseModel # type: ignore

from app.adapters.database.postgres.connection import Base
from app.adapters.database.postgres.models.utils import PydanticJSONB
from app.domain.enums import CompanyType, SocialMedia

class SocialMediaDefinition(BaseModel):
    type: SocialMedia
    identity: str


class Sponsor(Base):
    __tablename__="sponsor"

    id=Column(Integer, primary_key=True)
    company_name=Column(String, nullable=False, index=True)
    company_type=Column(Enum(CompanyType), nullable=False)
    description=Column(String, nullable=False)
    slogan=Column(String, nullable=False)
    logo=Column(String, nullable=False)

    social_media=Column(PydanticJSONB(SocialMediaDefinition))

    edition_id=Column(
        Integer, ForeignKey("edition.id", ondelete="CASCADE"), nullable=False
    )
