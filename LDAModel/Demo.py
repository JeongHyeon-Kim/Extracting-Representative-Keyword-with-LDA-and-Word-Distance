from collections import Counter
from konlpy.tag import Twitter; t = Twitter()
from konlpy.corpus import kolaw
#import nltk
import gensim
from gensim.models import LdaModel
from gensim import corpora,models
#import nltk
import MySQLdb
#import xlwt
db = MySQLdb.connect(host="localhost", user ="ice-kms", passwd="kkms1234", db="scraping", charset='utf8')

cursor = db.cursor(MySQLdb.cursors.DictCursor)
cursor2 = db.cursor(MySQLdb.cursors.DictCursor)
cursor3 = db.cursor(MySQLdb.cursors.DictCursor)
cursor.execute("set names utf8")
cursor2.execute("set names utf8")
cursor3.execute("set names utf8")

db.query("set character_set_connection=utf8;")
db.query("set character_set_server=utf8;")
db.query("set character_set_client=utf8;")
db.query("set character_set_results=utf8;")
db.query("set character_set_database=utf8;")

cursor.execute("set names utf8")

sql = "select * from Text3 where ArticleNumber=1"
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

for row in rows:

	lda_model_path = "/home/ice-kms/LDAModel/JJ_Real_lda_10000_pass_200_topicNum_20.lda"
	lda = LdaModel.load(lda_model_path)

	dictionary_path= "/home/ice-kms/LDAModel/JJ_Real_articleDic_10000_compound_topicNum_20.dict"
	dictionary = corpora.Dictionary.load(dictionary_path)

	document = row['Content'].decode('utf8')

	split = document.split()
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

	#print(len(clean_model))
        #tokens_ko = t.nouns(document)
	dicko = dictionary.doc2bow(clean_model)
	documentTopic = lda[dicko]

	maxprobability = 0
	for Topic in documentTopic:
		if Topic[1]>maxprobability:
			maxprobability = Topic[1]
			maxTopicnum = Topic[0]
	#print(maxTopicnum)
	ldashow = lda.show_topics(num_topics=20,num_words=10, formatted=False)	
	#print(ldashow)
	#print(ldashow[maxTopicnum])
	
	#print(ldashow[maxTopicnum][1][0][0])
	for word in ldashow[maxTopicnum][1]:
		LDAkeyword.append(word[0])
		#LDAkeyword.append(word[1])
		#LDAkeyword.append(word[2])
		#LDAkeyword.append(word[3])
		#LDAkeyword.append(word[4])
	print("LDA")
	print(LDAkeyword)
	print("WordDistance")
	
	sql2 = "select Sentence, Loc_in_sen from WordDistance where Articlenumber = %s and Word like %s or Word like %s or Word like %s or Word like %s or Word like %s"
	cursor2.execute(sql2,(row['ArticleNumber'], "%"+LDAkeyword[0]+"%", "%"+LDAkeyword[1]+"%","%"+LDAkeyword[2]+"%","%"+LDAkeyword[3]+"%","%"+LDAkeyword[4]+"%"))
	location = cursor2.fetchall()

	for locate in location:
		if locate['Sentence'] == 1:
			wd.append(locate['Loc_in_sen']+2)
			#sen.append(locate['Sentence'])
			wd.append(locate['Loc_in_sen']+1)
			#sen.append(locate['Sentence'])
			wd.append(locate['Loc_in_sen']-1)
			wd.append(locate['Loc_in_sen']-2)
	#print(wd)

	sql3 = "select * from WordDistance where Articlenumber = %s and Sentence=1 and Loc_in_sen = %s"
	#number = row['ArticleNumber']
	#i=0
	for ll in wd:
		cursor3.execute(sql3,(row['ArticleNumber'],ll))
		wd2 = cursor3.fetchall()
		#final.append(wd2['Word'])
		for wd3 in wd2:
			#print(wd3['Word'])
			final.append(wd3['Word'])
		#i = i+1
	#print(final)
	cnt = Counter(final)
	print(cnt)
#	wd2 = cursor3.fetchall()
#	print(len(wd2))
	
#	for sen in wd:
#		for wl in wd2:
#			if wl['Loc_in_sen'] == sen and wl['Sentence']==1:
#				wd2.append(wl['Word'])
#	print(wd2)


	print("정현식최종")
	print("LDA")
	print(LDAkeyword[0])
	#print(LDAkeyword[1])
	#print(LDAkeyword[2])
	print("WordDistance")
	print(final[0])
	print(final[1])
	print(final[2])
	print(final[3])
