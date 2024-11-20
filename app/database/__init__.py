from typing import Any, Generator
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import URL, create_engine, MetaData
from sqlalchemy.orm import Session, sessionmaker

from app import settings
logger = settings.logger


def get_database_url() -> URL:
    """
    Assembles the database URI from environment variables.
    """
    try:
        url = URL.create(
            drivername="postgresql",
            username=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_URL,
            port=settings.POSTGRES_PORT,
            database=settings.POSTGRES_DB
        )
    except KeyError:
        message = "No PostgreSQL settings found in environment variables."
        logger.error(message)
        raise KeyError(message)

    return url


dbschema = settings.POSTGRES_DB_SCHEMA
url = get_database_url()

logger.info(f"Connecting to database {url} with schema {dbschema}")
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
