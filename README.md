# Docker project with Streamlit, FastAPI and SQLite

This project is a demonstration of using Docker Compose to run a `Python` application consisting of `Streamlit`, `FastAPI`, and `SQLite` in `Docker` containers.<br>

## Prerequisites

Make sure you have `Docker` and `Docker Compose` installed on your machine.

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

<!-- ## Make migration

Move in `server` folder

```bash
python migrate.py
``` -->

## Clone project

```bash
git clone https://github.com/moiseberthe/sise-nlp.git
```

## Project structure

- `client/`: Application Streamlit
- `server/`: Application FastAPI

## Docker setup
The Docker files (`client/Dockerfile` and `server/Dockerfile`) contain the build configurations for the Streamlit and FastAPI services.<br>

The `docker-compose.yml` file contains the Docker configuration for the services.

### Build and run containers

```bash
docker compose up --build
```

The project will be accessible at the following address:

- Streamlit: [http://localhost:8501](http://localhost:8501)
- FastAPI: [http://localhost:8000](http://localhost:8000)

## Push images on Docker Hub
### Server

```bash
docker tag nlp-server:latest moiseberthe/nlp-server:latest
```

```bash
docker push moiseberthe/nlp-server:latest
```

### Client

```bash
docker tag nlp-client:latest moiseberthe/nlp-client:latest
```

```bash
docker push moiseberthe/nlp-client:latest
```