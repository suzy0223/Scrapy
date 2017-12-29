#-*- coding:utf8 -*-
#!/Downloads/douban.py
#filename:douban.py
#get the thumbnail of the book of literature
#Date:11-28-2016

import socket
import threading
import urllib
import urllib2
from lxml import etree
from multiprocessing.dummy import Pool
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#定义锁
lock = threading.Lock()

#获取网页，如果页面有内容返回页面，如果页面没内容直接异常退出
def getpage(url):
	req = urllib2.Request(url)
	req.add_header('User_Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0')
	try:
		page = urllib2.urlopen(req)
		return page.read()
	except Exception:
		return None


#判断一个页面是否有内容，根据页面下部的下一页是否有内容来判断，页面有内容、
#页面就有下一页，页面没有内容，就没有下一页
def isvalid(page):
	content = etree.HTML(page)
	xpath = '//*[@class="paginator"]/a/@href'
	element = content.xpath(xpath)
	
	if element:
		return True
	else:
		return False
#对每一个页面进行解析，获取每本图书封面urllist,返回一个页面的图书urllists和title
def parse(page):
	result = []
	title =[]
	prefix = "https://img3.doubanio.com/lpic/"
	content = etree.HTML(page)
	xpath = '//*[@id="subject_list"]/ul/li/div/a/img/@src'
	tipath ='//*[@id="subject_list"]/ul/li/div[2]/h2/a/@title'
	element = content.xpath(xpath)
	tit = content.xpath(tipath)
	print element
	print tit


	title.extend(tit)	
	for item in element:
		resu = item.split('/')[-1]
		url = prefix + resu
		result.append(url)
	

	return (result,title)

#将文件下载到当前目录下的downloaded子目录
def download(value):
	socket.setdefaulttimeout(120)
	url,name = value
	lock.acquire()
	if not os.path.exists('downloaded'):
		os.mkdir('downloaded')
	lock.release()
	filename = './downloaded/' + name+'.jpg'
	try:
		if url:
			urllib.urlretrieve(url,filename)
	except Exception:
		pass
	print '{} downloaded'.format(name,)

#使用线程池下载程序
def parallel(threadnum,func,para):
	pool=Pool(threadnum)
	pool.map(func,para)
	pool.close()
	pool.join()

	print "task done!"
	

#主程序
def main():
#第一阶段：获取豆瓣图书文学类图书封面的urllists，将结果存储在result中
	result=[]
	title=[]
	prefix = 'https://book.douban.com/tag/%E6%96%87%E5%AD%A6'
	startnum =0 
	while startnum<(98*20):
		pageurl = prefix+'?start='+str(startnum)+'&type=T'
		page = getpage(pageurl)
		if (page!=None):
			if isvalid(page):
				resu,tit = parse(page)
				#print resu
				result.extend(resu)
				title.extend(tit)
				startnum+=20
			else:
				break
		else:
			break
	print len(result)
	print len(title)

#第二阶段：使用100线程池塘下载文件
	parallel(100,download,zip(result,title))
	#for item in zip(result,title):
	#	download(item)

if __name__=="__main__":
	main()


	
