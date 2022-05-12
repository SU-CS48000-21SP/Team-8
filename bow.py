import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import csv
from csv import reader
import re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from gensim.models import Word2Vec
#Extracts all the query titles and deletes stopwords for semantic similarity analysis
print("Prepare Bag of Words From Extracted Query Titles")

stop_words = set(stopwords.words('english'))
filteredArr = []
# open query dataset in read mode
with open("python_queries.csv", "r", encoding= "utf-8") as f:
    reader = csv.reader(f, delimiter=",")
    for i, line in enumerate(reader):
        #extracting query titles
        contentlist ='line[{}] = ({}'.format(i, line)
        title= contentlist.split(",")[11]

        #preparing data
        title = re.sub(r'[^\w\s]', '', title)
        title = title.lower()
        word_tokens = word_tokenize(title)

        filtered = [w for w in word_tokens if not w in stop_words] 
        filteredArr = filteredArr + filtered
       
        # to use bigrams ngram_range=(2,2)
        CountVec = CountVectorizer(ngram_range=(1,1), stop_words='english')
        #transform
        Count_data = CountVec.fit_transform(filtered)
      
        #create dataframe
        cv_dataframe=pd.DataFrame(Count_data.toarray(),columns=CountVec.get_feature_names_out())
        #print(cv_dataframe)
        tf_idf_vec_smooth = TfidfVectorizer(use_idf=True, smooth_idf=True, ngram_range=(1,1),stop_words='english')
        tf_idf_data_smooth = tf_idf_vec_smooth.fit_transform(filtered)
        tf_idf_dataframe_smooth=pd.DataFrame(tf_idf_data_smooth.toarray(),columns=tf_idf_vec_smooth.get_feature_names_out())

        model = Word2Vec(filteredArr, min_count=1)
        print(model)
        words = model.wv.index_to_key
        print(words)
    