from sqlmodel import Session

from app.database import crud
from app.database.models import Country


def create_random_country(db: Session) -> Country:
    name = "random_lower_string"
    
    return crud.create_country(session=db, name=name)
