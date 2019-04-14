import time
from datetime import date, timedelta

from DBcontrol import DB

from mixP import MixNews
from wangyi.wangyiPageContent import wangyiPageContent
from wangyi.wangyiUrls import DateUrl


class EveryWangyi:

    def getEveryDayWangyi(self):
        dbhelper = DB()
        dateurl = DateUrl()
        oneContent = wangyiPageContent()
        print("共提取到新闻url的数量有")
        now_date = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")  # 昨天日期
        print(now_date)
        # print(dateurl.getOneDayNewUrl("2018-07-03"))
        #1.页面新闻url写入数据库

        dateurl.getRollUrlList(now_date)  # 1.这个就是当天的，和凤凰一样，老样子啊，获得了链接后直接可以写入数据库中去了

        todayNewUrl = dbhelper.__query__("select url from tengxun where urlState='False' and fromWhere='wangyi';")  # 只要数据库中取出需要读取的url
        # print(type(todayNewUrl))
        print(len(todayNewUrl))   #这个才是打开来的东西

        urlNumer = len(todayNewUrl)
        print("正在打开网易的新闻的东西")  
        print(todayNewUrl)

        # print("正在打开网易的新闻的东西")
        # print(todayNewUrl)

        # for newUrl in todayNewUrl:  # 2.然后把内容段落写入数据库
        #     title, Hcontent, Tcontent, Acontent = oneContent.getPageContent(newUrl)
        #     if (title != "网易没找到标题" and title != None and Hcontent != ""):  # 有内容的时候就更新这条数据
        #         dbhelper.updateContent(newUrl, title, Hcontent, Tcontent, Acontent)
        #
        #         print("正在生成新混合新闻。。。")  # 3. 然后是把页面页写入数据库，再然后是随机生成相同数量的
        #         mixNews = MixNews()
        #         mixNews.__startToMix__()  # 调用一次就执行一次，可以修改返回的状态
        #
        #     else:
        #         print("更新失败，标题提取失败，为空")
        count = 1                                                             #计数，每100个就休息1分钟
        for dic in todayNewUrl:
            url = dic['url'] #2.把写入数据库的这几个新闻url的内容提取出来
            if count%200==0:   #突然的中断应该是因为这边连接不上那儿，所以应该问题不大，每两百条休息一分钟
                time.sleep(60)
            count+=1

            #这儿的url是未转换成xw。电脑原版页面的url，所以，存的是这种url
            title, Hcontent, Tcontent, Acontent=oneContent.getNewsContent(url)  #这儿漏了更新到url中去  ,自动转换成xw的然后再下载
            time.sleep(1)
            # print(title, Hcontent, Tcontent, Acontent)
            if (title !="腾讯没找到标题" and title!=None and Hcontent!="" ):  #有内容的时候就更新这条数据
                # print("要更新的url是 "+url)
                resultState= dbhelper.updateContent(url,title,Hcontent,Tcontent,Acontent)  #要删除的是更新失败的那个
                if resultState==False:  #更新成功
                    print("更新失败，正在删除这个重复的url")
                    print(url)
                    # dbhelper.deleteUrl(url)  # 按url把这条记录删除掉咯,生成失败也不需要删除这个拉，
                    print()
                else:
                    # print("正在生成新混合新闻。。。")  # 3. 然后是把页面页写入数据库，再然后是随机生成相同数量的
                    mixNews = MixNews()
                    if mixNews.__startToMix__()!=True:  # 调用一次就执行一次，可以修改返回的状态
                        print("生成失败，已经没有刚填满的未用过的文章了")
                        print(url)
                        dbhelper.deleteUrl(url)  # 如何这个内容为空也要删除，（可能前面一个步骤更新的时候发现相同的标题，所以插入不了），
                        # print()
                    else:
                        print(True)
            else:
                print("打开页面提取失败,可能是页面为404网易，正在删除这条url "+url)   #为空的话，那么就删除这条把
                dbhelper.deleteUrl(url)  #按url把这条记录删除掉咯 todo don't delete it first
                #要清洗以前的东西，可以不用请求那么多的，还是得请求一次才可以，，  todo the error is can't get the website title .

        # print(urlNumer)
        # print("正在生成新混合新闻。。。")  # 3. 然后是把页面页写入数据库，再然后是随机生成相同数量的
        # for i in range(0, urlNumer):
        #     mixNews = MixNews()
        #     mixNews.__startToMix__()  # 调用一次就执行一次，可以修改返回的状态
        # except Exception as e:
        #     print("爬取网易的出现了问题 ")
        #     print(e)





if __name__ == "__main__":  #这个就是url的东西#   这部分是插入操作的东西，提交后
    chak = EveryWangyi()        #get yesterday total news here at 1 :00 .
    chak.getEveryDayWangyi()
    print("finish!")