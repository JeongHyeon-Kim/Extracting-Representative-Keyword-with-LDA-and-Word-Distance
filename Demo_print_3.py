from collections import Counter
from konlpy.tag import Twitter; t = Twitter()
from konlpy.corpus import kolaw
from types import *
import gensim
from gensim.models import LdaModel
from gensim import corpora,models
import MySQLdb
import operator
import decimal
db = MySQLdb.connect(host="localhost", user ="ice-kms", passwd="kkms1234", db="scraping", charset='utf8')

cursor = db.cursor(MySQLdb.cursors.DictCursor)
cursor2 = db.cursor(MySQLdb.cursors.DictCursor)
cursor3 = db.cursor(MySQLdb.cursors.DictCursor)
cursor4 = db.cursor(MySQLdb.cursors.DictCursor)
cursor5 = db.cursor(MySQLdb.cursors.DictCursor)
cursor6 = db.cursor(MySQLdb.cursors.DictCursor)
cursor7 = db.cursor(MySQLdb.cursors.DictCursor)
cursor8 = db.cursor(MySQLdb.cursors.DictCursor)
cursor9 = db.cursor(MySQLdb.cursors.DictCursor)
cursor10 = db.cursor(MySQLdb.cursors.DictCursor)
cursor11 = db.cursor(MySQLdb.cursors.DictCursor)
cursor12 = db.cursor(MySQLdb.cursors.DictCursor)
cursor13 = db.cursor(MySQLdb.cursors.DictCursor)

cursor.execute("set names utf8")
cursor2.execute("set names utf8")
cursor3.execute("set names utf8")
cursor4.execute("set names utf8")
cursor5.execute("set names utf8")
cursor6.execute("set names utf8")
cursor7.execute("set names utf8")
cursor8.execute("set names utf8")
cursor9.execute("set names utf8")
cursor10.execute("set names utf8")
cursor11.execute("set names utf8")
cursor12.execute("set names utf8")
cursor13.execute("set names utf8")

db.query("set character_set_connection=utf8;")
db.query("set character_set_server=utf8;")
db.query("set character_set_client=utf8;")
db.query("set character_set_results=utf8;")
db.query("set character_set_database=utf8;")

cursor.execute("set names utf8")

sql = "select * from Demo order by Number desc limit 1"

cursor.execute(sql.encode('utf8'))

rows = cursor.fetchall()
document = ''

koreanStopWord = kolaw.open('stopword.txt').readlines()

out = ''
document=''
lenght=0
tokens_ko=[]
Compound=''
maxprobability =0
LDAkeyword=[]
wd=[]
wd2=[]
wd3=[]
sen=[]
final=[]
frequency=[]
freword=[]
Tagging=[]
Tagword=[]
LDAscore=[]
LDAscoree=0
modelscore=0
jh_model=[]
allLdaScore = 0
allModelScore = 0
allfreScore=0
frescore=0
exceptcount=0
location1={}
location2={}
location3={}
location4={}
location5={}
wordscore={}
ldasscore=0
allword=[]
modelsscore=0
freqsscore=0
sentencenumber=[]
senNumber=[]
senword=[]
firstsen=[]
remainsen=[]
checksen=[]
sortsco=[]
Taggingarray=[]
User=['User3', 'User5', 'User6']
delTag=[]
compoundTag=''
RealTag=[]
tagcheck=0
alltagcount=0

