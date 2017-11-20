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

sql = "select * from Test3 limit 1"
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
subtract=0
check_ok=0

#User=['User3','User5','User6']

output_file = open('Model-Score_interval_abs5_sentence.txt', 'w')


for wordWeight in range(5,50,5):

	User=['User3','User5','User6']
	#subtract = wordWeight/5
	for Use in User:

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

		for row in rows:

			# 사전 불러오고 Lda 모델 불러오기
			lda_model_path = "/home/ice-kms/LDAModel/TopicNum20_LDAModel.lda"
			lda = LdaModel.load(lda_model_path)

			dictionary_path= "/home/ice-kms/LDAModel/TopicNum20_LDADic.dict"
			dictionary = corpora.Dictionary.load(dictionary_path)

			document = row['Content'].decode('utf8')

			# 공백 단위로 자르기
			split = document.split()
			i = 0
			# 자르고 난 후에 같은 위치에 명사 합치기
			for word in split:
				pos = t.nouns(split[i])
				for word2 in pos:
					Compound = Compound+word2
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
				if insert == 1:
					clean_model.append(word)

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

#			print("기사번호")
#			print(row['ArticleNumber'])
			#print(LDAkeyword)

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
			#print(senNumber)

			#print(wordscore)

			for sen in senNumber:
				wordW = 25
				for word in LDAkeyword:

					if wordW == 0:
						break

					sql8="select Loc_in_sen from WordDistance where Articlenumber=%s and Sentence=%s and Word=%s";
					cursor8.execute(sql8,(row['ArticleNumber'],sen,word))
					senword = cursor8.fetchall()
					#checksen = cursor8.fetchone()
					#print(type(checksen['Loc_in_sen']))
					#if senword is None:
					#	print("why")

					for locsen in senword:
						
						#print("현재 단어 가중치")
						#print(wordW)

						if sen == 1:
							sql9="select Word, 0.8*%s*(1/abs(Loc_in_sen-%s)) as value from (select * from WordDistance where Sentence=%s and Articlenumber=%s) as B where Loc_in_sen != %s ";
							cursor9.execute(sql9,(wordW,locsen['Loc_in_sen'],sen,row['ArticleNumber'],locsen['Loc_in_sen']))
							firstsen = cursor9.fetchall()
							#print("현재문장 번호:1")
							#print(firstsen)
							for fs in firstsen:
								#print(fs['Word'])
								wordscore[fs['Word']] = wordscore[fs['Word']]+ decimal.Decimal(fs['value'])
							#print(wordscore)

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

					wordW = wordW-1

			#print(wordscore)
			sortsco = sorted(wordscore.items(), key=operator.itemgetter(1),reverse=True)
			#print(sortsco)

			sql5 = "select Word, count(*) as cnt from WordDistance where ArticleNumber= %s group by Word order by cnt desc limit 5" % (row['ArticleNumber']) 
			cursor5.execute(sql5)
			frequency = cursor5.fetchall()

			for frewo in frequency:
				freword.append(frewo['Word'])

			User = Use
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

				for sortnum in range(0,10):
					if len(jh_model) == 5:
						break
					
					check_ok = 0

					for ldacheck in range(0,5):
						if LDAscore[ldacheck] == sortsco[sortnum][0]:
							check_ok = 1 
					if check_ok == 0:
						jh_model.append(sortsco[sortnum][0])

				print(jh_model)

				for sco in Tagword:
					for ldascore in LDAscore:

						if sco.find(ldascore)>=0 or ldascore.find(sco)>=0 :
				#			print(sco)
				#			print(ldascore)
							ldasscore = ldasscore+1

						if sco.strip() == ldascore.strip():
							allLdaScore = allLdaScore+1
							LDAscoree = LDAscoree+1
#				print("LDA Result")
#				print(LDAscore)

				for sco in Tagword:
					for jh_mo in jh_model:

						if sco.find(jh_mo)>=0 or jh_mo.find(sco)>=0:
				#			print(sco)
				#			print(jh_mo)
							modelsscore = modelsscore+1

						if sco.strip() == jh_mo.strip():
							allModelScore = allModelScore+1
							modelscore = modelscore+1
#				print("modelResult")
#				print(jh_model)
				#print(sortsco[5][0])
				#print(sortsco[6][0])
				for sco in Tagword:
					for fre_wo in freword:
						if sco.strip() == fre_wo.strip():
							#print("모델위치")
							#print(sco.strip().find(jh_mo.strip()))
							allfreScore = allfreScore+1
							frescore = frescore+1
				
#				print("빈도Result")
#				print(freword)
#				print("Tagging Result")
#				print(Tagword)
#				print("")


			except:
				exceptcount=exceptcount+1
			#	print(row['ArticleNumber'])
			#	print("except")
			
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

			#print("정현식최종")
			#print("LDA")
			#print(LDAkeyword[0])
			#print(LDAkeyword[1])
			#print(LDAkeyword[2])
			#print("WordDistance")
			#print(final[0])
			#print(final[1])
		
		output_file.write("\nWord 가중치: "+str(wordWeight))
		output_file.write("\nUSER: "+str(Use))
		output_file.write("\nLDA 점수:"+str(allLdaScore))
		output_file.write("\nLDA 유사 점수: "+str(ldasscore))
		output_file.write("\n총 모델 점수: "+str(allModelScore))
		output_file.write("\n모델 유사 점수: "+str(modelsscore))
		output_file.write("\n단어 빈도수 점수: " + str(allfreScore))
		output_file.write("\n제외 문서 수: "+ str(exceptcount))
		print("\nWord 가중치: "+str(wordWeight))
		#print(wordWeight)
		print("\nUSER: "+str(Use))
		#print(Use)
		print("\nLDA 점수:"+str(allLdaScore))
		#print(allLdaScore)
		print("\nLDA 유사 점수: "+str(ldasscore))
		#print(ldasscore)
		print("\n총 모델 점수: "+str(allModelScore))
		#print(allModelScore)
		print("\n모델 유사 점수: "+str(modelsscore))
		#print(modelsscore)
		print("\n단어 빈도수 점수: " + str(allfreScore))
		#print(allfreScore)
		print("\n제외 문서 수: "+ str(exceptcount))
		#print(exceptcount)



output_file.close()
db.close()

