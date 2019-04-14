#coding=utf-8
# from selenium import webdriver
# url = "http://www.eshow365.com/zhanhui/html/120062_0.html"
# driver = webdriver.PhantomJS(executable_path='/usr/bin/phantomjs') #这个路径就是你添加到PATH的路径
# driver.get(url)
# print (driver.page_source)
import json
import random
import chardet

import  requests
from tengxun.pageContent import pageContent

from tengxun.pageUrls import DateUrl
#主题编码
news_Theme = 1537874915062
ent_Theme = 1537876288634
sport_Theme = 1537877689177
finance_Theme = 1537878365483
tech_Theme = 1537879684280
auto_Theme = 1537887032223
house_Theme = 1537887128904
#主题标识

def returnThemeCode(theme):
    news_Theme = 1537874915062
    ent_Theme = 1537876288634
    sport_Theme = 1537877689177
    finance_Theme = 1537878365483
    tech_Theme = 1537879684280
    auto_Theme = 1537887032223
    house_Theme = 1537887128904

    if theme=='news':
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



def getThemeUrl(theme,today,pageNumber):  #获得主题的url
    rawUrl = "http://roll.news.qq.com/interface/cpcroll.php"
    rawReferer = '.qq.com/articleList/rolls/'  #'http://news   前面还有这个东西

    my_headers = [
        'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30',
        'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)',
        'Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)']

    headers = {"User-Agent": random.choice(my_headers), 'Referer': 'http://'+theme+rawReferer}  # 默认值

    # dataDic={
    #     'callback': 'rollback',
    #     'site':theme,
    #     'mode':1,
    #     'date':today,
    #     'page':pageNumber,
    #     '_':returnThemeCode(theme),
    #     # 'cata=':''
    #
    # }

    rawUrl = rawUrl+"?callback=rollback&mode=1&cata=&_="+str(returnThemeCode(theme))+"&site="+theme+"&page="+str(pageNumber)+"&date="+today
    try:
        rawhtml = requests.get(rawUrl, headers=headers, allow_redirects=False,timeout=30)  # 一般提取文本的话，那就用text，如果是文件就content
        rawhtml.encoding = chardet.detect(rawhtml.content)['encoding']

        print(rawhtml.url)
        print("状态码"+str(rawhtml.status_code))

        if rawhtml.status_code==504:
            print(504)
            return
        print("页面的读取结果为")
        print(rawhtml.text)
        if rawhtml.text.find('rollback')==0:
            jsonString = rawhtml.text.split("rollback")[1]  # 把js提取出来就可以了
        else:
            jsonString  = rawhtml.text
        print(jsonString)
        dicData = eval(jsonString)
        print(type(jsonString))
        print(jsonString)
        # print(dicData['data']['article_info'])
        print(len(dicData['data']['article_info']))
        if dicData['data']=="":
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
        return [] #没有东西诶



if __name__=="__main__":


         #todo 这些都还可能是 page2的情况
    # url    ="http://roll.news.qq.com/interface/cpcroll.php?callback=rollback&site=news&mode=1&cata=&date=2018-09-25&page=1&_=1537850539512"
    # 这个是时政新闻
    urlNew ="http://roll.news.qq.com/interface/cpcroll.php?callback=rollback&site=news&mode=1&cata=&date=2018-09-25&page=1&_=1537874915062"
    #这儿是国际标题， referer = http://news.qq.com/articleList/rolls/
    urlEnt ="http://roll.news.qq.com/interface/cpcroll.php?callback=rollback&site=ent&mode=1&cata=&date=2018-09-25&page=1&_=1537876288634" #referer = http://ent.qq.com/articleList/rolls/
                   #referer = http://ent.qq.com/articleList/rolls/
    urlSport="http://roll.news.qq.com/interface/cpcroll.php?callback=rollback&site=sports&mode=1&cata=&date=2018-09-25&page=1&_=1537877689177"  #r这个好像而是动态加载出来的，真是的
                   # todo 这个要重新解析，可能是动态的 referer = http://sports.qq.com/articleList/rolls/    有些page可能不止一个的，都有   体育的是动态的，待会回来再分析，有好多页，很厉害的样子呢
    #不同的theme要切换不同的referer
    urlFinance="http://roll.news.qq.com/interface/cpcroll.php?callback=rollback&site=finance&mode=1&cata=&date=2018-09-25&page=1&_=1537878365483"
                # referer http://finance.qq.com/articleList/rolls/
         # todo 默认的解析可以，但是好慢，使用代理的情况下 http://173.255.210.215:8000/?count=6&country=%E5%9B%BD%E5%86%85
    urlTech ="http://roll.news.qq.com/interface/cpcroll.php?callback=rollback&site=tech&mode=1&cata=&date=2018-09-25&page=2&_=1537879684280"
                # referer = http://tech.qq.com/articleList/rolls/
         # todo 这个也是偶尔有点慢的样子， 使用代理 下


    urlAuto   ="http://roll.news.qq.com/interface/cpcroll.php?callback=rollback&site=auto&mode=1&cata=&date=2018-09-25&page=1&_=1537887032223"
           #referer 这个是汽车的  http://auto.qq.com/articleList/rolls/dai'li
         #todo 这个汽车的应该使用另外的解析来解析才可以

    urlHouse="http://roll.news.qq.com/interface/cpcroll.php?callback=rollback&site=house&mode=1&cata=&date=2018-09-25&page=1&_=1537887128904"
            # referer http://house.qq.com/articleList/rolls/   这个是房产的 可以解析
    # getThemeUrl(urlSport,"http://sports.qq.com/articleList/rolls/")
    urlRaw = "http://roll.news.qq.com/interface/cpcroll.php?" #带参数进行post请求才对把
    # print(jsonDic)

# print(rawhtml.json())


    tengxun = pageContent()  #其余的当成第一部分去处理就可以了
    oneUrl=[]   #单单一个运动的就够了
    themeList = ['news', 'ent', 'tech', 'auto', 'house', 'finance', 'sports']

    for theme in themeList:
        print("第一个主题是")
        for i in range(1,11):
            print("第"+str(i)+"页")
            responseList = getThemeUrl(theme, "2018-09-26", i)  #这儿只是测试最大页数有多少而已
            if len(responseList)==0:
                print("最大页数为"+str(i-1)+"页")
                break
            else:
                oneUrl = oneUrl+responseList
            print(oneUrl)
    print(len(oneUrl))    #目前可以返回653    昨天的 完整的1140，数量是很可观的

