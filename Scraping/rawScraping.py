#library call
import sys
import re
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
from lxml import etree
import MySQLdb

# db 연결하고 인코딩 부분
db = MySQLdb.connect(host="localhost", user ="ice-kms", passwd="kkms1234", db="scraping", charset="utf8") 
db.set_character_set('utf8')

cursor = db.cursor()


#00은 정치라는 의미
TARGET_URL_BEFORE_PAGE_NUM = "http://news.donga.com/List/Politics?p="
TARGET_URL_REST = '&prod=news&ymd=&m='

def get_link_from_news_title(page_num, URL, output_file):
	for i in range(page_num):
		current_page_num = 56305 + i*20
		position = URL.index('=')
		URL_with_page_num = URL[: position+1] + str(current_page_num) \
				+ URL[position+1 :]
		try:
			source_code_from_URL = urllib.request.urlopen(URL_with_page_num)
			soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
			for title in soup.find_all('div', 'articleList'):
				for title in soup.find_all('div','thumb'):
					title_link = title.select('a')
					article_URL = title_link[0]['href']
					get_text(article_URL, output_file)
		except:
			pass
		#soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
		#for title in soup.find_all('p', 'title'):
		#	title_link = title.select('a')
		#	article_URL = title_link[0]['href']
		#	get_text(article_URL, output_file)

def get_text(URL, output_file):
	source_code_from_url = urllib.request.urlopen(URL)
	soup = BeautifulSoup(source_code_from_url, 'lxml', from_encoding='utf-8')
	#[s.extract() for s in soup('script')]
	for script in soup(["script"]):
		script.extract()
	for strong in soup(["strong"]):
		strong.extract()
	#for recommend in soup(["recommend"]):
	#	recommend.extract()
	#or photo in soup(["articlePhotoC"]):
	#	photo.extract()

	text = ''
	for item in soup.find_all('div', 'article_title'):
		title = item.select('h2')
	for item in title:
		#title1 = str(item.find_all(text=True))
		title1 = str(item)
	#	text = text + str(item.find_all(text=True)) + '\t'
		
	for item in soup.find_all('div','title_foot'):
		for item in soup.find_all('span','date01'):
			date = str(item.find_all(text=True))
			date =date[5:21]
			break
	for span in soup(["span"]):
                span.extract()
	for item in soup.find_all('div', 'article_txt'):
                #for item in soup.find_all('span','inspace_pos'):
		#print(len(item))
		#print(item)
		content1 = str(item)
        #       text = text + str(item.find_all(text=True)) + '\r\n'

	#title1 = clean_text(title1)
	print(title1)
	#print(content1)
#	content1 = str(content1.find_all(text=True))
	#print(content1)
	#print(date)
	cursor.execute("insert into Raw (ArticleTitle,Content,Date) values(%s, %s, %s)",(title1,content1,date))
	db.commit()
	#result_text = clean_text(text)
	#output_file.write(result_text)

def clean_text(text):
	cleaned_text = re.sub('[a-zA-Z]', '', text)
	cleaned_text = re.sub('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]', '', cleaned_text)
	return cleaned_text

def main(argv):
	#예외처리
	if len(argv) != 3:
		print("python3 [module] [pagenum] [output]")
		return

	#형변환
	page_num = int(argv[1])
	output_file_name = argv[2]

	#이걸 왜 지금 합치지?
	target_URL = TARGET_URL_BEFORE_PAGE_NUM + TARGET_URL_REST

	#출력 파일 열기
	output_file = open(output_file_name, 'w')

	#인자 넘겨주기
	get_link_from_news_title(page_num, target_URL, output_file)

	output_file.close()
	db.close()

if __name__ == '__main__':
	main(sys.argv)	
