FROM python:3.12
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY src src
COPY migrations migrations
COPY alembic.ini alembic.ini
CMD ["gunicorn", "--bind", "0.0.0.0:80", "src.torpedo:create_app()", "--timeout", "120"]
