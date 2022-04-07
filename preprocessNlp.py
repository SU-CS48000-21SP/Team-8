import spacy
from spacy.tokens import DocBin

nlp = spacy.blank("en")
f = open("nlpParsed.txt", "r")

training_data = f.read()
f.close()
# the DocBin will store the example documents
db = DocBin()
for text, annotations in training_data:
    doc = nlp(text)
    ents = []
    for start, end, label in annotations:
        span = doc.char_span(start, end, label=label)
        ents.append(span)
    doc.ents = ents
    db.add(doc)
db.to_disk("./train.spacy")