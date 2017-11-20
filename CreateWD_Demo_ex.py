#import nltk
from konlpy.corpus import kolaw
from konlpy.tag import *
from konlpy.utils import concordance, pprint
#from lxml import etree
import MySQLdb
import operator

db = MySQLdb.connect(host="localhost", user ="ice-kms", passwd="kkms1234", db="scraping", charset='utf8')
cursor = db.cursor(MySQLdb.cursors.DictCursor)
cursor.execute("set names utf8")

db.query("set character_set_connection=utf8;")
db.query("set character_set_server=utf8;")
db.query("set character_set_client=utf8;")
db.query("set character_set_results=utf8;")
db.query("set character_set_database=utf8;")

cursor.execute("set names utf8")
sql = "select * from Demo order by Number Desc limit 1"
cursor.execute(sql.encode('utf8'))

rows = cursor.fetchall()

# count는 문장에서의 위치
count=1

# 복합명사 Compound, 가져오는 문서 document
Compound=''
document=''

koreanStopWord = kolaw.open('stopword.txt').readlines()
# 문장의 위치
S=0
#num=0
checknum=0
poscheck1=[]
poscheck2=[]
numsen=0
numarray={}
#reverse=[]
no_action=0
num_2=0
no_sum = 0
more2 = 0
Locindex=0
puntuu =''
puntu1 = 0
puntu2 = 0
sum_no = 0
for row in rows:

	#document=row['Content'].decode('utf8')
	document = "'과반 저지'이다."
	#print(document)
	
	Locindex = 0
	more2 = 1
#	print(document)

	while (more2 == 1):
		if document.find('(') != -1:
			more2 = 2
			#print(document.find('('))
#			print(document)
			if ( document.find('(',document.find('(')+1) != -1 and document.find('(',document.find('(')+1) < document.find(')') ):
				document = document[0:document.find('(')] + document[document.find(')',document.find(')')+1)+1:]
			else :
				document = document[0:document.find('(')] + document[document.find(')')+1:]
			#print("후반")
#			print(document)
		if more2 == 2:
			more2 = 1
		else :
			more2 = 0
#	print(document)

	Loc_sentencee = document.split('.')
	#print(len(Loc_sentencee))
	
#	print(Loc_sentencee)


	for numsen in range(0,len(Loc_sentencee)):

		try:
			#print("첫문장")
			poscheck2=Twitter().pos(Loc_sentencee[numsen][0])
		#	print(checknum)
		#	print(Loc_sentencee[numsen].find("“"))
		#	print(Loc_sentencee[numsen].find("”"))
			if checknum ==1 and (poscheck2[0][1] == 'Number' or poscheck2[0][1] == 'Alpha') :
				#print("///")
				#numarray.append(numsen-1)
				numarray.append(numsen)
				#print(Loc_sentencee[numsen-1])
				#print(Loc_sentencee[numsen])
			checknum = 0
		except:
			no_action=0
		try:
			#print("마지막문장")
			poscheck1=Twitter().pos(Loc_sentencee[numsen][-1])
			#print("시작부호")
			#print(Loc_sentencee[numsen].find("“"))
			#print("마지막부호")
			#print(Loc_sentencee[numsen].rfind("”"))
			#print(" ") 
			if poscheck1[0][1] == 'Number' or poscheck1[0][1] == 'Alpha' :
#				print(Loc_sentencee[numsen])
				checknum = checknum +1
		except:
			no_action=0

		#print(Loc_sentencee[numsen].count("“"))
		#print(Loc_sentencee[numsen].count("”"))

	sum_no = 0
	puntu1 = 0
	puntu2 = 0
	numarray={}
	
	#print(num_array)
	for numsen in range(0,len(Loc_sentencee)):
#		print(num_array)
		puntu1 = puntu1 + Loc_sentencee[numsen].count("“")
		puntu2 = puntu2 + Loc_sentencee[numsen].count("”")
#		print(Loc_sentencee[numsen])
#		print(puntu1)
#		print(puntu2)
#		print(sum_no)
		if(puntu1 != puntu2) :
			#print("같지않다")
			#print(Loc_sentencee[numsen])
			sum_no = sum_no +1
#			numarray.append(numsen+1)
			continue
		else :
#			print(sum_no)
			if (puntu1 == 0) and (puntu2 == 0):
				continue
			for su in range(0,sum_no+1):
				numarray[numsen-sum_no] = sum_no
			#print(Loc_sentencee[numsen])
			sum_no = 0
			puntu1 = 0
			puntu2 = 0

#	print(numarray)
	numarray = sorted(numarray.items(),key=operator.itemgetter(0),reverse=True)
#	print(numarray)
#	print(Loc_sentencee)

#	print(type(numarray))	
	for key in numarray:

#		print(key)
#		print(key[0])
#		print(key[1])

#		print(Loc_sentencee[key[0]])
		#print(Loc_sentencee[num_2-1])

		for i in range(0,key[1]):
			Loc_sentencee[key[0]+key[1]-i-1] = Loc_sentencee[key[0]+key[1]-i-1] + "." + Loc_sentencee[key[0]+key[1]-i]
#		print(Loc_sentencee[num_2-2])
			del Loc_sentencee[key[0]+key[1]-i]

	#for locc in Loc_sentencee:
	#	print(locc)

#	print(Loc_sentencee)
#	Locindex = 0
#	for punctu in Loc_sentencee:
#		puntuu = punctu
#		more2 = 1
#		while (more2 == 1):
#			if puntuu.find('(') != -1:
#				more2 = 2
#				print(punctu)
#				puntuu = puntuu[0:puntuu.find('(')] + puntuu[puntuu.find(')')+1:]
#				print(punctu)
#			if more2 == 2:
#				more2 = 1
#			else :
#				more2 = 0 
#		Loc_sentencee[Locindex] = puntuu
#		Locindex = Locindex+1
#	print(Loc_sentencee)

	for sentence in Loc_sentencee:
		split = sentence.split()
		for word in split:
#			print(word)
			
			pos = Twitter().nouns(word)
			for  word2 in pos :
				Compound = Compound+word2
			more = 1
			while(more == 1):
				pos2 = Twitter().pos(Compound)
#				print(more)
				for poss in pos2:
					if poss[1] != 'Noun':
						more = 2
						pos3 = Twitter().nouns(Compound)
						Compound=''
						for word3 in pos3:
							Compound = Compound + word3
				if more == 2:
					more =1;
				else :
					more =0;
			insert=1

#			print(Compound)
			for stop in koreanStopWord:
				#if Compound == '대해선':
					#print('2')
				if Compound.strip() == stop.strip():
					#print(stop)
				#	if Compound=='아들':
				#		print('3')
					insert = 0
					#print('?')
			if insert == 1 and Compound !='':
				#if Compound=='대해선':
				#	print('1')
#				print(S+1)
#				print(count)
#				print(Compound)
#				cursor.execute("insert into WordDistance2 (ArticleNumber,Word,Sentence,Loc_in_sen) values(%s,%s,%s,%s)",(row['Number'],Compound,S+1,count))
#				db.commit()
				count = count+1
#				num = num+1
			Compound = ''

		S = S+1
		count = 1
	S=0


	checknum=0
	poscheck1=[]
	poscheck2=[]
	numsen=0
	numarray=[]
#reverse=[]
	no_action=0
	num_2=0


#print(num)
