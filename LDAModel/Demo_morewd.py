from collections import Counter
from konlpy.tag import Twitter; t = Twitter()
from konlpy.corpus import kolaw
from types import *
import gensim
from gensim.models import LdaModel
from gensim import corpora,models
import MySQLdb
db = MySQLdb.connect(host="localhost", user ="ice-kms", passwd="kkms1234", db="scraping", charset='utf8')

cursor = db.cursor(MySQLdb.cursors.DictCursor)
cursor2 = db.cursor(MySQLdb.cursors.DictCursor)
cursor3 = db.cursor(MySQLdb.cursors.DictCursor)
cursor4 = db.cursor(MySQLdb.cursors.DictCursor)
cursor5 = db.cursor(MySQLdb.cursors.DictCursor)

cursor.execute("set names utf8")
cursor2.execute("set names utf8")
cursor3.execute("set names utf8")
cursor4.execute("set names utf8")
cursor5.execute("set names utf8")

db.query("set character_set_connection=utf8;")
db.query("set character_set_server=utf8;")
db.query("set character_set_client=utf8;")
db.query("set character_set_results=utf8;")
db.query("set character_set_database=utf8;")

sql = "select * from Test3 limit 100"
cursor.execute(sql.encode('utf8'))

rows = cursor.fetchall()
document = ''

koreanStopWord = kolaw.open('stopword.txt').readlines()


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
except_count=0
location=[]
check=0
ldwcount=0
ldasscore=0
modelsscore=0
freqsscore=0

