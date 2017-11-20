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

db.query("set character_set_connection=utf8;")
db.query("set character_set_server=utf8;")
db.query("set character_set_client=utf8;")
db.query("set character_set_results=utf8;")
db.query("set character_set_database=utf8;")

cursor.execute("set names utf8")

#sql = "SELECT * FROM ( select * from Test3 limit 500 ) as A where A.Articlenumber = ArticleNumber order by rand() limit 100"

#cursor.execute(sql.encode('utf8'))

#rows = cursor.fetchall()
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
User=['User3','User5','User6']
delTag=[]
compoundTag=''
RealTag=[]
tagcheck=0
alltagcount=0

fls = 0
flss = 0
fms = 0
fmss =0
ffs=0
fec =0
ftc = 0

for exnum in range(0,10):
	sql = "SELECT * FROM ( select * from Test4 limit 500 ) as A where A.Articlenumber = ArticleNumber order by rand() limit 100"

	cursor.execute(sql.encode('utf8'))
	rows = cursor.fetchall()

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
	User=['User3','User5','User6']
	delTag=[]
	compoundTag=''
	RealTag=[]
	tagcheck=0
	alltagcount=0
	document2=''

	for row in rows:

		# 사전 불러오고 Lda 모델 불러오기
		lda_model_path = "/home/ice-kms/LDAModel/TopicNum20_LDAModel_fin.lda"
		lda = LdaModel.load(lda_model_path)

		dictionary_path= "/home/ice-kms/LDAModel/TopicNum20_LDADic_fin.dict"
		dictionary = corpora.Dictionary.load(dictionary_path)

		document = row['Content'].decode('utf8')

		more2 = 1
		while (more2 == 1):
			if document.find('(') != -1:
				more2 = 2
				#print(punctu)
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
		split = document2.split()
		i = 0
		# 자르고 난 후에 같은 위치에 명사 합치기
		for word in split:
			pos = t.nouns(split[i])
			for word2 in pos:
				Compound = Compound+word2
			more = 1
			while(more == 1):
				pos2 = Twitter().pos(Compound)
				for poss in pos2:
					if poss[1] != 'Noun':
						more = 2
						pos3 = Twitter().nouns(Compound)
						Compound=''
						for word3 in pos3:
							Compound = Compound + word3
				if more == 2:
					more =1
				else:
					more = 0

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

		#print(clean_model)
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
	#	print(LDAkeyword)

		#wordscore=[]
		# 모든 글자를 dict형태로 구성
		sql6 = "select Word from WordDistance where Articlenumber = %s" % (row['ArticleNumber'])
		cursor6.execute(sql6)
		allword = cursor6.fetchall()
		for allwd in allword:
			wordscore[allwd['Word']] = 0

		# 문장의 개수 받아오기
		sql7 = "select Sentence from WordDistance where Articlenumber = %s group by Sentence" % (row['ArticleNumber'])
		cursor7.execute(sql7)
		sentencenumber = cursor7.fetchall()
		for senN in sentencenumber:
			senNumber.append(senN['Sentence'])
	#	print(senNumber)

	#	print(wordscore)
	#	print(len(LDAkeyword))

		checksss = 0
		for sen in senNumber:
			wordW = 0.145
			for word in LDAkeyword:
				#print(wordW)
				#if wordW == 0.0:
				#	break

				sql8="select Loc_in_sen from WordDistance where Articlenumber=%s and Sentence=%s and Word=%s";
				cursor8.execute(sql8,(row['ArticleNumber'],sen,word))
				senword = cursor8.fetchall()
				#checksen = cursor8.fetchone()
				#print(type(checksen['Loc_in_sen']))
				#if senword is None:
				#	print("why")
				if sen == 1 :
					checksss = checksss + len(senword)
				if sen >1 and checksss == 0:
					for word in LDAkeyword:
