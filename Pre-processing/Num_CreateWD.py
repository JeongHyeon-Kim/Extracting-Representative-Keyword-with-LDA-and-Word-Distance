#import nltk
from konlpy.corpus import kolaw
from konlpy.tag import *
from konlpy.utils import concordance, pprint
from lxml import etree
import MySQLdb

db = MySQLdb.connect(host="localhost", user ="ice-kms", passwd="kkms1234", db="scraping", charset='utf8')
cursor = db.cursor(MySQLdb.cursors.DictCursor)
cursor.execute("set names utf8")

db.query("set character_set_connection=utf8;")
db.query("set character_set_server=utf8;")
db.query("set character_set_client=utf8;")
db.query("set character_set_results=utf8;")
db.query("set character_set_database=utf8;")

cursor.execute("set names utf8")
sql = "select * from Test3 limit 100"
cursor.execute(sql.encode('utf8'))

rows = cursor.fetchall()

# count는 문장에서의 위치
count=1

# 복합명사 Compound, 가져오는 문서 document
Compound=''
document=''

koreanStopWord = kolaw.open('stopword2.txt').readlines()
# 문장의 위치
S=0
num=0
pos=[]

for row in rows:

	document=row['Content'].decode('utf8')
	#print(document)
	Loc_sentencee = document.split('. ')
	#print(len(Loc_sentencee))
	for sentence in Loc_sentencee:
		split = sentence.split()
		for word in split:
			#pos = Twitter().nouns(word)
			pos1 = Twitter().pos(word)
			for poss in pos1:
				if poss[1] == "Noun" or poss[1]=="Number":
					pos.append(poss[0])
			#print(pos)
			for  word2 in pos :
				Compound = Compound+word2
			insert=1
			pos = []
			#print(Compound)
			for stop in koreanStopWord:
				#if Compound == '대해선':
					#print('2')
				if Compound.strip() == stop.strip():
					#print(stop)
				#	if Compound=='아들':
				#		print('3')
					insert = 0
					#print('?')
			if insert == 1:
				#if Compound=='대해선':
				#	print('1')
#				print(S+1)
#				print(count)
#				print(Compound)
				cursor.execute("insert into WordDistance2 (ArticleNumber,Word,Sentence,Loc_in_sen) values(%s,%s,%s,%s)",(row['ArticleNumber'],Compound,S+1,count))
				db.commit()
				#print(Compound)
				count = count+1
				#num = num+1
			Compound = ''

		S = S+1
		count = 1
	S=0

#print(num)
