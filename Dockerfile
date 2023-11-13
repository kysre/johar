# syntax=docker/dockerfile:1
FROM python:3.8
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "8000"]

EXPOSE 8000
STOPSIGNAL SIGINT
