#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2

from bs4 import BeautifulSoup

# 百度贴吧
from tool import Tool


class Post(object):
    def __init__(self, floor=1, author='', time='', content=''):
        self.__floor = floor
        self.__author = author
        self.__time = time
        self.__content = content

    def getFloor(self):
        return self.__floor

    def setFloor(self, floor):
        self.__floor = floor

    def setAuthor(self, author):
        self.__author = author

    def getAuthor(self):
        return self.__author

    def setTime(self, time):
        self.__time = time

    def getTime(self):
        return self.__time

    def setContent(self, content):
        self.__content = content

    def getContent(self):
        return self.__content


class BDTB(object):
    def __init__(self, baseUrl, seeLZ=0):
        self.baseUrl = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.tool = Tool()

    def getPage(self, pageIndex):
        try:
            url = self.baseUrl + self.seeLZ + '&pn=' + str(pageIndex)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            content = response.read().decode('utf-8')
            return content
        except urllib2.URLError, e:
            if hasattr(e, 'code'):
                print(e.code)
            if hasattr(e, 'reason'):
                print(e.reason)
            return None

    def getTitle(self):
        page = self.getPage(1)
        soup = BeautifulSoup(page, 'lxml')
        soup_title = soup.find('h3', class_='core_title_txt')
        if soup_title:
            return soup_title.text.strip()

    def getPageNumber(self):
        page = self.getPage(1)
        soup = BeautifulSoup(page, 'lxml')
        soup_page = soup.find('li', class_='l_reply_num')
        page_number = soup_page.find_all('span', class_='red')
        number = page_number[-1]
        if number:
            return number.get_text()

    def getContent(self, page):
        posts = []
        soup = BeautifulSoup(page, 'lxml')
        items = soup.find_all('div', class_='l_post')
        for item in items:
            floor = item.find_all('span', class_='tail-info')[-2].get_text()
            author = item.find('a', class_='p_author_name').get_text()
            time = item.find_all('span', class_='tail-info')[-1].get_text()
            content = self.tool.replace(item.find('div', class_='d_post_content').get_text())
            post = Post(floor=floor, author=author, time=time, content=content)
            posts.append(post)
        return posts


baseUrl = 'http://tieba.baidu.com/p/3138733512'
bdtb = BDTB(baseUrl, 0)
for post in bdtb.getContent(bdtb.getPage(1)):
    print('%s\n%s\t%s\n%s\n' % (post.getFloor(), post.getTime(), post.getAuthor(), post.getContent()))
