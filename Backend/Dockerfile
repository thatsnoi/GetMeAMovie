FROM python:3.8-slim-buster

EXPOSE 8000
WORKDIR /api

# Copy project files
COPY app ./app
COPY poetry.lock pyproject.toml ./

RUN pip install poetry && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-dev

# Run FastAPI on the specified port using 4 async workers
CMD poetry run gunicorn --bind 0.0.0.0:$PORT --workers 4 --worker-class uvicorn.workers.UvicornWorker app.main:app
