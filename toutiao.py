import requests
import os
import json
import time
import urllib.parse
import urllib.request

class ToutiaoImageSpider():

    def __init__(self):
        self.file_path = os.path.dirname(__file__) + '/toutiao/'
        keyword = input('输入需要查询的内容：')
        self.keyword = urllib.parse.quote(keyword)
        self.offset = str((int(input('爬取第几页的图片：'))-1) * 20) # 偏移量
        self.url = "https://www.toutiao.com/api/search/content/" \
                   "?aid=24&app_name=web_search&offset={offset}" \
                   "&format=json&keyword={keyword}" \
                   "&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab" \
                   "&pd=synthesis&timestamp={timestamp}"

    def download(self):
        '''
        下载图片
        :return:
        '''
        timestamp = str(round(time.time() * 1000))
        url = self.url.format(offset=self.offset,keyword=self.keyword,timestamp=timestamp)
        html = requests.get(url)
        data = json.loads(html.content)
        for i in data['data']:
            self.save_image(i)

    def save_image(self,data):
        '''
        下载单个新闻的图片
        :return:
        '''
        try:
            title = data['title']
            file_path = self.file_path + '/' + title + '/'
            if not os.path.exists(file_path):  # 如果没有这个目录，创建它
                os.makedirs(file_path)
            image_list = data['image_list']
            for url in image_list:
                image = url['url'].split('/')[-1]
                urllib.request.urlretrieve(url['url'],file_path + '%s.jpg'%image)
        except KeyError:
            pass


if __name__ == '__main__':
    ToutiaoImageSpider().download()



