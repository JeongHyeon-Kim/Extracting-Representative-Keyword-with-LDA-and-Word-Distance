#from konlpy.tag import Twitter; t = Twitter()
#import nltk
#import gensim
#from gensim.models import LdaModel
#from gensim import corpora,models
#import nltk
from collections import Counter
from konlpy.tag import Twitter; t = Twitter()
#import nltk
from konlpy.corpus import kolaw
from konlpy.tag import *
from konlpy.utils import concordance, pprint

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
sql = "select * from Text3 where ArticleNumber<=10000"
cursor.execute(sql.encode('utf8'))

rows = cursor.fetchall()

workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('word')

xlrow=3

koreanStopWord = kolaw.open('stopword.txt').read()
worksheet.write(2,1,"기사번호")
worksheet.write(2,2,"전체 단어의 개수")
worksheet.write(2,3,"명사만 추출")
worksheet.write(2,4,"복합명사고려-정지단어 제거")
worksheet.write(2,5,"기사의 날짜")

document=''
tokens_ko=[]
Compound=''

for row in rows:
	
	worksheet.write(xlrow,1,row['ArticleNumber'])
        #print(row['ArticleNumber'])
       # lenght = len(documentTopic)
       # for i in range(0,lenght):
       #        worksheet.write(xlrow,documentTopic[i][0]+2,documentTopic[i][1])
	#print(row['Date'])
	word = Twitter().pos(row['Content'].decode('utf8'))
	#cnt = Counter(word)
	#print("전체단어")
	all = len(word)
	#print(all)
	word2 = Twitter().nouns(row['Content'].decode('utf8'))
	#cnt2 = Counter(word2)
	#print("명사만")
	nounn=len(word2)
	#print(nounn)
	document=row['Content'].decode('utf8')
	split = document.split()
	i = 0
	for word in split:
		pos = t.nouns(split[i])
		#if pos=='지지'
		#	print(?)
		for word2 in pos:
			Compound = Compound+word2
		tokens_ko.append(Compound)
		Compound = ''
		i = i+1
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
		#clean_model.append(stop_m)
	#print(len(clean_model))
	#docRemovingStopWord = [i for i in tokens_ko if str(i.strip()) not in koreanStopWord]
	
	#print("복합명사 - 정지단어")
	#print(len(clean_model))
	worksheet.write(xlrow,2,all)
	worksheet.write(xlrow,3,nounn)
	worksheet.write(xlrow,4,len(clean_model))
	worksheet.write(xlrow,5,row['Date'])
	xlrow = xlrow+1
       # document=''
       # lenght=0


workbook.save('word-count-Date.xls')
