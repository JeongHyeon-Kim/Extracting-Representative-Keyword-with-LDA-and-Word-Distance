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

cursor.execute("set names utf8")

sql = "select * from Test3 limit 100"
cursor.execute(sql.encode('utf8'))

rows = cursor.fetchall()
document = ''

koreanStopWord = kolaw.open('stopword2.txt').readlines()


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
location=[]
ldasscore=0
modelsscore=0
freqsscore=0
pos=[]

for row in rows:

	# 사전 불러오고 Lda 모델 불러오기
	lda_model_path = "/home/ice-kms/LDAModel/TopicNum20_Number_LDAModel.lda"
	lda = LdaModel.load(lda_model_path)

	dictionary_path= "/home/ice-kms/LDAModel/TopicNum20_Number_LDADic.dict"
	dictionary = corpora.Dictionary.load(dictionary_path)

	document = row['Content'].decode('utf8')

	# 공백 단위로 자르기
	split = document.split()
	i = 0
	# 자르고 난 후에 같은 위치에 명사 합치기
	for word in split:
		pos1 = t.pos(split[i])
		for poss in pos1:
			if poss[1] =="Noun" or poss[1]=="Number":
				pos.append(poss[0])
		for word2 in pos:
			Compound = Compound+word2
		tokens_ko.append(Compound)
		Compound = ''
		pos=[]
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
		if insert == 1:
			clean_model.append(word)
	print(len(clean_model))
	# 위의 clean_model 배열을 바탕으로 사전 생성( 이문서에서의)
	dicko = dictionary.doc2bow(clean_model)
	# document Topic 분포를 확인하기 위한 부분
	documentTopic = lda[dicko]

	# 가장 높은 문서-토픽 확률을 가지는 토픽을 가져온다.
	for Topic in documentTopic:
		if Topic[1]>maxprobability:
			maxprobability = Topic[1]
			maxTopicnum = Topic[0]

	ldashow = lda.show_topics(num_topics=20,num_words=10, formatted=False)

	#초기화 부분	
	dicko = []
	clean_model=[]
	documentTopic = []
	maxprobability= 0
	tokens_ko=[]
	LDAkeyword = []

	#가장 확률 높은 문서-토픽 분포에서 단어 열개를 LDAKeyword에 넣어준다.
	for word in ldashow[maxTopicnum][1]:
		LDAkeyword.append(word[0])
	
	maxTopicnum = 0

	print(row['ArticleNumber'])
	#print(LDAkeyword)
	for word in LDAkeyword:
		sql2 = "select Sentence, Loc_in_sen from WordDistance2 where Articlenumber = %s and Sentence =1 and Word like %s"
		cursor2.execute(sql2,(row['ArticleNumber'], "%"+word+"%"))
		locate = cursor2.fetchall()
		#print(locate)
		for loc in locate:
			location.append(loc['Loc_in_sen'])

	#print(location)

	sql5 = "select Word, count(*) as cnt from WordDistance2 where ArticleNumber= %s group by Word order by cnt desc limit 5" % (row['ArticleNumber']) 
	cursor5.execute(sql5)
	frequency = cursor5.fetchall()

	for frewo in frequency:
		freword.append(frewo['Word'])

	for locate in location:
		wd.append(locate+1)
		wd.append(locate-1)

	sql3 = "select * from WordDistance2 where Articlenumber = %s and Sentence=1 and Loc_in_sen = %s"

	for ll in wd:
		cursor3.execute(sql3,(row['ArticleNumber'],ll))
		wd2 = cursor3.fetchall()
		for wd3 in wd2:
			final.append(wd3['Word'])

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

		LDAscore.append(LDAkeyword[0])
		LDAscore.append(LDAkeyword[1])
		LDAscore.append(LDAkeyword[2])
		LDAscore.append(LDAkeyword[3])
		LDAscore.append(LDAkeyword[4])

		jh_model.append(LDAkeyword[0])
		jh_model.append(LDAkeyword[1])
		jh_model.append(LDAkeyword[2])
		jh_model.append(final[0])
		jh_model.append(final[1])

		print(jh_model)

		for sco in Tagword:
			for ldascore in LDAscore:

				if sco.find(ldascore)>=0 or ldascore.find(sco)>=0 :
					print(sco)
					print(ldascore)
					ldasscore = ldasscore+1

				if sco.strip() == ldascore.strip():
					allLdaScore = allLdaScore+1
					LDAscoree = LDAscoree+1
		print("LDA Score")
		print(LDAscoree)

		for sco in Tagword:
			for jh_mo in jh_model:

				if sco.find(jh_mo)>=0 or jh_mo.find(sco)>=0:
					print(sco)
					print(jh_mo)
					modelsscore = modelsscore+1

				if sco.strip() == jh_mo.strip():
					allModelScore = allModelScore+1
					modelscore = modelscore+1
		print("modelScore")
		print(modelscore)
		
		for sco in Tagword:
			for fre_wo in freword:
				if sco.strip() == fre_wo.strip():
					#print("모델위치")
					#print(sco.strip().find(jh_mo.strip()))
					allfreScore = allfreScore+1
					frescore = frescore+1
		
		print("빈도점수")
		print(frescore)
	except:
		exceptcount=exceptcount+1
		print("except")
	
	wd = []
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
	location=[]
	#print("정현식최종")
	#print("LDA")
	#print(LDAkeyword[0])
	#print(LDAkeyword[1])
	#print(LDAkeyword[2])
	#print("WordDistance")
	#print(final[0])
	#print(final[1])

print("LDA 점수")
print(allLdaScore)
print("LDA 유사 점수")
print(ldasscore)
print("총 모델 점수")
print(allModelScore)
print("모델 유사 점수")
print(modelsscore)
print("단어 빈도수 점수")
print(allfreScore)
print("제외 문서 수")
print(exceptcount)
