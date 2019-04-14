import gzip
import json
import random

import chardet
import requests
import queue
from DBcontrol import DB
from TimeHelper import TimeHelper

#todo 得增加一个集合，用来存东西先，然后再去重，这样操作
from makebeautifulSoup import makeBS


class DateUrl:
    # def __init__(self):
    #     self.UrlList = []  #默认搞一个
    #     self.JINGXUAN = "T1467284926140"  #网易精选
    #     self.JINGXUAN_URL = "http://c.3g.163.com/nc/article/list/T1467284926140/0-40.html"
    #     self.TOUTIAO = "T1348647853363"   #网易头条
    #     self.TOUTIAO_URL  = "http://c.m.163.com/nc/article/headline/T1348647853363/0-40.html"
    #     self.YULE = "T1348648517839"      #网易娱乐
    #     self.YULE_URL = "http://c.3g.163.com/nc/article/list/T1348648517839/0-40.html"


#这个是按天来的，组合一下就行了,获取滚动列表的新闻url
    # def getDateUrlList(self,startDate,endDate): #这儿包括整合和写入数据库,输入起始和结束的日期，返回这些url 列表
    #     timehelper = TimeHelper()
    #     timeList =[]
    #     if startDate==endDate:
    #         timeList.append(startDate)
    #     else:
    #         timeList = timehelper.getTimeList(startDate, endDate)  # 获得这个日期间隔的列表，或者相同时就是当天的
    #
    #     allurlList = []
    #     for date in timeList:
    #         allurlList = allurlList+self.getJINGXUAN(date)
    #         self.saveListToMysql(allurlList, date)
    #
    #     return allurlList


    # def getTOUTIAO(self,date):
    #     pass
    #     result =self.wangyiMS("http://c.m.163.com/nc/article/headline/T1348647853363/0-40.html") #这样就可以了啦
    #     result =result['T1348647853363']
    #     allUrls = []
    #     for one in result:
    #         # print(one)
    #         if 'url_3w' in one.keys() and 'ptime' in one.keys():
    #             url = one['url_3w']
    #             time = one['ptime'].split(" ")[0]
    #             # print(one['url_3w'] +" "+one['ptime'].split(" ")[0])
    #             allUrls.append([url, time])
    #             # if(time!=date): #不等于最新的当天那个时间的话
    #             #     break
    #             # else:
    #             #     allUrls.append(url)
    #
    #     resultUrl = []
    #     for URL in allUrls:  # 这儿一般又多少条呢
    #         # print(URL[0])
    #         # print(URL[1])
    #         if URL[0] != "" and URL[1] == date:
    #             # print("fuck")
    #             resultUrl.append(URL[0])
    #     self.UrlList=self.UrlList+resultUrl
    #     return resultUrl

    # -----------------------------------新的放在这下面----------------------------------------------
    def mobiResponse(self,url):           #这个留着吧
        rollLatest = "http://news.163.com/latest/"
        # requestURL = "http://news.163.com/special/0001220O/news_json.js?0.3699326344116929"
        # requests.get(requestURL)
        # rawReferer = '.qq.com/articleList/rolls/'  # 'http://news   前面还有这个东西
        my_headers = [  # 这边为了得到直接的手机端的页面代码返回，直接使用手机ua
            'Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN',
            'Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 Mobile Safari/537.36 Maxthon/3047',
            # 'Mozilla/5.0 (iPhone 84; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14G60 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1',
            'Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; STF-AL00 Build/HUAWEISTF-AL00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.9 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; SM-C7000 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.6.2.948 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 7.0; STF-AL10 Build/HUAWEISTF-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.2.0_730_YYB_D QQ/7.2.0.3270 NetType/4G WebP/0.3.0 Pixel/1080']
        headers = {"User-Agent": random.choice(my_headers), 'Referer': "http://news.163.com/latest/"}  # 默认值
        try:
            rawhtml = requests.get(url, headers=headers, allow_redirects=False,             #跳转怎么是false
                                   timeout=30)  # 一般提取文本的话，那就用text，如果是文件就content
            rawhtml.encoding = "GBK"  ##gbk>gb2312   使用这种方式尚且还有乱码的情况，部分乱码，那就是gbk可以修复
            # print(chardet.detect(rawhtml.content)['encoding'])
            if rawhtml.status_code == 504:
                print(504)
                return
            # print(rawhtml.url)
            # print("状态码" + str(rawhtml.status_code))
            # print("页面的读取结果为")
            html = rawhtml.text
            return html
        except Exception as e:
            print(e)
            return


    def getRollUrlList(self,date):  #这个打开会是手机端的东西    #又重写了一遍了这个东西
        rollLatest = "http://news.163.com/latest/"
        requestURL ="http://news.163.com/special/0001220O/news_json.js?0.3699326344116929"

        my_headers = [                       #这边为了得到直接的手机端的页面代码返回，直接使用手机ua
            'Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 MicroMessenger/6.5.13.1100 NetType/WIFI Language/zh_CN',
            'Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 Mobile Safari/537.36 Maxthon/3047',
            # 'Mozilla/5.0 (iPhone 84; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14G60 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1',
            'Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; STF-AL00 Build/HUAWEISTF-AL00) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.9 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; SM-C7000 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.6.2.948 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 7.0; STF-AL10 Build/HUAWEISTF-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043508 Safari/537.36 V1_AND_SQ_7.2.0_730_YYB_D QQ/7.2.0.3270 NetType/4G WebP/0.3.0 Pixel/1080']

        headers = {"User-Agent": random.choice(my_headers), 'Referer': "http://news.163.com/latest/"}  # 默认值

        try:
            rawhtml = requests.get(requestURL, headers=headers, allow_redirects=False,
                                   timeout=30)  # 一般提取文本的话，那就用text，如果是文件就content
            rawhtml.encoding = "GBK"  ##gbk>gb2312   使用这种方式尚且还有乱码的情况，部分乱码，那就是gbk可以修复
            # print(chardet.detect(rawhtml.content)['encoding'])
            if rawhtml.status_code == 504:
                print(504)
                return
            # print(rawhtml.url)
            print("状态码" + str(rawhtml.status_code))
            # print("页面的读取结果为")
            html = rawhtml.text

            result10=[]
            if html.find('"news":')!=-1:
                rawjsonString = html.split('"news":')[1].replace("};","")
                jsDic = eval("("+rawjsonString+")")
                for i in jsDic:
                    if len(i)!=0:
                        for content in i:
                            if content['p'].split(" ")[0]==date:   #这个是今天的
                                url = content['l']
                                if url.find("photoview")==-1:            #不是图片的写入这儿
                                    result10.append(content['l'])
                                else:
                                    pass

                # print("插入了"+str(len(result10)))
                self.saveListToMysql(result10, date)  #

                return result10          #这个是返回前一天的所有的url链接放在这儿，大概200条以内，又变少了啊
        except Exception as e:
            print(e)
            return   #返回为空



    # def getJINGXUAN(self, date):  #先遍历api提取出url 最新的和日期
    #     result = self.wangyiMS("http://c.3g.163.com/nc/article/list/T1467284926140/0-60.html")  #这样每天才有53条数据，远远不够呀
    #     # print(result)
    #     result = result['T1467284926140']
    #     allUrls =[]
    #     for one in result:
    #         # print(one)
    #         if 'url_3w' in one.keys() and 'ptime' in one.keys():
    #             url = one['url_3w']
    #             time = one['ptime'].split(" ")[0]
    #             # print(one['url_3w'] +" "+one['ptime'].split(" ")[0])
    #             allUrls.append([url,time])
    #             # if(time!=date): #不等于最新的当天那个时间的话
    #             #     break
    #             # else:
    #             #     allUrls.append(url)
    #
    #     resultUrl = []
    #     for URL in allUrls:  #这儿一般又多少条呢
    #         # print(URL[0])
    #         # print(URL[1])
    #         if URL[0]!="" and URL[1]==date:
    #             # print("fuck")
    #             resultUrl.append(URL[0])
    #     return resultUrl


    def saveListToMysql(self,list,date):             #url list写入数据库中去
        connect = DB()
        for i in list:
            connect.insertTenxun(i,date,"wangyi")
        # print("所有插入完毕")
        # connect.__close__()

    def wangyiMS(self,apiUrl):
        my_headers = [
            'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30',
            'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)',
            'Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)']
        headers = {"User-Agent": random.choice(my_headers),
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                   'Accept-Encoding': 'gbk, utf-8',
                   'Accept-Language': 'zh-CN,zh;q=0.9',

                   }
        html = requests.get(apiUrl, headers=headers, allow_redirects=True)  # 不允
        print(html.status_code)
        if (html.status_code==404):

            pass
        else:
            print("正在打印东西")
            return html.json()  #因为是json载如，所以这样处理






if __name__ == "__main__":






    #----------------------下面是新滚动新闻提取的页面------------------------------------
    url="http://news.163.com/special/0001220O/news_json.js?0.17019531732162552"
    dateurl = DateUrl()

    number10 = dateurl.getRollUrlList("2019-04-05")
    print(len(number10))



