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
#sql = "select * from Test4 limit 1"
sql = "select * from Training3"
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
Locindex=0
document2 = ''


#원문서에서 트위터를 사용해서 nouns만 출력, morphs도 가능, 토큰으로 만든
for row in rows:
	document1 = row['Content'].decode('utf8')

	print(row['ArticleNumber'])

	#괄호 제거
	more2=1
	while (more2 == 1):
		if document1.find('(') != -1:
			more2 = 2
			#print(punctu)
			if ( document1.find('(',document1.find('(')+1) != -1 and document1.find('(',document1.find('(')+1) < document1.find(')') ):
				document1 = document1[0:document1.find('(')] + document1[document1.find(')',document1.find(')')+1)+1:]
			else :
				document1 = document1[0:document1.find('(')] + document1[document1.find(')')+1:]
		if more2 == 2:
			more2 = 1
		else :
			more2 = 0
#	print(document1)

	#문장 끊기?
	first = document1.split('.')
	document2=''
	for ff in first:
		document2 = document2 + ' ' + ff

	split = document2.split()
	i = 0
	for word in split:
		pos = t.nouns(split[i])
		for word2 in pos:
			Compound = Compound+word2
		more =1
		while(more == 1):
			pos2 = Twitter().pos(Compound)
			for poss in pos2:
				if poss[1] != 'Noun':
					more =2
					pos3 = Twitter().nouns(Compound)
					Compound=''
					for word3 in pos3:
						Compound = Compound + word3
			if more == 2:
				more = 1
			else:
				more = 0

		tokens_ko.append(Compound)
		Compound = ''
		i = i+1
	#tokens_ko = t.nouns(document1)
	#print(type(tokens_ko))
	#print(tokens_ko)
	
	#정지단어 제거
	clean_model=[]
        #print(len(koreanStopWord))
	for word in tokens_ko:
                #print(word)
		insert = 1
		for stop in koreanStopWord:
			if word.strip() == stop.strip():
				insert = 0
				break
		if insert == 1 and word !='':
			clean_model.append(word) 
	#print(len(clean_model))
	texts.append(clean_model)
	tokens_ko=[]
#print(len(texts[0]))
#print(len(texts[1]))
#print(texts)
#찾기 위해 선언한 변수(굳이 없어도 실행가능)
#ko = nltk.Text(tokens_ko, name='document')

#토큰으로 만든 데이터를 다시 list로 변환시킨다.
# texts.append(tokens_ko)

#토큰으로 만든 데이터 list를 사전으로 형성(각 토큰마다 id를 생성) 
dictionary = corpora.Dictionary(texts)
#print(dictionary)
dictionary_path = "/home/ice-kms/LDAModel/TopicNum20_LDADic_fin_9231.dict"
corpora.Dictionary.save(dictionary, dictionary_path)


#문서-단어 행렬를 만들기 위해서 bag-of-word로 변형하는 과정(토큰화 데이터를 사용)
corpus = [dictionary.doc2bow(text) for text in texts]

#lda 모델 형성
#ldamodel = gensim.models.LdaMallet(corpus,num_topics=20,id2word=dictionary, passes=20)
ldamodel = gensim.models.ldamodel.LdaModel(corpus,num_topics=20,id2word = dictionary, passes = 200, iterations=2000)

#print(len(ldamodel))

print(ldamodel.show_topics(num_topics=20,num_words=15,formatted=False))

lda_model_path = "/home/ice-kms/LDAModel/TopicNum20_LDAModel_fin_9231.lda"
ldamodel.save(lda_model_path)

db.close()

