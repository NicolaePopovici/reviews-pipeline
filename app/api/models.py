import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

class Country(SQLModel, table=True):
    id: uuid.UUID = Field(default=uuid.uuid4(), primary_key=True)
    name: str = Field(sa_column_kwargs={"unique": True}, max_length=100)

class Countries(SQLModel):
    data: list[Country]
    count: int

class CountryCreate(SQLModel):
    name: str

class CountryPut(SQLModel):
    name: str