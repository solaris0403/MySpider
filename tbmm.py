#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import urllib
import urllib2
from bs4 import BeautifulSoup

from tool import Tool


class Pretty(object):
    def __init__(self):
        pass


class Spider:
    def __init__(self):
        self.site = 'http://mm.taobao.com/json/request_top_list.htm'
        self.tool = Tool()

    def getPage(self, pageIndex):
        url = self.site + '?page=' + str(pageIndex)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        content = response.read().decode('gbk')
        return content

    def getContent(self, pageIndex):
        pretties = []
        content = self.getPage(pageIndex)
        soup = BeautifulSoup(content, 'lxml')
        items = soup.find_all('div', class_='list-item')
        for item in items:
            pretty = Pretty()
            pretty.name = item.find('a', class_='lady-name').get_text()
            pretty.site = item.find('a', class_='lady-avatar').get('href')
            pretty.avatar = item.find('a', class_='lady-avatar').find('img').get('src')
            pretty.age = item.find('strong').get_text()
            pretty.address = item.find_all('span')[0].get_text()
            pretties.append(pretty)
            print('name:\t' + pretty.name)
            print('site:\t' + pretty.site)
            print('avatar:\t' + pretty.avatar)
            print('age:\t' + pretty.age)
            print('address:\t' + pretty.address + '\n')
        return pretties

    def saveImg(self, imageUrl, fileName):
        u = urllib.urlopen(imageUrl)
        date = u.read()
        f = open(fileName, 'wb')
        f.write(date)
        f.close()

    def saveBrief(self, content, name):
        fileName = name + "/" + name + ".txt"
        f = open(fileName, 'w+')
        print('正在保存' + fileName)
        f.write(content.decode('utf-8'))

    def mkdir(self, path):
        path = path.strip()
        isExits = os.path.exists(path)
        if not isExits:
            os.mkdir(path)
            return True
        else:
            return False


spider = Spider()
spider.getContent(1)
