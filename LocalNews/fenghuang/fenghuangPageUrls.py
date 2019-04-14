
#主要从官网的这儿提取就可以了
#url = http://news.ifeng.com/listpage/11502/0/1/rtlist.shtml
'''
http://news.ifeng.com/listpage/11502/20170528/1/rtlist.shtml
后面那个是日期，然后有返回回来的页数
'''
import random
import time
from datetime import date, timedelta

import chardet
import requests

from DBcontrol import DB
from TimeHelper import TimeHelper
from makebeautifulSoup import makeBS


class fenghuangDateUrls:
#这个是按天来的，组合一下就行了,获取滚动列表的新闻url
    def __init__(self):
        # self.fenghuangUrlHome = "http://news.ifeng.com/listpage/11502/0/1/rtlist.shtml"
        # self.fenghuangPage =    "http://news.ifeng.com/listpage/11502/"+20180729+"/"+16+"/rtlist.shtml"
        self.raw = "http://news.ifeng.com/listpage/11502/"
        self.fenghuangUrl ="http://news.ifeng.com/listpage/11502/20170528/1/rtlist.shtml"  # todo 这儿有的问题是，页面的格式各不相同，解析失败

    def checkEnd(self,url,flag):
        soup = makeBS().makesoup(url)
        m_page = soup.find("div",attrs={"class","m_page"})
        # print(m_page)
        nextFlag = False
        if m_page!=None:
            for a in m_page.find_all("a"):  #一个找全部闹出来那么久的东西
                # print(type(a))
                # print(a.text)
                if a.text.find("下一页")==0:
                    nextFlag=True
                    break
                    # return True #有就返回这个
        return nextFlag  #有下一页就继续遍历





    def getUrlLists(self,date):  #这个就是输入日期的东西  网址是：http://news.ifeng.com/listpage/11502/20180928/1/rtlist.shtml
        '''
        凤凰资讯的 -》即时新闻
        :param date:
        :return:
        '''
        # date = "2018-07-29"
        urldate=date.replace("-","")
        pageNumber = 1
        flag = True
        allfenghuangUrls =[]
        while(flag):  #1,2,3,.....40
            tempUrl = self.raw +urldate+"/"+ str(pageNumber) + "/rtlist.shtml"

            print("url是:"+tempUrl)
            allfenghuangUrls = allfenghuangUrls+self.getOnePageUrl(tempUrl)  #提取一页中的所有url
            time.sleep(3)
            flag = self.checkEnd(tempUrl,flag)
            print(flag)
            pageNumber=pageNumber+1
            print("页面是第"+str(pageNumber))

            print()
            #检查一下是不是还有下一页
        # todo 记住，这儿先不写进去先，注释掉了这个保存到数据库的
        self.saveListToMysql(allfenghuangUrls,date,"fenghuang")     #这个就是把url写入数据库
        print(len(allfenghuangUrls))
        return allfenghuangUrls
        # print("以把今天页面url写入数据库")

    def getOnePageUrl(self,url):  #找到有下一页按钮那就直接数字加起来就可以了，先点第一页的下一页
        soup  = makeBS().makesoup(url)  #统一使用了一样的
        dictt  =[]
        # button = soup.find("div",attrs={"class":"m_page"})
        if soup==None:
            return dictt
        li = soup.find_all("li")

        print(url)
        for i in li:
            if (i.h4!=None):
                title = i.a.text
                url = i.a['href']
                dictt.append(url)
                print(title,url)   #这儿只写入url和fromWhere就可以了
        print("找完一页的url")

        return dictt   #返回找到的url的列表在这里面给v你你

    def saveListToMysql(self, lists, date,fromWhere):
        connect = DB()
        lists = list(set(lists))
        for i in lists:
            connect.insertTenxun(i, date,fromWhere)
            print("所有插入完毕")
        # connect.__close__()

    #------------------------------------最新的，打算爬取的是网易滚动这儿------------------------------------------------



if __name__ == "__main__":
    newone = fenghuangDateUrls()
    datehelp = TimeHelper()
    now_date = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")  # 昨天日期

    # now_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 获取当前日期,每次执行操作的时候都这样
    # dateList = datehelp.getTimeList(now_date,now_date)      # 2018-09-这儿是决定
    # for i in dateList:
    newone.getUrlLists(now_date)   #开始执行把url写入进去  todo 这儿要保存一下，上次没有保存好这个东西  5

    # print(len(newone.getUrlLists("2018-09-30")))   #这儿也才167条，远远不够啊,这样也才勉强接近而已,200条

