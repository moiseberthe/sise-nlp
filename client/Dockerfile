FROM python:3.9-slim

COPY requirements.txt /app/requirements.txt

WORKDIR /app
RUN apt-get update
RUN apt-get -y install gcc
RUN pip install -r requirements.txt

COPY . /app/

CMD ["streamlit", "run", "app.py"]