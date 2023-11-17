# syntax=docker/dockerfile:1
FROM python:3.8-alpine
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "johar.wsgi:application", "--bind", "0.0.0.0:8000"]

EXPOSE 8000
STOPSIGNAL SIGINT
