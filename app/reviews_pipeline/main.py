import boto3
import csv
import io
from sqlalchemy.orm import Session
from botocore import UNSIGNED
from botocore.client import Config

from pydantic import ValidationError
from app.reviews_pipeline.database import crud
from app.reviews_pipeline.database import session_manager

from app.reviews_pipeline import settings
from app.reviews_pipeline.schema import CSVRow
logger = settings.logger


def process(session: Session):
    # Initialize S3 client
    # TODO: Use a singleton client to avoid creating a new client for each request
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

    # TODO: Add retry logic
    # TODO: Process data in batches
    response = s3.get_object(Bucket=settings.BUCKET_NAME, Key=settings.KEY)
    stream = response['Body']

    # Wrap the stream with TextIOWrapper to handle the CSV content as text
    csv_file = io.TextIOWrapper(stream, encoding='utf-8')
    csv_reader = csv.DictReader(csv_file)

    # Modify the header
    csv_reader.fieldnames = ['reviewer_name', 'review_title', 'review_rating',
                             'review_content', 'email_address', 'country', 'review_date']

    for line_number, row in enumerate(csv_reader, start=1):
        try:
            # Validate the row with Pydantic
            validated_row = CSVRow(**row)

            try:
                # Execute these operations in a transaction
                country = crud.get_country_by_name(session, validated_row.country)
                reviewer = crud.get_reviewer_by_email(
                    session, validated_row.email_address, validated_row.reviewer_name, country)
                crud.create_review(session, reviewer, validated_row.review_title,
                                   validated_row.review_rating, validated_row.review_content, validated_row.review_date)

                session.commit()
            except Exception as e:
                session.rollback()
                logger.error(f"Failed to save review: {e}")
        except ValidationError as e:
            # Add to a list/queue of validation errors to be processed later
            logger.error(f"Validation error at line {line_number}: {e}")
            pass


if __name__ == "__main__":
    with session_manager() as session:
        process(session)
