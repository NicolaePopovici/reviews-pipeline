FROM python:3.12

EXPOSE 80
WORKDIR /reviews-pipeline

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Needed for dependency pinning
COPY ./pyproject.toml ./poetry.lock ./

# Install fastapi dependencies
RUN pip install "fastapi[standard]"

# Allow installing dev dependencies to run tests
RUN poetry install --no-dev

COPY ./reviews_pipeline /reviews-pipeline/reviews_pipeline/

COPY ./alembic /reviews_pipeline/alembic/
COPY ./alembic.ini /reviews_pipeline/alembic.ini

ENV PYTHONPATH="${PYTHONPATH}:/reviews_pipeline/"

CMD ["fastapi", "run", "app/main.py", "--port", "80"]