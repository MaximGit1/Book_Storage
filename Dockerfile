FROM python:3.12.6-slim

WORKDIR /app

RUN pip install poetry && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-root

COPY . /app/

EXPOSE 8000

CMD ["python", "book_storage/manage.py", "runserver", "0.0.0.0:8000"]
