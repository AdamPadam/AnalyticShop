## Run application with poetry
```
git clone https://github.com/AlexandrChikur/fastapi-postgresql-quickstart.git
cd fastapi-postgresql-quickstart/
poetry install poetry shell
```
To run the web application in debug use:
```
uvicorn app.main:app --reload
```

## Run application in Docker\docker-compose
```
docker-compose up --build
```
---