import urllib.error
from bs4 import BeautifulSoup
import requests


class Qiushibaike(object):

    def start(self,page):
        url = 'http://www.qiushibaike.com/hot/page/' + str(page)

        html = ''
        try:
            html = requests.get(url)
        except urllib.error.HTTPError as e:
            if hasattr(e,'code'):
                print(e.code)
            if hasattr(e,'reason'):
                print(e.reason)
        soup = BeautifulSoup(html.content,'lxml')
        content = self.content(soup)
        for i in content:
            print(i)

    def content(self,soup):
        for i in soup.find_all('div',class_='article block untagged mb15 typs_long'):
            url = 'http://www.qiushibaike.com' + i.find('a',class_='contentHerf')['href']
            content = self.more(url)
            if content:
                yield content
        for i in soup.find_all('div',class_='article block untagged mb15 typs_hot'):
            content = i.span.string
            if content:
                yield content

    def image(self):
        '''
        当存在图片时
        :return:
        '''
        return

    def more(self,url):
        '''
        当有更多文字信息时
        :return:返回文章总体内容
        '''
        html = requests.get(url)
        soup = BeautifulSoup(html.content,'lxml')
        content = soup.find('div',class_='content')
        return content.string



if __name__ == '__main__':
    Qiushibaike().start(page=2)