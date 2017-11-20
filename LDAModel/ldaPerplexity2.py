#-*- coding: utf-8 -*-

#라이브러리 추가
from konlpy.corpus import kolaw
from konlpy.tag import Twitter; t = Twitter()
import nltk
import gensim
from gensim import corpora, models
#from gensim import LdaMallet
import MySQLdb
from jpype import *
import codecs
from gensim.models import LdaModel
import numpy
from gensim import corpora,models
import random

# db 연결하고 인코딩 부분
db = MySQLdb.connect(host="localhost", user ="ice-kms", passwd="kkms1234", db="scraping", charset='utf8')

cursor = db.cursor(MySQLdb.cursors.DictCursor)
cursor.execute("set names utf8")

db.query("set character_set_connection=utf8;")
db.query("set character_set_server=utf8;")
db.query("set character_set_client=utf8;")
db.query("set character_set_results=utf8;")
db.query("set character_set_database=utf8;")

cursor.execute("set names utf8")
sql = "select Content from Text3 where ArticleNumber <= 10000"
cursor.execute(sql.encode('utf8'))

#rows =[]
array=[]

rows = cursor.fetchall()
#감사합니다 신이시여 잘하겠습니다

for row in rows:
	array.append(row['Content'].decode('utf8'))

#print(array)

koreanStopWord = kolaw.open('stopword.txt').read()

#토큰화된 데이터를 list로 만들기위해 선언한 변수
texts =[]
ids = []

#Kolaw 필드를 사용해서 konlpy를 사용
#files_ko = kolaw.fileids()
ldatest=[]

Compound=''
tokens_ko=[]
#원문서에서 트위터를 사용해서 nouns만 출력, morphs도 가능, 토큰으로 만든

for row in array:
	#document1 = row['Content'].decode('utf8')
	#print(row)
	split = row.split()
	i = 0
	for word in split:
		pos = t.nouns(split[i])
		for word2 in pos:
			Compound = Compound+word2
		tokens_ko.append(Compound)
		Compound = ''
		i = i+1
	#tokens_ko = t.nouns(document1)
	#print(type(tokens_ko))
	#print(tokens_ko)
	split=[]
	docRemovingStopWord = [i for i in tokens_ko if not i in koreanStopWord] 
	texts.append(docRemovingStopWord)
	tokens_ko=[]

#찾기 위해 선언한 변수(굳이 없어도 실행가능)
#ko = nltk.Text(tokens_ko, name='document')
print("다 넣음")
#토큰으로 만든 데이터를 다시 list로 변환시킨다.
# texts.append(tokens_ko)

#토큰으로 만든 데이터 list를 사전으로 형성(각 토큰마다 id를 생성) 
dictionary = corpora.Dictionary(texts)
#dictionary_path = "/home/ice-kms/LDAModel/iter_1000_Real_articleDic_10000_compound_topicNum_20.dict"
#corpora.Dictionary.save(dictionary, dictionary_path)
#dictionary2 = corpora.Dictionary(ldatest)

#문서-단어 행렬를 만들기 위해서 bag-of-word로 변형하는 과정(토큰화 데이터를 사용)
corpus = [dictionary.doc2bow(text) for text in texts]
#corpus2 = [dictionary2.doc2bow(ltest) for ltest in ldatest]

#print(type(corpus))
random.shuffle(corpus)
p = int(len(corpus)* 0.8)
rows_train = corpus[0:p]
rows_test = corpus[p:]

print(len(rows_train))
print(len(rows_test))

Topic_list=[10,15,20,30,50,100]

output_file = open('LDA-Perplexity.txt', 'w')

to = "Topic"
pe = "Perplex"
wpp ="Per-word Perplexity: "
writee=''

for topic in Topic_list:
	ldamodel = gensim.models.ldamodel.LdaModel(rows_train,num_topics=topic,id2word = dictionary, passes = 100,iterations=1000)

	perplex = ldamodel.bound(rows_test)
	#topicnum = to+str(topic)
	print("Topic")
	print(topic)
	#output_file.write(topicnum)
	print("Perplex")
	print(perplex)

	print("Per-word Perplexity: ")
	#print(sum(cnt for document in corpus for _, cnt in document))
	word_perplex = numpy.exp2(-perplex / sum(cnt for document in rows_test for _, cnt in document))
	print(word_perplex)
	writee = to+str(topic)+"\n"+pe+str(perplex)+"\n"+wpp+str(word_perplex)+"\n"
	output_file.write(writee)

#lda_model_path = "/home/ice-kms/LDAModel/iter_1000_Real_lda_10000_pass_100_topicNum_20.lda"
#ldamodel.save(lda_model_path)
output_file.close()
db.close()

