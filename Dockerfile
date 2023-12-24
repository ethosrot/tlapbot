FROM python:3-alpine

ENV SERVICE_NAME="tlapbot"
ENV FLASK_APP="tlapbot"
ARG UID=911
ARG GID=911

RUN apk update
RUN apk add bash

RUN addgroup -g ${GID} ${SERVICE_NAME} \
    && adduser -h /app -s /bin/false -D -G ${SERVICE_NAME} -u ${UID} ${SERVICE_NAME}

RUN mkdir /app/instance
RUN chown -R tlapbot. /app/instance
WORKDIR /app

COPY setup.py startup.sh ./
COPY tlapbot ./tlapbot

RUN pip install -e .
RUN pip install gunicorn

USER $SERVICE_NAME
EXPOSE 8000

ENTRYPOINT "/app/startup.sh"