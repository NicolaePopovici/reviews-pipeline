import uuid
from datetime import date
from sqlalchemy.orm import Session
from typing import Optional
from app.reviews_pipeline.database import models
from app.reviews_pipeline import settings
logger = settings.logger


def get_country_by_name(session: Session, name: str) -> Optional[models.Country]:
    logger.info(f"Checking if country {name} exists")
    country = session.query(models.Country).filter_by(name=name).first()

    if not country:
        country = models.Country(
            id=uuid.uuid4(),
            name=name
        )
        session.add(country)

    return country


def get_reviewer_by_email(session: Session, email: str, reviewer_name: str, country: models.Country) -> Optional[models.Reviewer]:
    logger.info(f"Checking if reviewer {email} exists")
    reviewer = session.query(models.Reviewer).filter_by(email_address=email).first()

    if not reviewer:
        reviewer = models.Reviewer(
            id=uuid.uuid4(),
            email_address=email,
            name=reviewer_name,
            country_id=country.id,
            country=country
        )
        session.add(reviewer)

    return reviewer


def create_review(session: Session, reviewer: models.Reviewer, title: str, rating: int, content: str, review_date: date) -> models.Review:
    logger.info(f"Saving review: {title}")

    try:
        review = models.Review(
            id=uuid.uuid4(),
            reviewer_id=reviewer.id,
            title=title,
            rating=rating,
            content=content,
            date=review_date,
        )
        session.add(review)
    except Exception as e:
        logger.error(f"Error saving review: {e}")
        raise e

    return review


def get_country(session: Session, name: str) -> Optional[models.Country]:
    logger.info(f"Checking if country {name} exists")

    try:
        country = session.query(models.Country).filter_by(name=name).first()
    except Exception as e:
        logger.error(f"Error retrieving country: {e}")
        raise e

    return country

def get_country_by_id(session: Session, id: uuid) -> Optional[models.Country]:
    logger.info(f"Checking if country {id} exists")

    try:
        country = session.query(models.Country).filter_by(id=id).first()
    except Exception as e:
        logger.error(f"Error retrieving country: {e}")
        raise e

    return country


def create_country(session: Session, name: str) -> models.Country:
    logger.info(f"Creating country: {name}")

    try:
        country = models.Country(
            id=uuid.uuid4(),
            name=name
        )
        session.add(country)
    except Exception as e:
        logger.error(f"Error creating country: {e}")
        raise e

    return country


def get_reviewer(session: Session, email_address: str) -> Optional[models.Country]:
    logger.info(f"Checking if reviewer {email_address} exists")

    try:
        reviewer = session.query(models.Reviewer).filter_by(email_address=email_address).first()
    except Exception as e:
        logger.error(f"Error retrieving reviewer: {e}")
        raise e

    return reviewer


def create_reviewer(session: Session, email_address: str, name: str, country_id: uuid) -> models.Reviewer:
    logger.info(f"Creating reviewer: {email_address}")

    try:
        reviewer = models.Reviewer(
            id=uuid.uuid4(),
            email_address=email_address,
            name=name,
            country_id=country_id
        )
        session.add(reviewer)
    except Exception as e:
        logger.error(f"Error creating reviewer: {e}")
        raise e

    return reviewer
