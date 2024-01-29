# Docker project with Streamlit, FastAPI and SQLite


This project is part of a course in Text Mining, an exciting discipline that explores text analysis techniques for extracting meaningful information. Carried out in a school context, this project aims to apply the concepts and methodologies learned in class to a concrete application.<br>
<!-- This project is a demonstration of using Docker Compose to run a `Python` application consisting of `Streamlit`, `FastAPI`, and `SQLite` in `Docker` containers. -->
<br>

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
  - controller/
  - pages/
  - app.py
  - Dockerfile
  - env.sample.py
  - requirements.txt
- `server/`: Application FastAPI
  - database/
  - utils/
  - app.py
  - Dockerfile
  - env.sample.py
  - migrate.py
  - requirements.txt

## Environment configuration

Before running the application, you need to create two env.py files, one in the `server/` directory and another in the `client/` directory. You can take inspiration from the available example files.<br>

For the client :
```bash
cp client/env.sample.py client/env.py 
```

For the server :
```bash
cp server/env.sample.py server/env.py 
```
<br>
You need to have credentials to access the Pôle Emploi API, which is used in this project to retrieve job offers. Visit [https://pole-emploi.io](pole-emploi.io) to obtain these credentials.<br>

*This is optional, but you will only have access to job offers available on Apec.*

## Docker setup
The Docker files (`client/Dockerfile` and `server/Dockerfile`) contain the build configurations for the Streamlit and FastAPI services.<br>

The `docker-compose.yml` file is designed to orchestrate the different services.

### Build and run containers

To build and start the services using Docker Compose, you can use the following command:
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