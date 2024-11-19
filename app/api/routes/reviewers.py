
import uuid
from typing import Any
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlmodel import func, select

from app.reviews_pipeline import settings
from app.reviews_pipeline.database import get_database, models, crud
from app.api.models import Reviewer, Reviewers, ReviewerCreate, ReviewerPut

router = APIRouter()
logger = settings.logger


@router.get("/", response_model=Reviewers)
def read_reviewers(session: Session = Depends(get_database), skip: int = 0, limit: int = 100) -> Any:
    try:
        count_statement = select(func.count()).select_from(models.Reviewer)
        count = session.scalar(count_statement)
        statement = select(models.Reviewer).offset(skip).limit(limit)
        reviewers = session.scalars(statement).all()

        logger.info(f"Found {reviewers} reviewers")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return Reviewers(data=reviewers, count=count)


@router.get("/{reviewer_id}", response_model=Reviewer)
def read_reviewer(reviewer_id: uuid.UUID, session: Session = Depends(get_database)) -> Any:
    try:
        statement = select(models.Reviewer).where(models.Reviewer.id == reviewer_id)
        reviewer = session.scalar(statement)

        logger.info(f"Found reviewer {reviewer}")
        if not reviewer:
            raise HTTPException(status_code=404, detail="Reviewer not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return reviewer


@router.post("/", response_model=Reviewer)
def create_reviewer(reviewer_in: ReviewerCreate, session: Session = Depends(get_database)) -> Any:
    try:
        reviewer = crud.get_reviewer(session=session, email_address=reviewer_in.email_address)
        if reviewer:
            raise HTTPException(
                status_code=400,
                detail="The reviewer email_address is already exists in the system.",
            )

        country = crud.get_country_by_id(session=session, id=reviewer_in.country_id)
        if not country:
            raise HTTPException(
                status_code=400,
                detail="The country id is not valid.",
            )

        reviewer = crud.create_reviewer(
            session=session,
            name=reviewer_in.name,
            email_address=reviewer_in.email_address,
            country_id=reviewer_in.country_id
        )
        session.commit()
        return reviewer
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{reviewer_id}", response_model=Reviewer)
def update_reviewer(reviewer_id: uuid.UUID, reviewer_in: ReviewerPut, session: Session = Depends(get_database)) -> Any:
    try:
        reviewer = session.get(models.Reviewer, reviewer_id)
        if not reviewer:
            raise HTTPException(status_code=404, detail="Reviewer not found")

        country = crud.get_country_by_id(session=session, id=reviewer_in.country_id)
        if not country:
            raise HTTPException(
                status_code=400,
                detail="The country id is not valid.",
            )

        update_dict = reviewer_in.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(reviewer, key, value)
        session.add(reviewer)
        session.commit()
        session.refresh(reviewer)
        return reviewer
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{reviewer_id}", status_code=200)
def delete_reviewer(reviewer_id: uuid.UUID, session: Session = Depends(get_database)) -> Any:
    try:
        logger.info(f"Deleting reviewer {reviewer_id}")
        statement = select(models.Reviewer).where(models.Reviewer.id == reviewer_id)
        reviewer = session.scalar(statement)
        if not reviewer:
            raise HTTPException(status_code=404, detail="Reviewer not found")
        session.delete(reviewer)
        session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
