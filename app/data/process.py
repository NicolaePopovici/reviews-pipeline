import csv
import io
from sqlalchemy.orm import Session
from pydantic import ValidationError
from app.database import crud, session_manager
from app.data.s3_client import get_s3_object
from app.data.schema import CSVRow
from app import settings
logger = settings.logger


def get_csv_reader(stream):
    # Wrap the stream with TextIOWrapper to handle the CSV content as text
    csv_file = io.TextIOWrapper(stream, encoding='utf-8')
    csv_reader = csv.DictReader(csv_file)
    csv_reader.fieldnames = list(CSVRow.model_fields.keys())

    return csv_reader


def process(session: Session):
    stream = get_s3_object(settings.BUCKET_NAME, settings.KEY)
    csv_reader = get_csv_reader(stream)

    # TODO: Process in batches
    for line_number, row in enumerate(csv_reader, start=1):
        try:
            # Validate the row with Pydantic
            validated_row = CSVRow(**row)

            try:
                # Execute these operations in a transaction
                country = crud.get_country_by_name(session, validated_row.country)
                reviewer = crud.get_reviewer_by_email(
                    session, validated_row.email_address, validated_row.reviewer_name, country)
                crud.create_review(session, reviewer.id, validated_row.review_title,
                    validated_row.review_rating, validated_row.review_content, validated_row.review_date)

                session.commit()
            except Exception as e:
                session.rollback()
                logger.error(f"Failed to save review: {e}")
        except ValidationError as e:
            # Add to a queue of validation errors to be processed later
            logger.error(f"Validation error at line {line_number}: {e}")
            pass


if __name__ == "__main__":
    with session_manager() as session:
        process(session)
