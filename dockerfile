FROM python:3.9-alpine
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add libpq-dev
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt 

COPY ./app/db db
COPY ./app/minio_S3 minio_S3
COPY ./app/sel sel
COPY ./app/main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]