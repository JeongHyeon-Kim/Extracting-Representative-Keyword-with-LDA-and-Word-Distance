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
import math
db = MySQLdb.connect(host="localhost", user ="ice-kms", passwd="kkms1234", db="scraping", charset='utf8')

cursor = db.cursor(MySQLdb.cursors.DictCursor)
cursor2 = db.cursor(MySQLdb.cursors.DictCursor)

cursor.execute("set names utf8")
cursor2.execute("set names utf8")
db.query("set character_set_connection=utf8;")
db.query("set character_set_server=utf8;")
db.query("set character_set_client=utf8;")
db.query("set character_set_results=utf8;")
db.query("set character_set_database=utf8;")

Articlenumber=[]
Word = {}
eachword={}
tfidf={}
maxfre = 0
flag = 0

sql = "SELECT Articlenumber FROM WordDistance group by Articlenumber"
cursor.execute(sql.encode('utf8'))
rows = cursor.fetchall()
for row in rows:
	Articlenumber.append(row['Articlenumber'])

sql3 = "SELECT Word FROM WordDistance group by Word"
cursor2.execute(sql3.encode('utf8'))
words = cursor2.fetchall()
for wo in words:
	Word[wo['Word']] = 0

#print(Word)
for number in Articlenumber:
	sql2 = "SELECT Word FROM WordDistance where Articlenumber=%s group by Word" % (number)
	cursor.execute(sql2)
	groupword = cursor.fetchall()
	for group in groupword:
#		print(group['Word'])
		Word[group['Word'].strip()] = Word[group['Word'].strip()] + 1

sortword = sorted(Word.items(), key =operator.itemgetter(1), reverse = True)
#print(sortword)

#for number in Articlenumber:
sql4 = "SELECT Word,count(Word) as cnt FROM WordDistance where Articlenumber=1 group by Word order by cnt desc" 
cursor.execute(sql4)
frequency = cursor.fetchall()
flag = 0
eachword={}
for fre in frequency:
	if flag == 0:
		maxfre = fre['cnt']
		flag = 1
#	print(maxfre)
	eachword[fre['Word']] = 0.5 + 0.5*fre['cnt']/maxfre
#print(eachword)

for key in eachword.keys():
	print(key)
	print(eachword[key])
	print(math.log10(500/Word[key]))
	tfidf[key] = eachword[key]*math.log10(500/Word[key])

ttfsort = sorted(tfidf.items(), key =operator.itemgetter(1), reverse = True)
#print(ttfsort)
