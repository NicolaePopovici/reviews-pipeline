from fastapi import APIRouter
from fastapi import FastAPI

from app.api.routes import countries, reviewers
from app.reviews_pipeline.settings import API_V1_STR

app = FastAPI()

api_router = APIRouter()

api_router.include_router(countries.router, prefix="/countries", tags=["countries"])
api_router.include_router(reviewers.router, prefix="/reviewers", tags=["reviewers"])

app.include_router(api_router, prefix=API_V1_STR)