for row in rows:

	# 사전 불러오고 Lda 모델 불러오기
	lda_model_path = "/home/ice-kms/LDAModel/TopicNum16_LDAModel_fin_9231.lda"
	lda = LdaModel.load(lda_model_path)

	dictionary_path= "/home/ice-kms/LDAModel/TopicNum16_LDADic_fin_9231.dict"
	dictionary = corpora.Dictionary.load(dictionary_path)

	document = row['Content'].decode('utf8')

	more2 =1
	while (more2 == 1):
		if document.find('(') != -1:
			more2 = 2
			#print(punc
			if ( document.find('(',document.find('(')+1) != -1 and document.find('(',document.find('(')+1) < document.find(')') ):
				document = document[0:document.find('(')] + document[document.find(')',document.find(')')+1)+1:]
			else :
				document = document[0:document.find('(')] + document[document.find(')')+1:]
		if more2 == 2:
			more2 = 1
		else :
			more2 = 0

	first = document.split('.')
	document2=''
	for ff in first:
		document2 = document2 + ' ' + ff

	# 공백 단위로 자르기
	split = document.split()
	i = 0
	# 자르고 난 후에 같은 위치에 명사 합치기
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
				more =1
			else :
				more =0
		tokens_ko.append(Compound)
		Compound = ''
		i = i+1
	# split 초기화 및 정지단어를 제거하기 위해 새로운 clean 배열 생성
	split=[]
	clean_model=[]

	# 정지-단어 제거
	for word in tokens_ko:
		insert = 1
		for stop in koreanStopWord:
			if word.strip() == stop.strip():
				insert = 0
				break
		if insert == 1 and word !='':
			clean_model.append(word)

	# 위의 clean_model 배열을 바탕으로 사전 생성( 이문서에서의)
	dicko = dictionary.doc2bow(clean_model)
	# document Topic 분포를 확인하기 위한 부분
	documentTopic = lda[dicko]
#	print(documentTopic)

	# 가장 높은 문서-토픽 확률을 가지는 토픽을 가져온다.
	for Topic in documentTopic:
		if Topic[1]>maxprobability:
			maxprobability = Topic[1]
			maxTopicnum = Topic[0]

	ldashow = lda.show_topics(num_topics=16,num_words=20, formatted=False)
#	print(ldashow)
	#초기화 부분	
	dicko = []
	clean_model=[]
	documentTopic = []
	maxprobability= 0
	tokens_ko=[]
	LDAkeyword = []

#	for word in ldashow[maxTopicnum][1]:
#		print(word[1])
	#가장 확률 높은 문서-토픽 분포에서 단어 열개를 LDAKeyword에 넣어준다.
	for word in ldashow[maxTopicnum][1]:
		LDAkeyword.append(word[0])
		print(word[1])
	
	maxTopicnum = 0
	print(row['Number'])

	# 모든 글자를 dict형태로 구성
	sql6 = "select Word from WordDistance2 where Articlenumber = %s" % (row['Number'])
	cursor6.execute(sql6)
	allword = cursor6.fetchall()
	for allwd in allword:
		wordscore[allwd['Word']] = 0

	# 문장의 개수 받아오기
	sql7 = "select Sentence from WordDistance2 where Articlenumber = %s group by Sentence" % (row['Number'])
	cursor7.execute(sql7)
	sentencenumber = cursor7.fetchall()
	for senN in sentencenumber:
		senNumber.append(senN['Sentence'])
#	print(senNumber)

#	print(wordscore)
#	print(LDAkeyword)

	checksss = 0
	for sen in senNumber:
		#wordW = 0.145
		for word in LDAkeyword:
			#print(wordW)
			#if wordW == 0.0:
			#	break

			sql8="select Loc_in_sen from WordDistance2 where Articlenumber=%s and Sentence=%s and Word=%s";
			cursor8.execute(sql8,(row['Number'],sen,word))
			senword = cursor8.fetchall()
			#checksen = cursor8.fetchone()
			#print(type(checksen['Loc_in_sen']))
			#if senword is None:
			#	print("why")
			if sen == 1 :
				checksss = checksss + len(senword)
			if sen >1 and checksss == 0:
				for word in LDAkeyword:
#					print("재검색")
					sql8="select Loc_in_sen from WordDistance2 where Articlenumber=%s and Sentence=%s and Word like %s";
					cursor8.execute(sql8,(row['Number'],1,'%'+word+'%'))
					senword = cursor8.fetchall()

					for locsen in senword:
						sql9="select Word, 0.9*(1/log(abs(Loc_in_sen-%s)+1)) as value from (select * from WordDistance2 where Sentence=%s and Articlenumber=%s) as B where Loc_in_sen != %s ";
						cursor9.execute(sql9,(locsen['Loc_in_sen'],1,row['Number'],locsen['Loc_in_sen']))
						firstsen = cursor9.fetchall()
#                                       print("현재문장 번호:1")
                                        #print(firstsen)
						for fs in firstsen:
                                                #print(fs['Word'])
							wordscore[fs['Word']] = wordscore[fs['Word']]+ decimal.Decimal(fs['value'])
