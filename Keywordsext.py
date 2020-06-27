import Preprocesstowords as mp, NormalizeStemLemmatize as mn
from nltk.stem import LancasterStemmer, WordNetLemmatizer
import pandas
from sklearn.feature_extraction.text import CountVectorizer
import re
#Gensim
import gensim
import gensim.corpora as corpora

import logging
import warnings

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)


warnings.filterwarnings("ignore", category=DeprecationWarning)


def stem_words(words):
    """Stem words in list of tokenized words"""
    stemmer = LancasterStemmer()
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems


def lemmatize_verbs(words):
    """Lemmatize verbs in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas.append(lemma)
    return lemmas


class Keywordsext:

    def __init__(self, url):

        self.url = url

    def stem_and_lemmatize(self, words):
        stems = stem_words(words)
        lemmas = lemmatize_verbs(words)
        return stems, lemmas

    def keywords(self):
        pw = mp.Preprocesstowords(self.url)
        pwwords = pw.textpreprocessor()
        nsl = mn.NormalizeStemLemmatize(pwwords)
        nslwords = nsl.normalize()
        stems, lemmas = self.stem_and_lemmatize(nslwords)

        for st in stems:
            if len(st) == 1:
                stems.remove(st)
        for le in lemmas:
            if len(le) == 1 or len(le) == 2:
                lemmas.remove(le)

        return lemmas


class Nlpapp(Keywordsext):

    def __init__(self, urls):
        self.urls = urls

    def topwords(self):

        stops = []
        f = open("stopwords.txt", "r")
        for x in f:
            stops.append(x.strip("\n"))

        f.close()

        dictlemma = []

        for url in self.urls:
            ob = Keywordsext(url)
            lemma = ob.keywords()
            for l in lemma:
                if l in stops:
                    lemma.remove(l)
            dictlemma.append(lemma)




        keyslist = []

        #for 1 word keywords
        
         # Create Dictionary
        id2word = corpora.Dictionary(dictlemma)

        # Create Corpus
        texts = dictlemma

        # Term Document Frequency
        corpus = [id2word.doc2bow(text) for text in texts]

        # Build LDA model
        lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=10, random_state=100, update_every=1, chunksize=100, passes=10, alpha='auto', per_word_topics=True)

        
        listoflist = lda_model.print_topics()
        
        lookuplist = listoflist[0:1]

        for item in lookuplist:

            itemstr = str(item[1])
            itemstr = itemstr.strip(''',''')
            itemstr = itemstr.strip('''"''')
            keys = re.findall('''"(.*?)\"''', itemstr)
            for k in keys:
                if k not in keyslist:
                    keyslist.append(k)
        

        indexcorp = 0
        corp_updated = [None] * len(dictlemma)

        # Most frequently occuring Bi-grams
        for lemitem in dictlemma:
            corp_updated[indexcorp] = " "
            for stringtext in lemitem:
                corp_updated[indexcorp] = corp_updated[indexcorp] + " " + stringtext
            corp_updated[indexcorp].strip("  ")
            indexcorp += 1

        for bitri in range(2, 4):

            vec1 = CountVectorizer(ngram_range=(bitri, bitri),
                                   max_features=2000).fit(corp_updated)
            bag_of_words = vec1.transform(corp_updated)
            sum_words = bag_of_words.sum(axis=0)
            words_freq = [(word, sum_words[0, idx]) for word, idx in
                          vec1.vocabulary_.items()]
            words_freq = sorted(words_freq, key=lambda x: x[1],
                                reverse=True)
            topg_df = pandas.DataFrame(words_freq[:5])

            topg_df.columns = ["gram", "Freq"]

            keyslist.append((topg_df["gram"].tolist()))

        return keyslist
