import logging
from sqlalchemy.orm import Session

from app.adapters.database.postgres.models.category_model import Category
from app.adapters.database.postgres.models.edition_model import Edition
from datetime import datetime, timezone, timedelta

from app.adapters.database.postgres.models.evaluation_model import Evaluation
from app.adapters.database.postgres.models.role_model import Role
from app.adapters.database.postgres.models.sponsor_model import SocialMediaDefinition, Sponsor
from app.adapters.database.postgres.models.team_model import Team
from app.adapters.database.postgres.models.user_model import User, user_team_association, team_request_association
from app.ports.driving.seeder_interface import SeederInterface
from app.domain.enums import CompanyType, SocialMedia, TeamRequestStatus


class DevelopmentDataSeeder(SeederInterface):
    def __init__(self, db: Session) -> None:
        self.db=db
        self.logger=logging.getLogger(__name__)

    def run(self, clear_existing: bool=True) -> None:
        try:
            if clear_existing:
                self._clear_tables()

            self.logger.info("Development data seeding process started.")

            self._seed_tables()

            self.logger.info("Development data seeding process finished.")
            
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Error in development data model seeder: {str(e)}")
            raise

    def _clear_tables(self) -> None:
        self._clear_associations()

        self._clear_general_table("Edition", Edition)
        self._clear_general_table("Sponsor", Sponsor)
        self._clear_general_table("Role", Role)
        self._clear_general_table("Category", Category)
        self._clear_general_table("User", User)
        self._clear_general_table("Evaluation", Evaluation)
        self._clear_general_table("Team", Team)

    def _seed_tables(self) -> None:
        self._seed_edition_table()
        self._seed_sponsor_table()
        self._seed_role_table()
        self._seed_category_table()
        self._seed_user_table()
        self._seed_evaluation_table()
        self._seed_team_model()

        self._seed_associations()


    def _seed_edition_table(self) -> None:
        data=[
            Edition(
                id=1,
                name="HWC: SECOND EDITION",
                start_date=datetime.now(timezone.utc),
                end_date=datetime.now(timezone.utc) + timedelta(days=2),
            )
        ]

        self._seed_general_data("Edition", data)

    def _seed_sponsor_table(self) -> None:
        social_data=SocialMediaDefinition(
            type=SocialMedia.TEST_SOCIAL_MEDIA.value,
            identity="@usuario"
        )
        data=[
            Sponsor(
                id=1,
                company_name="Nombre",
                company_type=CompanyType.TEST_COMPANY.value,
                description="Descripción",
                slogan="Slogan",
                logo="nombre_del_logo.png",
                social_media=social_data,
                edition_id=1
            )
        ]

        self._seed_general_data("Sponsor", data)
    
    def _seed_role_table(self) -> None:
        data = [
            Role(
                id=1,
                name="Super Admin",
                description="Rol con todos los privilegios",
                is_super_user=True,
                internal_code="super_admin",
            ),
            Role(
                id=2,
                name="Competidor",
                description="Rol con privilegios de competidor",
                internal_code="competitor",
            ),
        ]

        self._seed_general_data("Role", data)

    def _seed_category_table(self) -> None:
        data=[
            Category(
                id=1,
                name="Junior",
                open_date=datetime.now(timezone.utc),
                close_date=datetime.now(timezone.utc) + timedelta(days=2),
                internal_code="junior_test",
            )
        ]

        self._seed_general_data("Category", data)

    def _seed_user_table(self) -> None:
        data = [
            User(
                id=1,
                username="super_admin",
                name="Super Admin",
                email="superadmin123@test.com",
                password_hash="password_hash",
                portrait=None,
                status=1,
                role_id=1,
                category_id=None,
            ),
            User(
                id=2,
                username="test_user",
                name="Test User",
                email="testuser123@test.com",
                password_hash="password_hash",
                portrait=None,
                status=1,
                role_id=2,
                category_id=1,
            ),
        ]

        self._seed_general_data("User", data)

    def _seed_evaluation_table(self) -> None:
        data = [
            Evaluation(
                id=1,
                file_name="evaluation_filename.pdf",
                category_id=1
            )
        ]

        self._seed_general_data("Evaluation", data)

    def _seed_team_model(self) -> None:
        data=[
            Team(
                id=1,
                name="Team Test",
                logo="nombre_del_logo.png",
                score=None,
                standing_position=None,
                cloud_repo_link=None,
                edition_id=1,
                category_id=1,
                evaluation_id=None,
                assigned_evaluator_id=1
            )
        ]

        self._seed_general_data("User", data)


    # UTILS

    def _seed_associations(self) -> None:
        self.db.execute(
            user_team_association.insert().values( # type: ignore
                [
                    {"user_id": 2, "team_id": 1},
                ]
            )
        )

        self.db.execute(
            team_request_association.insert().values(  # type: ignore
                [
                    {
                        "id": 1,
                        "team_id": 1,
                        "sender_user_id": 1,
                        "receiver_user_id": 2,
                        "status": TeamRequestStatus.PENDING.value,
                    },
                ]
            )
        )

        self.db.commit()
        self.logger.info("Associations seeded.")

    def _clear_associations(self) -> None:
        self.db.execute(user_team_association.delete()) # type: ignore
        self.db.execute(team_request_association.delete())  # type: ignore
        self.db.commit()
        self.logger.info("Associations cleared.")

    def _seed_general_data(self, table_name: str, data: list) -> None:
        created_count=0

        for register in data:
            self.db.add(register)
            created_count += 1

        self.db.commit()
        self.logger.info(f"{table_name} table: {created_count} records created.")

    def _clear_general_table(self, model_name: str, model) -> None:
        deleted_count=self.db.query(model).delete()
        self.db.commit()
        self.logger.info(f"Deleted {deleted_count} existing records from {model_name}.")
        pass