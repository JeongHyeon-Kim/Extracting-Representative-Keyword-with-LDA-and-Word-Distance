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
sql = "select * from Text2 where Articlenumber=7898"
cursor.execute(sql.encode('utf8'))

row = cursor.fetchone()
document = row['Content'].decode('utf8')


lda_model_path = "/home/ice-kms/LDAModel/iter_1000_Real_lda_10000_pass_100_topicNum_10.lda"
lda = LdaModel.load(lda_model_path)

dictionary_path= "/home/ice-kms/LDAModel/iter_1000_Real_articleDic_10000_compound_topicNum_10.dict"
dictionary = corpora.Dictionary.load(dictionary_path)

#document = "박근혜 정부는 헌재에서 탄핵이 인용됨에 따라 곧 이어"
tokens_ko = t.nouns(document)
dicko = dictionary.doc2bow(tokens_ko)
documentTopic = lda[dicko]


#ldaModel = lda.show_topics(num_topics=50, num_words=5, formatted=False)
#print(type(ldaModel[1][1][1][1]))
#print(ldaModel[1][1][1][0])
#print(ldaModel[1][1][1][1])

#print(len(ldaModel))
#print(lda.print_topics(20))
#print(lda.show_topics(num_topics=10, num_words=5, formatted=False))

#workbook=xlwt.Workbook()

#worksheet = workbook.add_sheet('TopicNum_20')
#worksheet.write(3,1,row['ArticleNumber'])

#T="Topic "
#for i in range(2,52):
	#print(i)
#TopicName = T+str(i-1)
#	worksheet.write(2,i,TopicName)	

#length=len(documentTopic)
#print(documentTopic)
#for i in range(0,length):
#	worksheet.write(3,documentTopic[i][0]+1,documentTopic[i][1])

##workbook.save('exx.xls')

#print(documentTopic)
#print(documentTopic[0][0])
#print(documentTopic[0][1])

#print(lda.print_topics(20))

#print(lda.get_document_topics(dicko,minimum_probability=0))

print('Perplexity: '),
perplex = lda.bound(dicko)
print (type(perplex))

print('Per-word Perplexity: '),
print (log_perplexity(1000,total_docs=10000))


#print numpy.exp2(-perplex / sum(cnt for document in cp_test for _, cnt in document)
