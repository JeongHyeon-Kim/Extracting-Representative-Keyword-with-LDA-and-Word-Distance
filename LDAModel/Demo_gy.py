from collections import Counter
from konlpy.tag import Twitter; t = Twitter()
from konlpy.corpus import kolaw
from types import *
#import nltk
import gensim
from gensim.models import LdaModel
from gensim import corpora,models
#import nltk
import MySQLdb
import operator
#import xlwt
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
wordselect=[]
Topicnum=0
dict={}
wordorder=0
exceptcount=0
for row in rows:

	lda_model_path = "/home/ice-kms/LDAModel/TopicNum20_LDAModel.lda"
	lda = LdaModel.load(lda_model_path)

	dictionary_path= "/home/ice-kms/LDAModel/TopicNum20_LDADic.dict"
	dictionary = corpora.Dictionary.load(dictionary_path)

	document = row['Content'].decode('utf8')

	split = document.split()
	i = 0

	#print(split)
	for word in split:
		pos = t.nouns(split[i])
		for word2 in pos:
			Compound = Compound+word2
		tokens_ko.append(Compound)
		Compound = ''
		i = i+1
	split=[]
	clean_model=[]
	#print(tokens_ko)
	for word in tokens_ko:
		insert = 1
		for stop in koreanStopWord:
			if word.strip() == stop.strip():
				insert = 0
				break
		if insert == 1:
			clean_model.append(word)

	dicko = dictionary.doc2bow(clean_model)

	documentTopic = lda.get_document_topics(dicko,minimum_probability=0)
	#print(documentTopic)
	#maxprobability = 0
	ldashow = lda.show_topics(num_topics=20,num_words=5, formatted=False)
	#print(ldashow)
	#for Topic in documentTopic:
	for ldaword in ldashow:
		#print(len(ldaword[1]))
		for sword in ldaword[1]:
		#print(ldaword[1][wordorder][0])
		#print(ldaword[1][wordorder][1])
			#print(sword)
			#print(sword[wordorder][0])
				#print(sword[0])
				#print(sword[1])
				#print(Topic[1])
			#print(type(sword[0]))
			#print(sword[0])
			#print(documentTopic[Topicnum][1])
			dict[sword[1]*documentTopic[Topicnum][1]] = sword[0]
		#wordorder = wordorder + 1
		#print(dict)
		Topicnum = Topicnum + 1
		#wordorder=0
		
	#print(ldashow)	
			#print(dict)
	Topicnum = 0
	sorted_word = sorted(dict.items(),key=operator.itemgetter(0),reverse=True)
	LDAkeyword.append(sorted_word[0][1])
	LDAkeyword.append(sorted_word[1][1])
	LDAkeyword.append(sorted_word[2][1])
	LDAkeyword.append(sorted_word[3][1])
	LDAkeyword.append(sorted_word[4][1])

	#print(sorted_word)
	#print(documentTopic)
	sorted_word.clear()
	dict.clear()
	dict = {}
	
	print(LDAkeyword)
	#ldashow = lda.show_topics(num_topics=20,num_words=5, formatted=False)	
	#print(ldashow)
	#print(ldashow[maxTopicnum])
	
	#print(ldashow[maxTopicnum][1][0][0])
	#for word in ldashow[maxTopicnum][1]:
	#	LDAkeyword.append(word[0])
		#LDAkeyword.append(word[1])
		#LDAkeyword.append(word[2])
		#LDAkeyword.append(word[3])
		#LDAkeyword.append(word[4])
	#print("LDA만")
	#print(LDAkeyword)
	#print("WordDistance")
	
	#초기화 부분
	dicko = []
	clean_model=[]
	documentTopic = []
	tokens_ko=[]

	print(row['ArticleNumber'])
	sql2 = "select Sentence, Loc_in_sen from WordDistance where Articlenumber = %s and Word like %s or Word like %s or Word like %s or Word like %s or Word like %s"
	cursor2.execute(sql2,(row['ArticleNumber'], "%"+LDAkeyword[0]+"%", "%"+LDAkeyword[1]+"%","%"+LDAkeyword[2]+"%","%"+LDAkeyword[3]+"%","%"+LDAkeyword[4]+"%"))
	location = cursor2.fetchall()

	sql5 = "select Word, count(*) as cnt from WordDistance where ArticleNumber= %s group by Word order by cnt desc limit 5" % (row['ArticleNumber']) 
	cursor5.execute(sql5)
	frequency = cursor5.fetchall()

	for frewo in frequency:
		freword.append(frewo['Word'])
	#print(freword)

	#print(row['ArticleNumber'])
	for locate in location:
		if locate['Sentence'] == 1:
			if len(wd)>=2 :
				break
			#print(locate['Sentence'])
			#wd.append(locate['Loc_in_sen']+2)
			#sen.append(locate['Sentence'])
			wd.append(locate['Loc_in_sen']+1)
			#sen.append(locate['Sentence'])
			wd.append(locate['Loc_in_sen']-1)
			#wd.append(locate['Loc_in_sen']-2)

	sql3 = "select * from WordDistance where Articlenumber = %s and Sentence=1 and Loc_in_sen = %s"
	#number = row['ArticleNumber']
	#i=0
	#print(wd)
	for ll in wd:
		cursor3.execute(sql3,(row['ArticleNumber'],ll))
		wd2 = cursor3.fetchall()
		#final.append(wd2['Word'])
		for wd3 in wd2:
			#print(wd3['Word'])
			final.append(wd3['Word'])
		#i = i+1
	#print(final)
	#if len(final) != 2 :
	#	print("wd 없다")
	#cnt = Counter(final)
	#print(len(final))
#	wd2 = cursor3.fetchall()
#	print(len(wd2))

#	for sen in wd:
#		for wl in wd2:
#			if wl['Loc_in_sen'] == sen and wl['Sentence']==1:
#				wd2.append(wl['Word'])
#	print(wd2)

	User = "User6"
	sql4 = "select * from Tagging where Articlenumber = %s and User=%s"
	cursor4.execute(sql4,(row['ArticleNumber'],User))
	Tagging = cursor4.fetchone()

	#print(len(Tagging['Word1']))
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

		#print(jh_model)
		#print(Tagword)

		for sco in Tagword:
			for ldascore in LDAscore:
				if sco.strip() == ldascore.strip():
					#print("위치")
					#print(sco.strip().find(ldascore.strip()))
					allLdaScore = allLdaScore+1
					LDAscoree = LDAscoree+1
		print("LDA Score")
		print(LDAscoree)

		for sco in Tagword:
			for jh_mo in jh_model:
				if sco.strip() == jh_mo.strip():
					#print("모델위치")
					#print(sco.strip().find(jh_mo.strip()))
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
		exceptcount = exceptcount +1
		print("except")
	#print("정현 Model")
	#print(modelscore)
	#print(Tagword)
	#print(jh_model)
	#print(ldascore)
	
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
	dict = {}
	sorted_word = {}
	#print("정현식최종")
	#print("LDA")
	#print(LDAkeyword[0])
	#print(LDAkeyword[1])
	#print(LDAkeyword[2])
	#print("WordDistance")
	#print(final[0])
	#print(final[1])

print("총 LDA 점수")
print(allLdaScore)
print("총 모델 점수")
print(allModelScore)
print("단어 빈도수 점수")
print(allfreScore)
print("제외 문서 수")
print(exceptcount)
