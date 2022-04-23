FROM python:3.8-slim-buster

LABEL name="ForgeNode Tools Backend"

RUN apt-get update && apt-get install -y curl

RUN apt-get install -y git

RUN apt-get install -y --reinstall build-essential

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

ENV PATH="${PATH}:/root/.poetry/bin"

WORKDIR /forgenode/

COPY ./poetry.* ./pyproject.toml /forgenode/

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0"]
#CMD ["tail", "-F", "anything"]