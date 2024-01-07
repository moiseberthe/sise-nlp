import spacy
from string import punctuation

def _clean(doc: str, parser, pos_tags: list, stopwords: list):
    punctuations = list(punctuation)
    doc = "".join([char for char in list(doc) if not (char in punctuations)])
    doc = doc.lower().replace("’", "'").strip()
    # supprimer les espaces en double
    doc = " ".join(doc.split())
    doc = parser(doc)
    doc = " ".join([word.lemma_ for word in doc if not (word.pos_ in pos_tags or word.lemma_ in stopwords or word.is_digit or len(word) <= 2)])
    return doc

def clean_corpus(corpus, pos_tags=[], stopwords=[]):
    parser = spacy.load("fr_core_news_lg")
    return [_clean(doc, parser, pos_tags, stopwords) for doc in corpus]