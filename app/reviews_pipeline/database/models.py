import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (String, Integer, Text, Date, ForeignKey, CheckConstraint)
from sqlalchemy.orm import (relationship, Mapped, mapped_column)
from . import Base


class Country(Base):
    __tablename__ = 'countries'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4, nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    reviewers: Mapped[list["Reviewer"]] = relationship(
        "Reviewer", back_populates="country")


class Reviewer(Base):
    __tablename__ = 'reviewers'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4, nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email_address: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True)
    country_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey('countries.id', ondelete="SET NULL"))

    country: Mapped["Country"] = relationship(
        "Country", back_populates="reviewers")
    reviews: Mapped[list["Review"]] = relationship(
        "Review", back_populates="reviewer")


class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4, nullable=False
    )
    reviewer_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('reviewers.id', ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, CheckConstraint(
        'rating >= 1 AND rating <= 5'), nullable=False)
    content: Mapped[str | None] = mapped_column(Text)
    date: Mapped[Date] = mapped_column(Date, nullable=False)

    reviewer: Mapped["Reviewer"] = relationship(
        "Reviewer", back_populates="reviews")
