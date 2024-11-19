from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime


class CSVRow(BaseModel):
    reviewer_name: str
    review_title: str
    review_rating: int
    review_content: str
    email_address: EmailStr
    country: str
    review_date: str

    @field_validator('review_date')
    def check_date_format(cls, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError('review_date must be in the format YYYY-MM-DD')
        return value

    @field_validator('review_rating')
    def check_rating(cls, value):
        if value < 1 or value > 5:
            raise ValueError('review_rating must be between 1 and 5')
        return value

    @field_validator('review_content')
    def check_content_length(cls, value):
        if len(value) < 10:
            raise ValueError('review_content must be at least 10 characters long')
        return value

    @field_validator('review_title')
    def check_title_length(cls, value):
        if len(value) < 5:
            raise ValueError('review_title must be at least 5 characters long')
        return value

    @field_validator('reviewer_name')
    def check_name_length(cls, value):
        if len(value) < 5:
            raise ValueError('reviewer_name must be at least 5 characters long')
        return value
