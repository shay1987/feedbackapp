FROM python:3.9-alpine3.15

WORKDIR /app

COPY ./app/requirements.txt .
RUN pip install -r requirements.txt

COPY ./app .

ENTRYPOINT ["python3", "app.py"]