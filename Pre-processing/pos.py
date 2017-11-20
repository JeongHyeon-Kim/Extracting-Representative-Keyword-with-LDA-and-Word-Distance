from collections import Counter

#import nltk
from konlpy.corpus import kolaw
from konlpy.tag import *
from konlpy.utils import concordance, pprint
import MySQLdb
import matplotlib 
matplotlib.use('Agg')

db = MySQLdb.connect(host="localhost", user ="ice-kms", passwd="kkms1234", db="scraping", charset='utf8')
cursor = db.cursor(MySQLdb.cursors.DictCursor)
cursor.execute("set names utf8")

db.query("set character_set_connection=utf8;")
db.query("set character_set_server=utf8;")
db.query("set character_set_client=utf8;")
db.query("set character_set_results=utf8;")
db.query("set character_set_database=utf8;")

cursor.execute("set names utf8")
sql = "select Content from Test3 where Articlenumber=5"
cursor.execute(sql.encode('utf8'))

rows = cursor.fetchall()

document2=''

for row in rows:
	print(row['Content'].decode('utf8'))
	document2 = document2+ row['Content'].decode('utf8')

#print(document2)

pos = Twitter().pos(document2+"'문재인은 바보이다'")
print(pos)
array=[]

#cnt = Counter(pos)
for poss in pos:
	if poss[1] == "Noun" or poss[1] == "Number":
		array.append(poss[0])

print(array)

#print('nchars  :', len(document2))
#print('ntokens :', len(document2.split()))
#print('nmorphs :', len(set(pos)))
#print('\nTop 50 frequent morphemes:'); pprint(cnt.most_common(30))
#ko = nltk.Text(pos, name='명사추출')
##output_file = open('pos0.txt', 'w')
##for row in cnt.most_common(3000):
##	output_file.write(str(row)+'\n')

##output_file.close()
#ko.vocab()
#ko.plot(50)
#ko.savefig('word.png')
#ko.show()
#x = pos
#y = cnt
#plt.plot(x,y)
#plt.show()
