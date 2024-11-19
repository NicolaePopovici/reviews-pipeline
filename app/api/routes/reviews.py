
import uuid
from typing import Any
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlmodel import func, select

from app.reviews_pipeline import settings
from app.reviews_pipeline.database import get_database, models, crud
from app.api.models import Review, Reviews, ReviewCreate

router = APIRouter()
logger = settings.logger


@router.get("/", response_model=Reviews)
def read_reviews(session: Session = Depends(get_database), skip: int = 0, limit: int = 100) -> Any:
    try:
        count_statement = select(func.count()).select_from(models.Review)
        count = session.scalar(count_statement)
        statement = select(models.Review).offset(skip).limit(limit)
        reviews = session.scalars(statement).all()

        logger.info(f"Found {reviews} reviews")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return Reviews(data=reviews, count=count)


@router.get("/{review_id}", response_model=Review)
def read_review(review_id: uuid.UUID, session: Session = Depends(get_database)) -> Any:
    try:
        statement = select(models.Review).where(models.Review.id == review_id)
        review = session.scalar(statement)

        logger.info(f"Found review {review}")
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return review


@router.post("/", response_model=Review)
def create_reviewer(review_in: ReviewCreate, session: Session = Depends(get_database)) -> Any:
    try:
        reviewer = crud.get_reviewer_by_id(session=session, id=review_in.reviewer_id)
        if not reviewer:
            raise HTTPException(
                status_code=400,
                detail="The reviewer id is not valid.",
            )

        review = crud.create_review(
            session=session,
            reviewer_id=review_in.reviewer_id,
            title=review_in.title,
            rating=review_in.rating,
            content=review_in.content,
            date=review_in.date
        )
        session.commit()
        return review
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{review_id}", status_code=200)
def delete_review(review_id: uuid.UUID, session: Session = Depends(get_database)) -> Any:
    try:
        logger.info(f"Deleting reviewer {review_id}")
        statement = select(models.Review).where(models.Review.id == review_id)
        review = session.scalar(statement)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        session.delete(review)
        session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