#						print("재검색")
						sql8="select Loc_in_sen from WordDistance where Articlenumber=%s and Sentence=%s and Word like %s";
						cursor8.execute(sql8,(row['ArticleNumber'],1,'%'+word+'%'))
						senword = cursor8.fetchall()

						for locsen in senword:
							sql9="select Word, 0.9*%s*(1/abs(Loc_in_sen-%s)) as value from (select * from WordDistance where Sentence=%s and Articlenumber=%s) as B where Loc_in_sen != %s ";
							cursor9.execute(sql9,(wordW,locsen['Loc_in_sen'],1,row['ArticleNumber'],locsen['Loc_in_sen']))
							firstsen = cursor9.fetchall()
					#print("현재문장 번호:1")
					#print(firstsen)
							for fs in firstsen:
					#print(fs['Word'])
								wordscore[fs['Word']] = wordscore[fs['Word']]+ decimal.Decimal(fs['value'])
					#print(wordscore)
					checksss = 1

				for locsen in senword:
					
	#				print("현재 단어 가중치")
	#				print(wordW)

					if sen == 1:
						sql9="select Word, 0.9*%s*(1/abs(Loc_in_sen-%s)) as value from (select * from WordDistance where Sentence=%s and Articlenumber=%s) as B where Loc_in_sen != %s ";
						cursor9.execute(sql9,(wordW,locsen['Loc_in_sen'],sen,row['ArticleNumber'],locsen['Loc_in_sen']))
						firstsen = cursor9.fetchall()
	#					print("현재문장 번호:1")
						#print(firstsen)
						for fs in firstsen:
							#print(fs['Word'])
							wordscore[fs['Word']] = wordscore[fs['Word']]+ decimal.Decimal(fs['value'])
	#					print(wordscore)

					else :
						sql10="select Word, 0.1*%s*(1/abs(Loc_in_sen-%s)) as value from (select * from WordDistance where Sentence=%s and Articlenumber=%s) as B where Loc_in_sen !=%s";
						cursor10.execute(sql10,(wordW,locsen['Loc_in_sen'],sen,row['ArticleNumber'],locsen['Loc_in_sen']))
						remainsen = cursor10.fetchall()
						#print("현재문장번호:")
						#print(sen)
						#print("찾은 단어 위치")
						#print(locsen['Loc_in_sen'])
						#print(sen)
						#print(remainsen)
						for rs in remainsen:
							wordscore[rs['Word']] = wordscore[rs['Word']]+ decimal.Decimal(rs['value'])
						#print(wordscore)
				wordW = wordW-0.01
				wordW = round(wordW,3)
		#print(wordscore)
		sortsco = sorted(wordscore.items(), key=operator.itemgetter(1),reverse=True)
		#print(sortsco)

		sql5 = "select Word, count(*) as cnt from WordDistance where ArticleNumber= %s group by Word order by cnt desc limit 5" % (row['ArticleNumber']) 
		cursor5.execute(sql5)
		frequency = cursor5.fetchall()

		for frewo in frequency:
			freword.append(frewo['Word'])

		#for Use in User:
		for Use in User:
			sql4 = "select * from Tagging where ArticleNumber = %s and User=%s order by date DESC limit 1;"
			cursor4.execute(sql4,(row['ArticleNumber'],Use))
			Tagging = cursor4.fetchone()
			Tagword.append(Tagging['Word1'])
			Tagword.append(Tagging['Word2'])
			Tagword.append(Tagging['Word3'])
			Tagword.append(Tagging['Word4'])
			Tagword.append(Tagging['Word5'])
	#	print(len(Tagword))
		
		for tag in range(0,len(Tagword)):
			delTag = 0
			if str(Tagword[tag]).strip().find(" ") >= 0:
	#			print("띄어쓰기")
	#			print(Tagword[tag])
				delTag = 1
			poss = Twitter().pos(Tagword[tag])
			for possum in poss:
				if (possum[1]) == 'Number':
					delTag = 1
					break
				if (possum[1]) == 'Noun':
					compoundTag = compoundTag + possum[0]

			if delTag == 0 :
	#			print(compoundTag)
				if len(RealTag) >0:
					tagcheck = 0
					for Real in RealTag:
						if Real == compoundTag:	
							tagcheck = 1
					if tagcheck ==0 and compoundTag != '' :
						RealTag.append(compoundTag)
				else:
					RealTag.append(compoundTag)
			compoundTag =''	
#		print(RealTag)
		alltagcount = alltagcount + len(RealTag)
		try :
			#Tagword.append(Tagging['Word1'])
			#Tagword.append(Tagging['Word2'])
			#Tagword.append(Tagging['Word3'])
			#Tagword.append(Tagging['Word4'])
			#Tagword.append(Tagging['Word5'])

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

#			print(jh_model)

			for sco in RealTag:
				for ldascore in LDAscore:
					if sco.strip() == ldascore.strip():
						allLdaScore = allLdaScore+1
						LDAscoree = LDAscoree+1
			
			for ldascore in LDAscore:
				for sco in RealTag:
					if sco.find(ldascore)>=0 or ldascore.find(sco)>=0 :
						ldasscore = ldasscore+1
						break
			
	#		print("LDA Score")
#			print(LDAscore)

			for sco in RealTag:
				for jh_mo in jh_model:
					if sco.strip() == jh_mo.strip():
						allModelScore = allModelScore+1
						modelscore = modelscore+1

			for jh_mo in jh_model:
				for sco in RealTag:
					if sco.find(jh_mo)>=0 or jh_mo.find(sco)>=0 :
						modelsscore = modelsscore+1
						break
			#print("modelScore")
	#		print(modelscore)
			
			for sco in RealTag:
				for fre_wo in freword:
					if sco.strip() == fre_wo.strip():
						#print("모델위치")
						#print(sco.strip().find(jh_mo.strip()))
						allfreScore = allfreScore+1
						frescore = frescore+1
			
	#		print("빈도점수")
	#		print(frescore)
		except:
			exceptcount=exceptcount+1
	#		print(row['ArticleNumber'])
	#		print("except")
		
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

		#print("정현식최종")
		#print("LDA")
		#print(LDAkeyword[0])
		#print(LDAkeyword[1])
		#print(LDAkeyword[2])
		#print("WordDistance")
		#print(final[0])
		#print(final[1])

	print("시행횟수"+str(exnum))
	print("LDA 점수")
	print(allLdaScore)
	fls = fls + allLdaScore
	print("LDA 유사 점수")
	print(ldasscore)
	flss = flss + ldasscore
	print("총 모델 점수")
	print(allModelScore)
	fms = fms + allModelScore
	print("모델 유사 점수")
	print(modelsscore)
	fmss = fmss + modelsscore
	print("단어 빈도수 점수")
	print(allfreScore)
	ffs = ffs + allfreScore
	print("제외 문서 수")
	print(exceptcount)
	fec = fec + exceptcount
	print("정답지 총 개수")
	print(alltagcount)
	ftc = ftc + alltagcount

print("문서 가중치 0.9, 0.1 / 역수 / 0.145 / 10개 빼는 거 없음")
print("LDA 점수")
print(fls/5000)
print("LDA 유사")
print(flss/5000)
print("모델 점수")
print(fms/5000)
print("모델 유사")
print(fmss/5000)
print("빈도 점수")
print(ffs/5000)
print("제외 문서수")
print(fec)
print("정답지 총 개수")
print(ftc)

