import uuid
from datetime import date

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


# Review routes

class Review(SQLModel, table=True):
    id: uuid.UUID = Field(default=uuid.uuid4(), primary_key=True)
    reviewer_id: uuid.UUID = Field(foreign_key="reviewers.id")
    title: str = Field(max_length=255)
    rating: int = Field(ge=0, le=5)
    content: str = Field(default=None)
    date: date


class Reviews(SQLModel):
    data: list[Review]
    count: int


class ReviewCreate(SQLModel):
    title: str
    rating: int
    content: str
    date: date
    reviewer_id: uuid.UUID
