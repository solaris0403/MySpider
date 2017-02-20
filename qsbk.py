# -*- coding:utf-8 -*-
import urllib2
from bs4 import BeautifulSoup


class Comedy(object):
    def __init__(self, name, number, content):
        self.name = name
        self.number = number
        self.content = content


class QSBK(object):
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}
        self.stories = []
        self.enable = False

    def getPage(self, pageIndex):
        url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
        try:
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            content = response.read().decode('utf-8')
            return content
        except urllib2.URLError, e:
            if hasattr(e, 'code'):
                print(e.code)
            if hasattr(e, 'reason'):
                print(e.reason)
            return None

    def getPageItems(self, pageIndex):
        pageContent = self.getPage(pageIndex)
        if not pageContent:
            print('页面加载失败...')
            return None
        soup = BeautifulSoup(pageContent, 'lxml')
        items = soup.find_all('div', class_="article block untagged mb15")
        pageStories = []
        for item in items:
            name = item.find('h2').text
            content = item.find('div', class_="content").text
            number = item.find('span', class_='stats-vote').find('i', class_='number').text
            comedy = Comedy(name, number, content)
            pageStories.append(comedy)
        return pageStories

    def loadPage(self):
        if self.enable and len(self.stories) < 2:
            pageStories = self.getPageItems(self.pageIndex)
            if pageStories:
                self.stories.append(pageStories)
                self.pageIndex += 1

    def getOneStory(self, pageStories, page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == "Q" or input == 'q':
                self.enable = False
                return
            print u"第%d页\t发布人:%s\t赞:%s\n%s" % (page, story.name, story.number, story.content)

    def start(self):
        print u"正在读取糗事百科,按回车查看新段子，Q退出"
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStories, nowPage)


spider = QSBK()
spider.start()