for row in rows:
	#확인을 위해 문서에 LDA를 사용하게 되면 그 데이터가 학습이 되므로 매번 새로이 모델과 사전을 부른다.
	lda_model_path = "/home/ice-kms/LDAModel/TopicNum16_LDAModel.lda"
	lda = LdaModel.load(lda_model_path)

	dictionary_path= "/home/ice-kms/LDAModel/TopicNum16_LDADic.dict"
	dictionary = corpora.Dictionary.load(dictionary_path)

	#기사의 내용을 하나 가져온다.
	document = row['Content'].decode('utf8')

	#띄어쓰기되지 않은 명사 복원
	split = document.split()
	i = 0
	for word in split:
		pos = t.nouns(split[i])
		for word2 in pos:
			Compound = Compound+word2
		tokens_ko.append(Compound)
		Compound = ''
		i = i+1
	split=[]

	#정지단어 제거
	clean_model=[]
	for word in tokens_ko:
		insert = 1
		for stop in koreanStopWord:
			if word.strip() == stop.strip():
				insert = 0
				break
		if insert == 1:
			clean_model.append(word)
	tokens_ko=[] #문서 늘어나는 것을 방지하기 위해 초기화

	dicko = dictionary.doc2bow(clean_model)
	documentTopic = lda[dicko]


	maxprobability = 0
	for Topic in documentTopic:
		if Topic[1]>maxprobability:
			maxprobability = Topic[1]
			maxTopicnum = Topic[0]

	ldashow = lda.show_topics(num_topics=20, num_words=10, formatted=False)	

	documentTopic = []
	maxprobability= 0
	LDAkeyword = []

	for word in ldashow[maxTopicnum][1]:
		LDAkeyword.append(word[0])
	

	maxTopicnum = 0
	print("기사번호")
	print(row['ArticleNumber'])

	#LDA에서 뽑아낸 주제어를 토대로 단어거리 모델에서 문장과 문장의 위치 가져오기
	for word in LDAkeyword:
		sql2 = "select Sentence, Loc_in_sen from WordDistance where ArticleNumber = %s and Sentence = 1 and Word like %s"
		cursor2.execute(sql2, (row['ArticleNumber'], word))
		locate = cursor2.fetchall()
		for loc in locate:
			location.append(loc['Loc_in_sen'])

	#단어 빈도를 계산하기 위해 가져오기
	sql5 = "select Word, count(*) as cnt from WordDistance where ArticleNumber= %s group by Word order by cnt desc limit 5" % (row['ArticleNumber']) 
	cursor5.execute(sql5)
	frequency = cursor5.fetchall()

	for frewo in frequency:
		freword.append(frewo['Word'])

	for locate in location:
		if len(wd) >= 4 :
			break
		wd.append(locate+1)
		wd.append(locate-1)
	print("wd")
	print(wd)
	for wdcount in wd:
		if wdcount == 0:
			final.append(LDAkeyword[1])
	#final.append(wd[0])
	#final.append(wd[1])
	#final.append(wd[2])
	#final.append(wd[3])
	#단어거리 모델 사용을 위해 DB에서 가져오기
	sql3 = "select * from WordDistance where Articlenumber = %s and Sentence=1 and Loc_in_sen = %s"
	for ll in wd:
		if ll !=0:
			cursor3.execute(sql3,(row['ArticleNumber'],ll)) #wd에는 위치가 들어있음
			wd2 = cursor3.fetchall()
			for wd3 in wd2:
				#print(wd3['Word'])
				final.append(wd3['Word'])
	#		catch = 0;
	#		for idx, LDA in enumerate(LDAkeyword):
	#			if idx < 1 : #3개의 단어 캐치
					#print("LDA")
					#print(LDA)
	#				if LDA != wd3['Word']:
						#print("wd3")
						#print(wd3['Word'])
	#					catch = catch + 1
						#print(catch)
	#		if catch == 1 :
	#			final.append(wd3['Word'])
	#		if catch < 1 :
	#			for fre in freword:
	#				check=0
	#				ldwcount = 0
	#				for ldw in LDAkeyword:
	#					if fre == ldw:
	#						check = 1
	#					ldwcount = ldwcount+1
	#					if ldwcount == 1:
	#						break
	#				if check == 0:
	#					final.append(fre)
	#					break
	#태깅 데이터 DB에서 가져오기
	if len(final) != 4:
		final.append(freword[0])
		final.append(freword[1]) 
	User = "User6"
	sql4 = "select * from Tagging where Articlenumber = %s and User=%s"
	cursor4.execute(sql4,(row['ArticleNumber'],User))
	Tagging = cursor4.fetchone()
	try :
		Tagword.append(Tagging['Word1'])
		Tagword.append(Tagging['Word2'])
		Tagword.append(Tagging['Word3'])
		Tagword.append(Tagging['Word4'])
		Tagword.append(Tagging['Word5'])
		print("Tagword")
		print(Tagword)

		LDAscore.append(LDAkeyword[0])
		LDAscore.append(LDAkeyword[1])
		LDAscore.append(LDAkeyword[2])
		LDAscore.append(LDAkeyword[3])
		LDAscore.append(LDAkeyword[4])
		print("LDAscore")
		print(LDAscore)

		jh_model.append(LDAkeyword[0])
		jh_model.append(final[0])
		jh_model.append(final[1])
		jh_model.append(final[2])
		jh_model.append(final[3])
		print("jh_model")
		print(jh_model)

		print("freword")
		print(freword)

		for sco in Tagword:
			for ldascore in LDAscore:
				if sco.find(ldascore)>=0 or  ldascore.find(sco)>=0:
					ldasscore = ldasscore+1

				if sco.strip() == ldascore.strip():
					allLdaScore = allLdaScore+1
					LDAscoree = LDAscoree+1
		print("LDA Score")
		print(LDAscoree)

		for sco in Tagword:
			for jh_mo in jh_model:

				if sco.find(jh_mo)>=0 or jh_mo.find(sco)>=0:
					modelsscore=modelsscore+1
				

				if sco.strip() == jh_mo.strip():
					allModelScore = allModelScore+1
					modelscore = modelscore+1
		print("modelScore")
		print(modelscore)
		
		for sco in Tagword:
			for fre_wo in freword:
				if sco.strip() == fre_wo.strip():
					allfreScore = allfreScore+1
					frescore = frescore+1
		
		print("빈도점수")
		print(frescore)
	except:
		print("except")
		except_count = except_count + 1
	
	wd = []
	Tagword = []
	Tagging = []
	LDAscore = []
	jh_model = []
	final = []
	frequency=[]
	freword=[]
	dicko=[]
	documentTopic=[]
	ldashow=[]
	LDAscoree = 0
	modelscore = 0
	frescore=0
	location=[]

print("총 LDA 점수")
print(allLdaScore)
print("LDA 유사 점수")
print(ldasscore)
print("총 모델 점수")
print(allModelScore)
print("모델 유사 점수")
print(modelsscore)
print("단어 빈도수 점수")
print(allfreScore)
print("except 횟수")
print(except_count)
