FROM python:3.10.2

RUN mkdir banodoco-backend

WORKDIR banodoco-backend

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN echo "SERVER=production" > .env

COPY . .

EXPOSE 8080

CMD ["sh", "entrypoint.sh"]