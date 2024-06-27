FROM python:3.11-buster

RUN pip3 install poetry

WORKDIR /project
COPY . /project

RUN poetry install --without dev

CMD ["poetry", "run", "python", "-m", "app"]