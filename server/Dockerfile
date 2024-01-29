FROM python:3.9-slim

COPY requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app/

RUN python -m nltk.downloader stopwords
RUN python -m spacy download fr_core_news_sm

CMD ["uvicorn", "--host", "0.0.0.0", "app:app"]