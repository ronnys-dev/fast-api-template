FROM python:3.10-slim as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10-alpine

WORKDIR /backend

COPY --from=requirements-stage /tmp/requirements.txt /backend/requirements.txt

RUN pip install --no-cache-dir psycopg2-binary==2.9.3 `# проблемы с установкой через poetry на apple silicon`
RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

COPY . /backend
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]