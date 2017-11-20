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
sql = "select * from Text3 where ArticleNumber=10000"
cursor.execute(sql.encode('utf8'))

row = cursor.fetchone()
document = row['Content'].decode('utf8')

lda_model_path = "/home/ice-kms/LDAModel/iter_1000_Real_lda_10000_pass_100_topicNum_20.lda"
lda = LdaModel.load(lda_model_path)

dictionary_path= "/home/ice-kms/LDAModel/iter_1000_Real_articleDic_10000_compound_topicNum_20.dict"
dictionary = corpora.Dictionary.load(dictionary_path)

ldaModel = lda.show_topics(num_topics=20, num_words=5, formatted=False)

tokens_ko = t.nouns(document)
dicko = dictionary.doc2bow(tokens_ko)
documentTopic = lda[dicko]

print(documentTopic)
