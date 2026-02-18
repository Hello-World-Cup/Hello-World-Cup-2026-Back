import logging
from sqlalchemy.orm import Session
from app.adapters.database.postgres.models.test_model import Test
from datetime import datetime, timezone

from app.ports.driving.seeder_interface import SeederInterface


class TestSeeder(SeederInterface):
    def __init__(self, db: Session):
        self.db=db
        self.logger=logging.getLogger(__name__)

    def run(self, clear_existing: bool=True) -> None:
        try:
            if clear_existing:
                self._clear_table()

            created_count=self._seed_tests()

            self.db.commit()
            self.logger.info(
                f"Test model seed process completed. {created_count} records created"
            )

        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Error in test model seeder: {str(e)}")
            raise

    def _clear_table(self) -> None:
        deleted_count=self.db.query(Test).delete()
        self.logger.info(f"Deleted {deleted_count} existing records from tests")

    def _seed_tests(self) -> int:
        test_messages=[
            "Hello, World! This is a test message.",
            "Testing the database seeder functionality.",
            "This is another test message for the Test model.",
            f"Seeder run at {datetime.now(timezone.utc)}",
        ]

        created_count=0

        for _id, message in enumerate(test_messages, 1):
            test=Test(id=_id, message=message)
            self.db.add(test)
            created_count += 1

        return created_count
