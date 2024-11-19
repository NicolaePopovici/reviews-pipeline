from app.api.models import Country, Countries, CountryCreate, CountryPut
import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlmodel import func, select
from app.reviews_pipeline.database import get_database, models, crud
from app.reviews_pipeline import settings


router = APIRouter()
logger = settings.logger


@router.get("/", response_model=Countries)
def read_countries(session: Session = Depends(get_database), skip: int = 0, limit: int = 100) -> Any:
    try:
        count_statement = select(func.count()).select_from(models.Country)
        count = session.scalar(count_statement)
        logger.info(f"Found {count} countries")
        statement = select(models.Country).offset(skip).limit(limit)
        countries = session.scalars(statement).all()
        logger.info(f"Returning {len(countries)} countries")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return Countries(data=countries, count=count)


@router.get("/{country_id}", response_model=Country)
def read_country(country_id: uuid.UUID, session: Session = Depends(get_database)) -> Any:
    try:
        statement = select(models.Country).where(models.Country.id == country_id)
        country = session.scalar(statement)

        logger.info(f"Found country {country}")
        if not country:
            raise HTTPException(status_code=404, detail="Country not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return country


@router.post("/", response_model=Country)
def create_country(country_in: CountryCreate, session: Session = Depends(get_database)) -> Any:
    try:
        country = crud.get_country_by_name(session=session, name=country_in.name)
        if country:
            raise HTTPException(
                status_code=400,
                detail="The country name is already exists in the system.",
            )

        country = crud.create_country(session=session, name=country_in.name)
        session.commit()
        return country
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{country_id}", response_model=Country)
def update_country(country_id: uuid.UUID, country_in: CountryPut, session: Session = Depends(get_database)) -> Any:
    try:
        country = session.get(models.Country, country_id)
        if not country:
            raise HTTPException(status_code=404, detail="Country not found")
        update_dict = country_in.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(country, key, value)
        session.add(country)
        session.commit()
        session.refresh(country)
        return country
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{country_id}", status_code=200)
def delete_country(country_id: uuid.UUID, session: Session = Depends(get_database)) -> Any:
    try:
        statement = select(models.Country).where(models.Country.id == country_id)
        country = session.scalars(statement).one()
        if not country:
            raise HTTPException(status_code=404, detail="Country not found")
        session.delete(country)
        session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
