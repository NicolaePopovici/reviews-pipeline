from sqlalchemy import (
    String, Integer, Text, Date, ForeignKey, CheckConstraint
)
from sqlalchemy.orm import (
    relationship, Mapped, mapped_column
)
from . import Base


class Country(Base):
    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    reviewers: Mapped[list["Reviewer"]] = relationship(
        "Reviewer", back_populates="country")


class Reviewer(Base):
    __tablename__ = 'reviewers'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email_address: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True)
    country_id: Mapped[int | None] = mapped_column(
        ForeignKey('countries.id', ondelete="SET NULL"))

    country: Mapped["Country"] = relationship(
        "Country", back_populates="reviewers")
    reviews: Mapped[list["Review"]] = relationship(
        "Review", back_populates="reviewer")


class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    reviewer_id: Mapped[int] = mapped_column(
        ForeignKey('reviewers.id', ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, CheckConstraint(
        'rating >= 1 AND rating <= 5'), nullable=False)
    content: Mapped[str | None] = mapped_column(Text)
    review_date: Mapped[Date] = mapped_column(Date, nullable=False)

    reviewer: Mapped["Reviewer"] = relationship(
        "Reviewer", back_populates="reviews")
