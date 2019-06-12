# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

class Spider(object):
    '''
    链家房源信息爬虫
    '''

    def __init__(self,url):
        self.home_list = []
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'])
        self.browser = webdriver.Chrome(options=options)
        self.browser.get(url)
        self.wait = WebDriverWait(self.browser, 5, 0.2)

    def get_one_page(self,html=None):
        '''
        获取单个页面的房源信息
        :param html: 当前页面的html代码
        :return:
        '''
        html = BeautifulSoup(html,'lxml')
        homes = html.find_all(class_='info clear')
        key_list = ['title','address','houseInfo','positionInfo',
                    'followInfo','totalPrice','unitPrice','tag']
        for h in homes:
            home = {}
            for key in key_list:
                if key == 'tag':
                    tag = h.find(class_='tag').find_all('span')
                    home[key] = [i.text for i in tag if i.text != '']
                elif key in ['title','address']:
                    h.find(class_=key).a.text
                else:
                    home[key] = h.find(class_=key).text
            self.home_list.append(home)
        print(len(self.home_list))

    def click_page(self,num):
        '''
        点击页码更换页面
        :param num: 页码数
        :return:
        '''
        btu = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT,str(num))))
        btu.click()

    def save(self):
        '''
        保存到数据库，所有数据在self.home_list中
        根据自己用的数据库，修改这个函数
        :return:
        '''
        return

    def run(self):
        '''
        启动函数
        :return:
        '''
        btu = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, '二手房')))
        btu.click()
        self.wait.until(EC.presence_of_element_located(locator=(By.LINK_TEXT, '网站地图')))
        time.sleep(3)
        self.browser.switch_to.window(self.browser.window_handles[1])
        for i in range(1,101):
            if i != 1:
                self.click_page(i)
                time.sleep(1)
            html = self.browser.page_source
            self.get_one_page(html)


if __name__ == '__main__':
    url = "https://wh.lianjia.com/"
    spider = Spider(url=url)
    spider.run()



