import spacy

nlp = spacy.load('en_core_web_md')
token = lambda word: nlp(word)[0]  # shortcut to convert string to spacy.Token
score_words = lambda w1, w2: token(w1).similarity(token(w2))

print(score_words("nested", "in"))   # 0.1854
print(score_words("array", "list"))  # 0.3288
print(score_words("join", "merge"))  # 0.3276
print(score_words("shell", "terminal"))   # 0.3048
print(score_words("subclass", "inheritance"))  # 0.3655
print(score_words("parse", "transform")) #0.3127
print(score_words("sorting", "order")) #0.2881
print(score_words("combination", "shuffle")) #0.1702