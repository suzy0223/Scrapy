#coding=utf-8
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os

source_url = "https://91baby.mama.cn/thread-1505059-1-1.html?so_param=5LiN6KaB54mp56eN5q2n6KeGfGJhYnk5MV8xNTA1MDU5fDF8MXwxOQ=="

browser = webdriver.Chrome()

def getPage(source_url):

    html = []
    browser.get(source_url)
    soup = BeautifulSoup(browser.page_source, "lxml")
    html.append(soup)
    flag = True

    while flag ==True:

        try:
            browser.find_element_by_xpath("//a[contains(text(),'下一页')]").click()
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source,"lxml")
            html.append(soup)

        except:
            flag = False

    return html

def getText(html):

    postlist = html.find(attrs={"id":"postlist"})
    post = postlist.find_all(attrs={"class":"t_f"})
    text = []
    for i in post:
        text.append(i.get_text())

    return text


h = getPage(source_url)
browser.close()

try:
    fo = open("不要物种歧视.txt","a")
except:
    os.mkdir("不要物种歧视.txt")

for i in h:
    tx = getText(i)
    for j in tx:
        j = j.encode('utf8')
        fo.write(j)

fo.close()

