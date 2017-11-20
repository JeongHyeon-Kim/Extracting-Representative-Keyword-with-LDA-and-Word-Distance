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
sql = "select Content from Training2"
cursor.execute(sql.encode('utf8'))

#rows =[]
array=[]

rows = cursor.fetchall()
#감사합니다 신이시여 잘하겠습니다

koreanStopWord = kolaw.open('stopword.txt').readlines()



#토큰화된 데이터를 list로 만들기위해 선언한 변수
texts =[]
ids = []

#Kolaw 필드를 사용해서 konlpy를 사용
#files_ko = kolaw.fileids()

Compound=''
tokens_ko=[]
#원문서에서 트위터를 사용해서 nouns만 출력, morphs도 가능, 토큰으로 만든
for row in rows:
	document1 = row['Content'].decode('utf8')
	split = document1.split()
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
	clean_model=[]
        #print(len(koreanStopWord))
	for word in tokens_ko:
                #print(word)
		insert = 1
		for stop in koreanStopWord:
			if word.strip() == stop.strip():
				insert = 0
				break
		if insert == 1:
			clean_model.append(word) 
	print(len(clean_model))
	texts.append(clean_model)
	tokens_ko=[]

#찾기 위해 선언한 변수(굳이 없어도 실행가능)
#ko = nltk.Text(tokens_ko, name='document')

#토큰으로 만든 데이터를 다시 list로 변환시킨다.
# texts.append(tokens_ko)

#토큰으로 만든 데이터 list를 사전으로 형성(각 토큰마다 id를 생성) 
dictionary = corpora.Dictionary(texts)
dictionary_path = "/home/ice-kms/LDAModel/TopicNum10_LDADic.dict"
corpora.Dictionary.save(dictionary, dictionary_path)


#문서-단어 행렬를 만들기 위해서 bag-of-word로 변형하는 과정(토큰화 데이터를 사용)
corpus = [dictionary.doc2bow(text) for text in texts]

#lda 모델 형성
#ldamodel = gensim.models.LdaMallet(corpus,num_topics=20,id2word=dictionary, passes=20)
ldamodel = gensim.models.ldamodel.LdaModel(corpus,num_topics=16,id2word = dictionary, passes = 200, iterations=2000)

#print(len(ldamodel))

print(ldamodel.show_topics(num_topics=20,num_words=5,formatted=False))

lda_model_path = "/home/ice-kms/LDAModel/TopicNum10_LDAModel.lda"
ldamodel.save(lda_model_path)

db.close()

