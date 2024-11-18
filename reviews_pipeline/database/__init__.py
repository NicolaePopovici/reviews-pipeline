import os
from typing import Any, Generator
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import URL, create_engine, MetaData
from sqlalchemy.orm import Session, sessionmaker

from reviews_pipeline.settings import logger


def get_database_url() -> URL:
    """
    Assembles the database URI from environment variables.
    """
    try:
        url = URL.create(
            drivername="postgresql",
            username=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],  # unescaped password
            host=os.environ["POSTGRES_URL"],
            port=os.environ["POSTGRES_PORT"],
            database=os.environ["POSTGRES_DB"],
        )
    except KeyError:
        logger.error("No PostgreSQL settings found in environment variables.")
        raise KeyError

    return url


dbschema = os.getenv("POSTGRES_DB_SCHEMA")
url = get_database_url()

engine = create_engine(
    url, connect_args={"options": "-csearch_path={}".format(dbschema)}
)

session_manager = sessionmaker(autocommit=False, bind=engine)
metadata = MetaData(schema=dbschema)
Base = declarative_base(metadata=metadata)


def get_database() -> Generator[Session, Any, None]:
    db = session_manager()
    try:
        yield db
    except Exception as e:
        logger.critical(f"Error in the DB session: {e}")
        raise e
    finally:
        db.close()
