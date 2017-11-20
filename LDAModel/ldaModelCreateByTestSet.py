#-*- coding: utf-8 -*-

#라이브러리 추가
from konlpy.tag import Twitter; t = Twitter()
import nltk
import gensim
from gensim import corpora, models
#from gensim import LdaMallet
import MySQLdb
from jpype import *
import codecs

# db 연결하고 인코딩 부분
db = MySQLdb.connect(host="localhost", user ="ice-kms", passwd="kkms1234", db="scraping", charset='utf8')

cursor = db.cursor(MySQLdb.cursors.DictCursor)
cursor.execute("set names utf8")

db.query("set character_set_connection=utf8;")
db.query("set character_set_server=utf8;")
db.query("set character_set_client=utf8;")
db.query("set character_set_results=utf8;")
db.query("set character_set_database=utf8;")

f = open("./test_article_number2.txt", 'r')
lines = f.readlines()
#for line in lines:
#	print(line.strip())

cursor.execute("set names utf8")
for line in lines:
	sql = "insert into Test4 (select * from Text5 where ArticleNumber=%s)"%line.strip()
	cursor.execute(sql.encode('utf8'))
	db.commit()
f.close()
db.close()
