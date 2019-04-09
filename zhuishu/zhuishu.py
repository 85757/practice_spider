import urllib.request
import urllib.parse
import json
import requests
import os

class DownloadBook(object):

    def download(self,book):
        '''
        下载书籍
        :param book:
        :return:
        '''
        self.book = book
        self.file_path = os.path.dirname(__file__) + '/' + self.book['书籍名称']
        if not os.path.exists(self.file_path):  # 如果没有这个目录，创建它
            os.makedirs(self.file_path)
        book_directory = self.get_book_directory()
        for chapter in book_directory:
            self.save_chapter(chapter)
        print(self.book['书籍名称'], '已下载完毕！！！！')

    def get_book_directory(self):
        '''
        获取书籍目录列表
        :return: 返回书籍目录列表
        '''
        url = "http://api.zhuishushenqi.com/mix-toc/{book_id}?view=chapters".format(book_id=self.book['id'])
        html = requests.get(url)
        book_directory = json.loads(html.text)['mixToc']['chapters']
        return book_directory

    def save_chapter(self,chapter):
        '''
        保存单个章节内容
        :param chapter:单个章节的信息
        :return:
        '''
        print('正在下载：',chapter['title'])
        title = chapter['title'] + '.txt'
        link = chapter['link']
        content = chapter['title'] + '\n' + self.get_chapter_content(link)
        file_path = self.file_path + '/' + title
        with open(file_path,'w') as f:
            f.write(content)

    def get_chapter_content(self,link):
        '''
        获取单个章节的内容
        :return: 单个章节的内容
        '''
        link = urllib.parse.quote(link)
        url = 'http://chapter2.zhuishushenqi.com/chapter/' + link
        html = requests.get(url)
        content = json.loads(html.text)['chapter']['body']
        return content


class ZhuishuSpider(object):

    def __init__(self):
        self.download = DownloadBook()
        # target = input('输入要搜索的书籍名称:')
        target = '晚钟'
        books,total = self.get_books(target)
        print('*' * 50)
        print('相关书籍数：',str(total))
        print('*' * 50)
        result = self.parse_book(books)
        # 显示搜索到的相关书籍
        key_list = ['编号','书籍名称','类型','作者','总字数','简介','最后章节']
        for i in result:
            for key in key_list:
                print(key,':',i[key])
            print('\n')
        # 选择要下载的书籍
        num = input('选择要下载的书籍编号:')
        for i in result:
            if i['编号'] == int(num):
                self.download.download(i)

    def get_books(self,target,start=0,limit=10):
        '''
        模糊搜索与书籍名称相近的书籍
        :param target: 书籍名称
        :param start: 起始
        :param limit: 数量
        :return:
        '''
        target = urllib.parse.quote(target)
        if not start or not limit:
            url = "http://api.zhuishushenqi.com/book/fuzzy-search?query={target}".format(target=target)
        else:
            url = "http://api.zhuishushenqi.com/book/fuzzy-search?query={target}&start={start}&limit={limit}".format(
                target=target, start=start, limit=limit)
        respose = urllib.request.urlopen(url)
        html = respose.read()
        html = json.loads(html)
        return html['books'],html['total']

    def parse_book(self,books):
        '''
        从API接口获取到的书籍详细信息
        :param books:所有相关书籍
        :return:解析后的书籍相关信息
        '''
        key_list = ['_id','hasCp','title','aliases','cat','author','cover','shortIntro',
                    'lastChapter','retentionRatio','banned','allowMonthly',
                    'latelyFollower','wordCount','contentType','superscript','sizetype',
                    'highlight']
        key2_list = ['id','','书籍名称','','类型','作者','图片链接','简介','最后章节','','',
                     '','','总字数','文件类型','','','']
        # _id:书籍id
        # hasCp:
        # title:书籍名称
        # aliases:
        # cat:类型
        # author:作者
        # cover:图片链接
        # shortIntro:简介
        # lastChapter:最后章节
        # retentionRatio:
        # banned：
        # allowMonthly:
        # latelyFollower:
        # wordCount:总字数
        # contentType:文件类型
        # superscript:
        # sizetype:
        # highlight：
        num = 1
        result = []
        for book in books:
            dic = {}
            dic['编号'] = num
            for key,key2 in zip(key_list,key2_list):
                dic[key2] = book[key]
            result.append(dic)
            num += 1
        return result


if __name__ == "__main__":
    ZhuishuSpider()


