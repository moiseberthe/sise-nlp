# sise-nlp

## Make migration

Create and feed database

```bash
python app.py
```

## Run API

Move to `api` directory and run the command below
```bash
uvicorn app:app --reload
```


## Run Client

Move to `client` directory and run the command below
```bash
streamlit run app.py
```