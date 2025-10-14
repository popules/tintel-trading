FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir --upgrade pip
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .

COPY app ./app
COPY alembic.ini ./
COPY alembic ./alembic

ENV PORT=8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
