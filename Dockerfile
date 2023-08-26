FROM python:3.10.2

ARG APP_VERSION
ARG SERVER

RUN echo "APP_VERSION = ${APP_VERSION}"
RUN echo "SERVER = ${SERVER}"

ENV APP_VERSION ${APP_VERSION}
ENV SERVER ${SERVER}

RUN mkdir banodoco-backend

WORKDIR banodoco-backend

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN echo "SERVER=production" > .env

COPY . .

EXPOSE 8080

CMD ["sh", "entrypoint.sh"]