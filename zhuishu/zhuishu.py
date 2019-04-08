import urllib.request
import urllib.parse
import json

# target = input('输入要搜索的书籍名称:')
# start = input('输入搜索起始:')
# limit = input('输入搜索结束:')

class ZhuishuSpider(object):

    def __init__(self):
        # target = input('输入要搜索的书籍名称:')
        target = '晚钟'
        books,total = self.get_books(target)
        print('')
        result = self.parse_book(books)
        result = self.show_parse(books)
        for i in result:
            print(i)

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

    def show_parse(self,books):
        key_list = ['title','cat','author','wordCount','shortIntro','lastChapter']
        key2_list = ['名称','类型','作者','总字数','简介','最后章节']
        result = []
        for book in books:
            dic = {}
            for key, key2 in zip(key_list, key2_list):
                dic[key2] = book[key]
            result.append(dic)
        return result


    def parse_book(self,books):
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

        result = []
        for book in books:
            dic = {}
            for key,key2 in zip(key_list,key2_list):
                dic[key2] = book[key]
            result.append(dic)
        return result







if __name__ == "__main__":
    ZhuishuSpider()


