#from konlpy.tag import Twitter; t = Twitter()
#import nltk
#import gensim
#from gensim.models import LdaModel
#from gensim import corpora,models
#import nltk
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

workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('Date')

xlrow=3

for row in rows:
	
	worksheet.write(xlrow,1,row['ArticleNumber'])
        #print(row['ArticleNumber'])
       # lenght = len(documentTopic)
       # for i in range(0,lenght):
       #        worksheet.write(xlrow,documentTopic[i][0]+2,documentTopic[i][1])
	print(row['Date'])
	worksheet.write(xlrow,2,row['Date'])
	xlrow = xlrow+1
       # document=''
       # lenght=0


workbook.save('Date13.xls')