#                                       print(wordscore)
				checksss = 1

			for locsen in senword:
				
#				print("현재 단어 가중치")
#				print(wordW)

				if sen == 1:
					sql9="select Word, 0.9*(1/log(abs(Loc_in_sen-%s)+1)) as value from (select * from WordDistance2 where Sentence=%s and Articlenumber=%s) as B where Loc_in_sen != %s ";
					cursor9.execute(sql9,(locsen['Loc_in_sen'],sen,row['Number'],locsen['Loc_in_sen']))
					firstsen = cursor9.fetchall()
#					print("현재문장 번호:1")
					#print(firstsen)
					for fs in firstsen:
						#print(fs['Word'])
						wordscore[fs['Word']] = wordscore[fs['Word']]+ decimal.Decimal(fs['value'])
#					print(wordscore)

				else :
					sql10="select Word, 0.1*(1/log(abs(Loc_in_sen-%s)+1)) as value from (select * from WordDistance2 where Sentence=%s and Articlenumber=%s) as B where Loc_in_sen !=%s";
					cursor10.execute(sql10,(locsen['Loc_in_sen'],sen,row['Number'],locsen['Loc_in_sen']))
					remainsen = cursor10.fetchall()
					#print("현재문장번호:")
					#print(sen)
					#print("찾은 단어 위치")
					#print(locsen['Loc_in_sen'])
					#print(sen)
					#print(remainsen)
					for rs in remainsen:
						wordscore[rs['Word']] = wordscore[rs['Word']]+ decimal.Decimal(rs['value'])

	wordscore['대통령'] = 0
	wordscore['박근혜'] = 0
	wordscore['후보'] = 0
	wordscore['대선'] = 0
	wordscore['대표'] = 0
	wordscore['국민'] = 0
	wordscore['민주당'] = 0
	wordscore['자유한국'] = 0
	wordscore['의원'] = 0
	wordscore['정부']=0
	wordscore['총']=0

	sortsco = sorted(wordscore.items(), key=operator.itemgetter(1),reverse=True)
	print(sortsco[0][1])
	print(sortsco[1][1])
	print(sortsco[2][1])
	print(sortsco[3][1])
	print(sortsco[4][1])

	sql5 = "select Word, count(*) as cnt from WordDistance2 where ArticleNumber= %s group by Word order by cnt desc limit 5" % (row['Number']) 
	cursor5.execute(sql5)
	frequency = cursor5.fetchall()

	for frewo in frequency:
		freword.append(frewo['Word'])

	try :
		LDAscore.append(LDAkeyword[0])
		LDAscore.append(LDAkeyword[1])
		LDAscore.append(LDAkeyword[2])
		LDAscore.append(LDAkeyword[3])
		LDAscore.append(LDAkeyword[4])

		jh_model.append(sortsco[0][0])
		jh_model.append(sortsco[1][0])
		jh_model.append(sortsco[2][0])
		jh_model.append(sortsco[3][0])
		jh_model.append(sortsco[4][0])

		cursor11.execute("insert into LDAtest (ArticleNumber,Word1,Word2,Word3,Word4,Word5) values(%s,%s,%s,%s,%s,%s)",(row['Number'],LDAscore[0],LDAscore[1],LDAscore[2],LDAscore[3],LDAscore[4]))
		db.commit()
		cursor12.execute("insert into Modeltest (ArticleNumber,Word1,Word2,Word3,Word4,Word5) values(%s,%s,%s,%s,%s,%s)",(row['Number'],jh_model[0],jh_model[1],jh_model[2],jh_model[3],jh_model[4]))
		db.commit()

	except:
		exceptcount=exceptcount+1
	Tagword = []
	Tagging = []
	LDAscore = []
	LDAkeyword = []
	jh_model = []
	final = []
	frequency=[]
	freword=[]
	LDAscoree = 0
	modelscore = 0
	frescore=0
	sentencenumber=[]
	senNumber=[]
	senword=[]
	firstsen=[]
	remainsen=[]
	checksen=[]	
	sortsco=[]
	allword=[]
	wordscore={}
	RealTag=[]

