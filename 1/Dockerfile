FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/
RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./app /code/app
COPY ./tests /code/tests

COPY ./alembic /code/alembic 
COPY ./alembic.ini /code/alembic.ini

EXPOSE 8080

CMD ["/bin/sh", "-c", \
    "alembic upgrade head && \
    uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]