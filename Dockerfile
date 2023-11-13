# syntax=docker/dockerfile:1
FROM python:3.8-alpine
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "8000"]

EXPOSE 8000
STOPSIGNAL SIGINT
