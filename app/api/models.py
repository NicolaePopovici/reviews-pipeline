import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# Country routes

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


# Reviewer routes

class Reviewer(SQLModel, table=True):
    id: uuid.UUID = Field(default=uuid.uuid4(), primary_key=True)
    name: str = Field(max_length=100)
    email_address: EmailStr = Field(sa_column_kwargs={"unique": True}, max_length=255)
    country_id: uuid.UUID = Field(foreign_key="countries.id", nullable=True)


class Reviewers(SQLModel):
    data: list[Reviewer]
    count: int


class ReviewerCreate(SQLModel):
    name: str
    email_address: EmailStr
    country_id: uuid.UUID


class ReviewerPut(SQLModel):
    name: str
    country_id: uuid.UUID
