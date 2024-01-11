

# / return df (ville, size, latitude, longitude) dataframe grouper par ville sur le nombre d'annonce
# / return df (toute la base)
# / return corpus nettoyé. (get)
# / return n best document qui matche un text (get)
# / return n best document qui matche avec un CV (get)
# / clustering ????
# / get sentiment analysis from text
# / complete text 



from sklearn.cluster import KMeans
from nltk.corpus import stopwords
from nltk.stem.snowball import FrenchStemmer
from string import punctuation
import re
import spacy 
from transformers import pipeline, AutoTokenizer
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from gensim.models import Word2Vec
import gensim 
from gensim import corpora
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB, ComplementNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import jaccard
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import seaborn as sn
import urllib
import textract
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pickle
from random import randint
import os

try:
    nlp= spacy.load("fr_core_news_sm")
except:
    spacy.cli.download("fr_core_news_sm")
    nlp= spacy.load("fr_core_news_sm")

class Nettoyage:
    
    def __init__(self, algo="spacy", similarity="cosine", cleaned=False, contents=[], tags=[], ids=[], urls=[]) -> None:
        '''
         algo: spacy or nltk (pour le nettoyage)
         similarity: cosine or jaccard (pour la similarité entre documents)
         cleaned: boolean (si vrai on initialize les object deja nettoyer... sinon on refait le nettoyage et on recrée les objects)
         contents: liste des textes du corpus (raw data)
         tags: si existent, constituent les tags de chaque document
         ids: ids de chaque document
         urls: lien de chaque offre
        '''
        self.algo=algo
        self.similarity= similarity
        #get dataframe (2 colonnes 1 avec le texte et l'autre avec les étiquettes)
        self.tags=tags
        self.ids= ids
        self.urls= urls
        #raw sentences list
        self.contents= contents
        #score
        self.scores= {"accuracy":[], "precision":[], "rappel":[]}
        if cleaned:
            #tf idf vectorizer object
            self.tfidfvect= pickle.load(open("./utils/files/tfidfvect.pkl", "rb"))
            #list of cleaned sentences
            self.sentences= pickle.load(open("./utils/files/sentences.pkl", "rb"))
            #kmeans object
            self.kmeans= None
        else:
            self._clean_all()
            self.tfidfvect= TfidfVectorizer()
            self.tfidfvect.fit(self.sentences)
            self.kmeans= None

    def getSentences(self):
        return self.sentences

    def _clean_sent_spacy(self, sentence):
        sent= sentence.lower()
        sent= sent.replace("’", " ")
        doc= nlp(sent)
        stw = set([*stopwords.words('french'), "être"])
        tab= [mot.lemma_ for mot in doc if not (mot.is_punct or mot.is_space or mot.is_stop or mot.like_url or len(mot)<=2 or mot.is_digit or mot in stw)]
        return " ".join(tab)
    
    def _clean_sent_nltk(self, sentence):
        sent= sentence.lower()
        sent= sent.replace("’", " ")
        compiler= re.compile("[%s]"%re.escape(punctuation))
        sent =  compiler.sub(" ", sent)
        french_stopwords = set([*stopwords.words('french'), "être"])
        sp_pattern = re.compile( """[\.\!\"\s\?\-\,\'\d+]+""", re.M).split
        # add these to cleaning
        tokens= sp_pattern(sent)
        filtre_stopfr =  [token for token in tokens if token not in french_stopwords]
        stemmer = FrenchStemmer()
        stemming= " ".join([stemmer.stem(w) for w in filtre_stopfr if len(stemmer.stem(w))>2])        
        return stemming
    
    def _clean_all(self):
        if self.algo=="spacy":
            self.sentences= [self._clean_sent_spacy(content) for content in self.contents]
        else:
            self.sentences= [self._clean_sent_nltk(content) for content in self.contents]
            #self.tags.append()

    def tfidf_text_similarity(self, text):
        # prepare text
        if self.algo=="spacy":
            prep = self._clean_sent_spacy(text)
        else:
            prep = self._clean_sent_nltk(text)
        # Create the TF-IDF vectors
        vector1= self.tfidfvect.transform(self.sentences)
        vector2 = self.tfidfvect.transform([prep])
        # Calculate the cosine similarity
        if self.similarity=='cosine':
            similarity = cosine_similarity(vector1, vector2)
            idx= np.argsort(similarity[:, 0])[::-1]
        elif self.similarity=="jaccard":
            similarity= np.array([jaccard(vect, vector2.toarray()[0]) for vect in vector1.toarray()])
            idx= np.argsort(similarity)[::-1]
        return idx
    
    #retourne les n meilleurs documents ou les n meilleurs ids
    def return_n_best_doc(self, n=10, text="", to_return="id"):
        '''
         n => int : the limit of documents/ids to return
         text => str : the text to match
         to_return => str : if id must return ids, url:urls or document:description
        '''
        idx= self.tfidf_text_similarity(text=text)
        if to_return=="id":
            res= np.array(self.ids)[idx]
        elif to_return=="url":
            res= np.array(self.urls)[idx]
        else:
            res= np.array(self.contents)[idx]
        return res[:n]
    
    #composants ??? 
    def topic_modeling(self):
        dictionnary= corpora.Dictionary([x.split() for x in self.sentences])
        doc_tm=[dictionnary.doc2bow(doc.split()) for doc in self.sentences]
        Lda= gensim.models.ldamodel.LdaModel
        ldamodel= Lda(doc_tm, num_topics=3, id2word=dictionnary, passes= 50)
        tops= ldamodel.print_topics(num_topics=3, num_words=3)
        return tops

    def display_word_cloud(self):
        wordcloud = WordCloud().generate(" ".join(self.sentences))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()

    def save_objects(self):
        if len(self.sentences) > 0:
            pickle.dump(self.sentences, open("./utils/files/sentences.pkl", "wb"))
        if self.tfidfvect is not None:
            pickle.dump(self.tfidfvect, open("./utils/files/tfidfvect.pkl", "wb"))

    def sentiment_analysis(self, text):
        mod= "cmarkea/distilcamembert-base-sentiment"
        classifier = pipeline('sentiment-analysis', model=mod, tokenizer=mod)
        resp= classifier(text)
        score={"1 star":"red", "2 stars":"tomato", "3 stars":"yellow", "4 stars":"white", "5 stars": "green"}
        return score[resp[0]["label"]]
    
    def complete_sentence(self, text):
        tokenizer = AutoTokenizer.from_pretrained("camembert-base")
        pipe = pipeline("fill-mask", model="camembert-base", tokenizer=tokenizer)
        if "<mask>" not in text:
            text+= " <mask>"
        resp= [(x["score"], x["token_str"]) for x in pipe(text)][:5]
        return resp
    
    def match_cv(self, file, best=10, to_return="id"):
        '''
         file: url of cv file
         best: top match jobs corresponding
        '''
        #get extension of the file
        ext= file.split(".")[-1]
        #give name to cv
        name= "cv"+str(randint(0, 1000))+"."+ext
        #get cv locally
        res= urllib.request.urlretrieve(file, name)
        #retrieve information
        text = textract.process(name).decode()
        res= self.return_n_best_doc(n=best, text=text, to_return=to_return)
        #delete file
        if os.path.exists(name):
            os.remove(name)
        return res
    
    def match_cv_v2(self, chemin_fichier, best=10, to_return="id"):
        '''
         chemin_fichier: chemin local du cv 
         best: top match jobs corresponding
        '''
        #retrieve information
        text = textract.process(chemin_fichier).decode()
        res= self.return_n_best_doc(n=best, text=text, to_return=to_return)
        #delete file
        if os.path.exists(chemin_fichier):
            os.remove(chemin_fichier)
        return res
    
    def clustering(self, n_clusters=10):
        vector1= self.tfidfvect.transform(self.sentences)
        self.kmeans= KMeans(n_clusters=n_clusters, random_state=42, max_iter=100, n_init="auto")
        self.kmeans.fit(vector1)
        return self.kmeans.labels_
    
    def cluster_predict(self, text):
        if self.kmeans is None:
            print("please call clustering method first!!!")
            return -1
        # prepare text
        if self.algo=="spacy":
            prep = self._clean_sent_spacy(text)
        else:
            prep = self._clean_sent_nltk(text)
        # Create the TF-IDF vectors
        vector2 = self.tfidfvect.transform([prep])
        clust= self.kmeans.predict(vector2)
        return clust
    
    #plot document dispersion with tsne reduction + kmeans group (10)
    def tsne_reduc(self, n_comp=2):
        vector1= self.tfidfvect.transform(self.sentences)
        X = vector1.toarray()
        embeddings = TSNE(n_components=n_comp, random_state=42)
        Y = embeddings.fit_transform(X)
        # sn.scatterplot(x= Y[:, 0], y= Y[:, 1], hue=self.clustering())
        # for i in range(len(self.sentences)):
        #     plt.text(x= Y[i, 0], y= Y[i, 1], s=i)
        # plt.show()
        return Y


