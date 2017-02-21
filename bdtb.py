#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2

import re
from bs4 import BeautifulSoup


# 处理页面标签类
class Tool:
    # 去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        # strip()将前后多余内容删除
        return x.strip()


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
        soup = BeautifulSoup(page, 'lxml')
        items = soup.find_all('div', class_='d_post_content')
        print self.tool.replace((items[0]).get_text())
        # for item in items:
        #     print(item)


baseUrl = 'http://tieba.baidu.com/p/3138733512'
bdtb = BDTB(baseUrl, 1)
bdtb.getContent(bdtb.getPage(1))
