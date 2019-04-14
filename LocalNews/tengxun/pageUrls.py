import gzip
import json
import random
import urllib.request
from urllib import parse

import time

import chardet
import requests
from tengxun.pageContent import pageContent

from DBcontrol import DB
from TimeHelper import TimeHelper
from makebeautifulSoup import makeBS

#todo 排错的时候这儿的mysql操作给我停止了，耦合性好高。混合在一个起了，
class DateUrl:
    def __init__(self):
        self.dbhelper = DB()                #默认就给你创建好了，
#这个是按天来的，组合一下就行了,获取滚动列表的新闻url

    def getDateUrlList(self,startDate,endDate): #返回这两个日期区间的url,顺便就写入数据库了


        urlList =[]
        timehelper=TimeHelper()
        datelist = []
        if(startDate!=endDate):  #不相等的时候就算差值
            datelist = timehelper.getTimeList(startDate,endDate)
        else:
            datelist.append(startDate)
        for oneDay in datelist:
            time.sleep(1.5) #500毫秒一次，那我设置成800毫秒请求一次
            onedatelist=[]
            try:
                onedatelist = self.getOneDayNewUrl(oneDay)
            except Exception:
                time.sleep(30)
                onedatelist = self.getOneDayNewUrl(oneDay)
            urlList = urlList+onedatelist

            # todo 这样并不好，耦合性太高了，不方便平时的调试排错，融合进去了这些东西
            # self.saveListToMysql(onedatelist,oneDay,"tengxun")  #存到数据库里面去，把每个都插入进去
        return urlList

    def getOneDayNewUrl(self, date):
        date = parse.quote_plus(""+date)
        oneDayUrlList = []
        print(str(date))
        # date = "2018-07-26"
        appid = "3639833dae924cb9efb6ba30e6c5a6fa"
        url = "https://api.shenjian.io/?appid=" + appid + "&date=" + date
        # print(url)
        request = urllib.request.Request(url,
        headers={
            "Accept-Encoding": "gzip",
        })

        response = urllib.request.urlopen(request)
        gzipFile = gzip.GzipFile(fileobj=response)
        # print(gzipFile.read().decode('UTF-8'))
        jsonResult = json.loads(str(gzipFile.read().decode('UTF-8')))
        if "data" in jsonResult:
            print (jsonResult['data'])
            print("共有多少个新闻" + str(len(jsonResult['data'])))
            if(len(jsonResult['data'])==4):
                oneDayUrlList.append(jsonResult['data']['url'])
                return oneDayUrlList
            else:
                for i in jsonResult['data']:
                    # print(i['url'])
                    oneDayUrlList.append(i['url'])
                return oneDayUrlList
        else :
            print("检测到腾讯的api 中无  data key 10分钟后再试")
            time.sleep(60*10)  #如果一下子那个api没有反应的话，那就这样操作咯，用进程把，多个cpu哦
            return self.getOneDayNewUrl(date)  #采用递归的方式来处理，，
    #
    # def saveListToMysql(self,lists,date,fromWhere):
    #     connect = DB()
    #     lists = list(set(lists))
    #     for i in lists:
    #         connect.insertTenxun(i,date,fromWhere)
    #     print(fromWhere+"插入完毕")
        # connect.__close__()
    def tengxunGundong(self):
        url = 'http://news.qq.com/articleList/rolls/'
        cooker = makeBS()
        soup = cooker.makesoup(url,"computer")

        print(soup)

