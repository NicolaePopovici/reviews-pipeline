from typing import List

from reviews_pipeline.database import engine, models

models.Base.metadata.create_all(bind=engine)