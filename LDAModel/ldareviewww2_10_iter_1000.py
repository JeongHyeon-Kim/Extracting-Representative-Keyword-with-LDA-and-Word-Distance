from konlpy.tag import Twitter; t = Twitter()
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
sql = "select * from Text2 where ArticleNumber<=10011"
cursor.execute(sql.encode('utf8'))

rows = cursor.fetchall()
document = ''

workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('TopicNum10_pass_100_iter_1000')

#lda_model_path = "/home/ice-kms/LDAModel/Real_lda_10000_pass_100_topicNum_20.lda"
#lda = LdaModel.load(lda_model_path)

#dictionary_path= "/home/ice-kms/LDAModel/Real_articleDic_10000_compound_topicNum_20.dict"
#dictionary = corpora.Dictionary.load(dictionary_path)

xlrow=3
document=''
lenght=0
#document = "박근혜 정부는 헌재에서 탄핵이 인용됨에 따라 곧 이어"
for row in rows:
	
	lda_model_path = "/home/ice-kms/LDAModel/iter_1000_Real_lda_10000_pass_100_topicNum_10.lda"
	lda = LdaModel.load(lda_model_path)
	
	dictionary_path= "/home/ice-kms/LDAModel/iter_1000_Real_articleDic_10000_compound_topicNum_10.dict"
	dictionary = corpora.Dictionary.load(dictionary_path)
	
	document = row['Content'].decode('utf8')
	tokens_ko = t.nouns(document)
	dicko = dictionary.doc2bow(tokens_ko)
	documentTopic = lda[dicko]
	
	worksheet.write(xlrow,1,row['ArticleNumber'])
	#print(row['ArticleNumber'])
	lenght = len(documentTopic)
	for i in range(0,lenght):
        	worksheet.write(xlrow,documentTopic[i][0]+2,documentTopic[i][1])
	xlrow = xlrow+1
	document=''
	lenght=0

#workbook.save('exxx.xls')

#ldaModel = lda.show_topics(num_topics=50, num_words=5, formatted=False)
#print(type(ldaModel[1][1][1][1]))
#print(ldaModel[1][1][1][0])
#print(ldaModel[1][1][1][1])

#print(len(ldaModel))
#print(lda.print_topics(20))
#lda.show_topics(num_topics=20, num_words=5, formatted=False)

#worksheet.write(3,1,row['ArticleNumber'])

T="Topic "
for i in range(2,12):
	#print(i)
	TopicName = T+str(i-1)
	worksheet.write(2,i,TopicName)	

#length=len(documentTopic)
#print(documentTopic)
#for i in range(0,length):
#	worksheet.write(3,documentTopic[i][0]+1,documentTopic[i][1])

workbook.save('TopicNum10_pass_100_iter_1000.xls')

#print(documentTopic)
#print(documentTopic[0][0])
#print(documentTopic[0][1])

#print(lda.print_topics(20))

#print(lda.get_document_topics(dicko))
