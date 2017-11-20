from konlpy.tag import Twitter; t = Twitter()
import nltk
import gensim
from gensim.models import LdaModel
from gensim import corpora,models
import nltk

lda_model_path = "/home/ice-kms/LDAModel/lda_20_topic_10000.lda"
lda = LdaModel.load(lda_model_path)

dictionary_path= "/home/ice-kms/LDAModel/articleDic_10000.dict"
dictionary = corpora.Dictionary.load(dictionary_path)

document = "박근혜 정부는 헌재에서 탄핵이 인용됨에 따라 곧 이어"
tokens_ko = t.nouns(document)
dicko = dictionary.doc2bow(tokens_ko)
similarity = lda[dicko]


print(lda.show_topics(num_topics=20,num_words=5,formatted=False))
print(similarity)

#print(lda.print_topics(20))

#print(lda.get_document_topics(dicko))
