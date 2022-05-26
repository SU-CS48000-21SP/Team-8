import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import csv
from csv import reader
import re

#Extracts all the query titles and deletes stopwords for semantic similarity analysis

def preProcessFile(inputFile, filteredFile):
    stop_words = set(stopwords.words('english'))
    add_stopword = ['python', 'how', 'to', 'show', 'shows', 'showing']
    # open query dataset in read mode
    # with open("StackOverflow_Python_Scraping\python_queries.csv", "r", encoding= "utf-8") as f:
    with open(inputFile, "r", encoding= "utf-8") as f:
        reader = csv.reader(f, delimiter=",")
        for i, line in enumerate(reader):
            #extracting query titles
            contentlist ='line[{}] = ({}'.format(i, line)
            title= contentlist.split(",")[11]

            #preparing data
            title = re.sub(r'[^\w\s]', '', title)
            title = title.lower()
            word_tokens = word_tokenize(title)
           
            #writing filtered queries to a new txt file
            filtered = [w for w in word_tokens if not (( w in stop_words) or ( w in add_stopword))] 
            #print(filtered)
            #f = open("filteredNew.csv", "a")
            f = open(filteredFile, "a")
            line = ''
            for word in filtered:
                line += word + ' '
            f.write( line +",")
            f.close()
            line = ''

print("Extracting Queries For NLP Preprocessing")
preProcessFile("StackOverflow_Python_Scraping\python_queries.csv", "filteredDeneme.csv")
