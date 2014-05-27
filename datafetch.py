# this is a program could automatically fetch data and create databases

from selenium import webdriver
import os
import time
import sys
import sqlite3

#start the browser depend on the specific profile
#and install the webcrawler extension

def run_browser():
	profile_1 = webdriver.FirefoxProfile('/home/zhangyoufu/profile_1/')
	extension = webdriver.FirefoxProfile.add_extension(profile_1,'/home/zhangyoufu/WebCrawler/crawler.xpi')
	browser = webdriver.Firefox(profile_1)
	#check if the program run correctly
	time.sleep(60)
	statinfo = os.stat('/home/zhangyoufu/profile_1/httpfox.sqlite')
	file_size = statinfo.st_size 
	# if open again, the add-on would cover it.
	while file_size < 100:
		browser.quit()
		profile_1 = webdriver.FirefoxProfile('/home/zhangyoufu/profile_1/')
		#extension = webdriver.FirefoxProfile.add_extension(profile_1,'/home/zhangyoufu/WebCrawler/crawler.xpi')
		browser = webdriver.Firefox(profile_1)
		time.sleep(60)

	time.sleep(50000)
	browser.quit()



#change extension: each time give url_list a list of 500 urls

def change_extension():
	os.chdir('/home/zhangyoufu/Downloads/addon-sdk-1.16/')
	os.system('source bin/activate')

	os.chdir('/home/zhangyoufu/WebCrawler/data/')
	os.system('rm url_list.txt')
	#each create a new url_list for 500 lines
	f = open('url_origin.txt','r')
	f_out = open('url_list.txt','w')
	flag = 0
	for line in f:
		flag++
		f.write(line)
		if (flag == 500):
			break
	f.close()

	os.system('cfx xpi')


# according to the number of databases to move to a certain directory

def move_db(num):
	os.chdir('/home/zhangyoufu/profile_1/')
	os.system('mv httpfox_sqlite /home/zhangyoufu/database1_merge/httpfox_' + str(num) + '.sqlite' )

# merge all the databases with same schema

def merge_db(num):
	os.chdir('/home/zhangyoufu/database1_merge/')
	for i in range(2,num):
		conn = sqlite3.connect('httpfox_1.sqlite3')
		c = conn.cursor()
		c.execute("attach 'httpfox_' + str(i) + '.sqlite' as toMerge")
		c.execute('BEGIN')
		c.execute('insert into http_request_headers select * from toMerge.http_request_headers')
		c.execute('insert into http_requests select * from toMerge.http_requests')
		c.execute('insert into pages select * from toMerge.pages')
		c.execute('commit')
		c.close()
		conn.close()

# each time update databases with the previous number of entries in that database

def update_db(num):
	os.chdir('/home/zhangyoufu/database1_merge/')
	for i in range(2,num):
		conn = sqlite3.connect("httpfox_ + str(i-1) +'.sqlite' ")
		c = conn.cursor()
		id_pages = c.execute('select id from pages where id = (select max(id) from pages)')
		id_request = c.execute('select id from http_requests where id = (select max(id) from http_requests)')
		id_headers = c.execute('select id from http_request_headers where id = (select max(id) from http_request_headers)')
		conn = sqlite3.connect("httpfox_ + str(i) +'.sqlite' ")
		c = conn.cursor()
		c.execute('UPDATE pages SET id = id + 10000000000')
		c.execute("UPDATE pages SET id = id - (1000000000 - '%d')" % id_pages)
		c.execute("UPDATE pages SET parent_id = parent_id + '%d'" % id_pages)

		c.execute('UPDATE http_requests SET id = id + 10000000000')
		c.execute("UPDATE http_requests SET id = id - (10000000000 - '%d')" % id_request)
		c.execute("UPDATE http_requests SET page_id = page_id + '%d'" % id_pages)

		c.execute('UPDATE http_request_headers SET id = id + 10000000000')
		c.execute("UPDATE http_request_headers SET id = id - (10000000000 - '%d')" % id_headers)
		c.execute("UPDATE http_request_headers SET http_request_id = http_request_id + '%d'" % id_request)
		

# main function
def main():
	#number is the total number of url_list
	number = 2880
	times = number/500 + 1
	for i in range(1,times):
		change_extension()
		run_browser()
		move_db(i)

	#update_db(times)
	#merge_db(times)

if __name__ == "__main__":
	main()







