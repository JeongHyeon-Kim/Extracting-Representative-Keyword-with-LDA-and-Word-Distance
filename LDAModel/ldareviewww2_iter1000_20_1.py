from konlpy.tag import Twitter; t = Twitter()
from konlpy.corpus import kolaw
import nltk
import gensim
from gensim.models import LdaModel
from gensim import corpora,models
import nltk
import MySQLdb
import xlwt
db = MySQLdb.connect(host="localhost", user ="ice-kms", passwd="kkms1234", db="scraping", charset='utf8')

cursor = db.cursor(MySQLdb.cursors.DictCursor)
cursor.execute("set names utf8")

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

#koreanStopWord = kolaw.open('stopword.txt').read()

#workbook = xlwt.Workbook()
#worksheet = workbook.add_sheet('TopicNum_20_pass_100_iter_1000')

#lda_model_path = "/home/ice-kms/LDAModel/Real_lda_10000_pass_100_topicNum_20.lda"
#lda = LdaModel.load(lda_model_path)

#dictionary_path= "/home/ice-kms/LDAModel/Real_articleDic_10000_compound_topicNum_20.dict"
#dictionary = corpora.Dictionary.load(dictionary_path)

koreanStopWord = kolaw.open('stopword.txt').readlines()

xlrow=3
document=''
lenght=0
tokens_ko=[]
Compound=''

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
		if insert == 1:
			clean_model.append(word)

	#print(len(clean_model))
	#tokens_ko = t.nouns(document)
	dicko = dictionary.doc2bow(clean_model)
	documentTopic = lda[dicko]
	tokens_ko=[]
	
	#worksheet.write(xlrow,1,row['ArticleNumber'])
	#print(row['ArticleNumber'])
	#print(lda[0])
	#print(documentTopic)
	#lenght = len(documentTopic)
	#for i in range(0,lenght):
        #	worksheet.write(xlrow,documentTopic[i][0]+2,documentTopic[i][1])
	#xlrow = xlrow+1
	#document=''
	#lenght=0

#workbook.save('exxx.xls')

ldaModel = lda.show_topics(num_topics=50, num_words=5, formatted=True)
#print(type(ldaModel[1][1][1][1]))
print("Topic 1")
print(ldaModel[1][1])
print("Topic 2")
print(ldaModel[2][1])
print("Topic 3")
print(ldaModel[3][1])
print("Topic 4")
print(ldaModel[4][1])
print("Topic 5")
print(ldaModel[5][1])



#print(ldaModel[1][1][1][1])

#print(len(ldaModel))
#print(lda.print_topics(20))
#print(lda.show_topics(num_topics=20, num_words=5, formatted=False))

#worksheet.write(3,1,row['ArticleNumber'])

#T="Topic "
#for i in range(2,22):
	#print(i)
#	TopicName = T+str(i-1)
#	worksheet.write(2,i,TopicName)	

#length=len(documentTopic)
#print(documentTopic)
#for i in range(0,length):
#	worksheet.write(3,documentTopic[i][0]+1,documentTopic[i][1])

#workbook.save('J_TopicNum20_pass_100_iter_1000_compound.xls')

#print(documentTopic)
#print(documentTopic[0][0])
#print(documentTopic[0][1])

#print(lda.print_topics(20))

#print(lda.get_document_topics(dicko))
