import spacy
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from statistics import mean 

import string

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import stop_words
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

#Plotting Libraries
import matplotlib.pyplot as plt
import seaborn as sns

# nlp = spacy.load('en_core_web_md')
# token = lambda word: nlp(word)[0]  # shortcut to convert string to spacy.Token
# score_words = lambda w1, w2: token(w1).similarity(token(w2))

# print(score_words("nested", "in"))   # 0.1854
# print(score_words("array", "list"))  # 0.3288
# print(score_words("join", "merge"))  # 0.3276
# print(score_words("shell", "terminal"))   # 0.3048
# print(score_words("subclass", "inheritance"))  # 0.3655
# print(score_words("parse", "transform")) #0.3127
# print(score_words("sorting", "order")) #0.2881
# print(score_words("combination", "shuffle")) #0.1702

vect = CountVectorizer(max_features= 5000, preprocessor=clean)
X_train_dtm = vect.fit_transform(X_train)
X_val_dtm = vect.transform(X_val)

print(X_train_dtm.shape, X_val_dtm.shape)