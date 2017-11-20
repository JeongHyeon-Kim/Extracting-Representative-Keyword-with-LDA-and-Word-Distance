import sys
import re
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
from lxml import etree
#from html2text import html2text
import MySQLdb

db = MySQLdb.connect(host="localhost", user ="ice-kms", passwd="kkms1234", db="scraping", charset="utf8")
db.set_character_set('utf8')

cursor = db.cursor(MySQLdb.cursors.DictCursor)
cursor.execute("set names utf8")

db.query("set character_set_connection=utf8;")
db.query("set character_set_server=utf8;")
db.query("set character_set_client=utf8;")
db.query("set character_set_results=utf8;")
db.query("set character_set_database=utf8;")

cursor.execute("set names utf8")
sql = "select * from Raw2"
cursor.execute(sql.encode('utf8'))

rows = cursor.fetchall()
content=''
content2=''
splitnum=0
title=''
def clean_text(text):
        cleaned_text = re.sub('[a-zA-Z]', '', text)
        cleaned_text = re.sub('[\{\}\[\]\/?,;:|\n*~`!^\-_+<>@\#$%&\\\=\'\"]', '', cleaned_text)
        return cleaned_text

def html2text(html): 
    soup = BeautifulSoup(html) 
    text_parts = soup.findAll(text=True) 
    return ''.join(text_parts)


for row in rows:
	#print(row)
	content = str(row['Content'].decode('utf8'))
	#print(content)
	splitnum = content.find('<div class="recommend"')
	content2 = content[0:splitnum]
	content2 = html2text(content2)
	#print(content2)
	content2 = clean_text(content2)
	print(content2)
	title = html2text(str(row['ArticleTitle']))
	title = clean_text(title)
	#print(row['ArticleNumber'])
	#row['Date'])
	cursor.execute("insert into Text5 (ArticleNumber,ArticleTitle,Content,Date) values(%s, %s, %s, %s)",(row['ArticleNumber'],title,content2,row['Date']))
	db.commit()
	#print(content2)

#print(title)
#print(content2)