# -----------------------------------------------------下面开始是新的提取出页面的url的-----------------------------------

    def returnThemeCode(self,theme):
        ent_Theme = 1537876288634
        sport_Theme = 1537877689177
        finance_Theme = 1537878365483
        tech_Theme = 1537879684280
        auto_Theme = 1537887032223
        house_Theme = 1537887128904
        news_Theme = 1537874915062

        if theme == 'news':
            return news_Theme
        if theme == 'ent':
            return ent_Theme
        if theme == 'sports':
            return sport_Theme

        if theme == 'tech':
            return tech_Theme
        if theme == 'auto':
            return auto_Theme
        if theme == 'house':
            return house_Theme
        if theme == 'finance':
            return finance_Theme


    def getThemeUrl(self,theme, today, pageNumber):
        rawUrl = "http://roll.news.qq.com/interface/cpcroll.php"
        rawReferer = '.qq.com/articleList/rolls/'  # 'http://news   前面还有这个东西

        my_headers = [
            'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30',
            'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)',
            'Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)']

        headers = {"User-Agent": random.choice(my_headers), 'Referer': 'http://' + theme + rawReferer}  # 默认值

        rawUrl = rawUrl + "?callback=rollback&mode=1&cata=&_=" + str(self.returnThemeCode(theme)) + "&site=" + theme + "&page=" + str(pageNumber) + "&date=" + today
        try:
            rawhtml = requests.get(rawUrl, headers=headers, allow_redirects=False,
                                   timeout=30)  # 一般提取文本的话，那就用text，如果是文件就content
            rawhtml.encoding = chardet.detect(rawhtml.content)['encoding']

            print(rawhtml.url)
            print("状态码" + str(rawhtml.status_code))

            if rawhtml.status_code == 504:
                print(504)
                return
            print("页面的读取结果为")
            print(rawhtml.text)
            if rawhtml.text.find('rollback') == 0:
                jsonString = rawhtml.text.split("rollback")[1]  # 把js提取出来就可以了
            else:
                jsonString = rawhtml.text
            print(jsonString)
            dicData = eval(jsonString)
            print(type(jsonString))
            print(jsonString)
            # print(dicData['data']['article_info'])
            print(len(dicData['data']['article_info']))
            if dicData['data'] == "":
                print("超过了最大页数了，跳出了就可以了")
                return
            urllist = []
            for one in dicData['data']['article_info']:
                # print(one['url'])
                print(one['url'].replace("\\", "/"))  # 还需要检查一下这个和之前的那种野蛮是不是一样的
                urllist.append(one['url'].replace("\\", "/"))
            return urllist
        except Exception as e:
            # print(e)
            return []  # 没有东西诶

    def pageUrlMain(self,date):                             #汇总到这儿来,输入日期就可以返回这个了

        # todo 这些都还可能是 page2的情况
        # url    ="http://roll.news.qq.com/interface/cpcroll.php?callback=rollback&site=news&mode=1&cata=&date=2018-09-25&page=1&_=1537850539512"
        # 这个是时政新闻
        urlNew = "http://roll.news.qq.com/interface/cpcroll.php?callback=rollback&site=news&mode=1&cata=&date=2018-09-25&page=1&_=1537874915062"
        # 这儿是国际标题， referer = http://news.qq.com/articleList/rolls/
        urlEnt = "http://roll.news.qq.com/interface/cpcroll.php?callback=rollback&site=ent&mode=1&cata=&date=2018-09-25&page=1&_=1537876288634"  # referer = http://ent.qq.com/articleList/rolls/
        # referer = http://ent.qq.com/articleList/rolls/
        urlSport = "http://roll.news.qq.com/interface/cpcroll.php?callback=rollback&site=sports&mode=1&cata=&date=2018-09-25&page=1&_=1537877689177"  # r这个好像而是动态加载出来的，真是的
        # todo 这个要重新解析，可能是动态的 referer = http://sports.qq.com/articleList/rolls/    有些page可能不止一个的，都有   体育的是动态的，待会回来再分析，有好多页，很厉害的样子呢
        # 不同的theme要切换不同的referer
        urlFinance = "http://roll.news.qq.com/interface/cpcroll.php?callback=rollback&site=finance&mode=1&cata=&date=2018-09-25&page=1&_=1537878365483"
        # referer http://finance.qq.com/articleList/rolls/
        # todo 默认的解析可以，但是好慢，使用代理的情况下 http://173.255.210.215:8000/?count=6&country=%E5%9B%BD%E5%86%85
        urlTech = "http://roll.news.qq.com/interface/cpcroll.php?callback=rollback&site=tech&mode=1&cata=&date=2018-09-25&page=2&_=1537879684280"
        # referer = http://tech.qq.com/articleList/rolls/
        # todo 这个也是偶尔有点慢的样子， 使用代理 下

        urlAuto = "http://roll.news.qq.com/interface/cpcroll.php?callback=rollback&site=auto&mode=1&cata=&date=2018-09-25&page=1&_=1537887032223"
        # referer 这个是汽车的  http://auto.qq.com/articleList/rolls/dai'li
        # todo 这个汽车的应该使用另外的解析来解析才可以

        urlHouse = "http://roll.news.qq.com/interface/cpcroll.php?callback=rollback&site=house&mode=1&cata=&date=2018-09-25&page=1&_=1537887128904"
        # referer http://house.qq.com/articleList/rolls/   这个是房产的 可以解析
        # getThemeUrl(urlSport,"http://sports.qq.com/articleList/rolls/")
        urlRaw = "http://roll.news.qq.com/interface/cpcroll.php?"  # 带参数进行post请求才对把
        # print(jsonDic)

        # print(rawhtml.json())

        oneUrl = {}  # 单单一个运动的就够了
        themeList = ['news', 'ent', 'tech', 'auto', 'house', 'finance', 'sports']   #一共有7个主题，其实不止这7个的，真好。
        tempList =[]
        #想想用什么数据类型。二维数组？url,theme, 都是字符串

        for theme in themeList:
            print("第一个主题是")
            for i in range(1, 11):
                print("第" + str(i) + "页")
                responseList = self.getThemeUrl(theme, date, i)  # 这儿只是测试最大页数有多少而已
                if len(responseList) == 0:
                    print("最大页数为" + str(i - 1) + "页")
                    break
                else:
                    tempList = tempList+responseList
                    oneUrl[theme]=responseList   #这样不就可以了，分开来
                print(oneUrl)
        resultUrl = oneUrl
        tempList = set(tempList)

        from pprint import pprint
        pprint(resultUrl)
        print(len(resultUrl))  # 目前可以返回653    昨天的 完整的1140，数量是很可观的
        #写一个函数分类存就可以了  ，本来是一起存的，现在

        self.dbhelper.saveDicToMysql(oneUrl,date,"tengxun")

        #这边不需要分类，可能是因为这个切换了又没放回去的原因
        # resultUrl = self.dbhelper.saveListToMysql(resultUrl,date,"tengxun")   #这儿没啥去重的  #保存到mysql中去先,这样就可以重复使用拉
                                                                    #经过去重，去掉已经插入过的东西，然后再返回去 ，这儿还得转会list才可以。
        return tempList   #直接这儿去重后



#提取到的url先存到数据库里面去
if __name__ == "__main__":
    newUrl = DateUrl()
    print(newUrl.pageUrlMain("2019-04-06"))
    pass
    # dateurl = DateUrl()
    # print("共提取到新闻url的数量有")
    # newslist = []

    # allUrl = dateurl.getDateUrlList("2018-09-13","2018-09-13")
    # print(len(allUrl))
# print(dateurl.getOneDayNewUrl("2018-07-30"))  #一天就用这个啊
#     for i in range(5):
#         newslist =newslist+ dateurl.getOneDayNewUrl("2018-09-23")   #因为是滚动新闻，所以应该说会实时的不一样，那么怎么办，每分钟刷新一次吗
#         time.sleep(60)
#     newslist.sort()
#     print((len(newslist)))   #才21条。。。。

    # dateurl.tengxunGundong()
    # pageContent()

    # dateUrl = DateUrl()                        #2018-09-27 日编辑
    # pageUrlMain   =dateUrl.pageUrlMain("2018-10-05")
    # print(len(pageUrlMain))

    #2018-10-05  test 直接打开，用收集ua来打开页面

    # html  = dateUrl.

