import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import csv
from csv import reader
import re

#Extracts all the query titles and deletes stopwords for semantic similarity analysis
print("Extracting Queries For NLP Preprocessing")

stop_words = set(stopwords.words('english'))

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
        #Writing the data to txt file
        f = open("Titles.txt", "a")
        f.write(title + "\n")
        f.close()
        #writing filtered queries to a new txt file
        filtered = [w for w in word_tokens if not w in stop_words] 
        print(filtered)
        f = open("filteredTitles.csv", "a")
        line = ''
        for word in filtered:
            line += word + ' '
        f.write( line +",")
        f.close()
        line = ''