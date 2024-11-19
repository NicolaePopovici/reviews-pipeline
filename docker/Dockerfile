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

COPY ./app /reviews-pipeline/app/

COPY ./alembic /reviews-pipeline/alembic/
COPY ./alembic.ini /reviews-pipeline/alembic.ini

ENV PYTHONPATH="${PYTHONPATH}:/reviews-pipeline/"

CMD ["fastapi", "run", "app/main.py", "--port", "80"]