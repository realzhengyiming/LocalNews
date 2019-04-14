# 这个首先是创建一个可以爬取url列表的方法，大体流程都是这样子的，可以复用的部分就不管。
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time

class SinaUrls(object):
    pass
    def __init__(self):
        pass

    def getUrlList(self,url):
        # coding=utf-8
        # 导包
        from selenium import webdriver
        import time

        if __name__ == '__main__':
            from selenium.webdriver.chrome.options import Options
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--headless')
            driver = webdriver.Chrome(chrome_options=chrome_options)
            driver.get(url)


            title = driver.title
            # list = driver.find_element_by_xpath('//a[@target="_blank"]')
            # print(title)
            urlList = []  # 一个页面上的所有的url都在这儿了。
            for link in driver.find_elements_by_xpath('//a[@target="_blank"]'):
                tempUrl = link.get_attribute('href')
                if tempUrl=="http://news.sina.com.cn/guest.html":
                    pass
                else:
                    urlList.append(tempUrl)   # 难怪你会那么的抉择。
                    print(link.get_attribute('href'))

            # print( list )
            # print(list.text)

            # 翻页按钮在哪儿，结合进去。
            print("下一页的链接在这儿。")

            # //*[@id="d_list"]/div/span[15]/a
            html = driver.page_source
            # driver.save_screenshot('baidu1.png')
            print(html)
            return driver.page_source


        pass

    def check(self,url):
        # coding=utf-8
        import time
        from selenium import webdriver

        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.implicitly_wait(6)
        driver.get(url)
        # time.sleep(1)

        for link in driver.find_elements_by_xpath("//*[@href]"):
            print(link.get_attribute('href'))
        driver.quit()

    def byApi(self,url):
        pass
        response = requests.get(url)
        print(response.text)
        from pprint import pprint
        pprint(BeautifulSoup(response.text,'lxml'))



if  __name__  == '__main__':
    pass
    testSina = SinaUrls()

    url = "http://www.baidu.com"

    urlSina = "https://news.sina.com.cn/roll/#pageid=153&lid=2509&k=&num=50&page=1"


    urltest = "https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page=2&r=0.2212089653320295&callback=jQuery111207469187819386303_1554713485795&_=1554713485824"
    # testSina.getUrlList(urlSina)
    # testSina.check(url)
    testSina.byApi(urltest)

    # 这个下面开始是单元的测试地方。
