import time
from datetime import date, timedelta

from DBcontrol import DB

from fenghuang.fenghuangPageContent import fenghuangPageContent
from fenghuang.fenghuangPageUrls import fenghuangDateUrls
from mixP import MixNews

# todo 剩下的就是跑一下到底行不行这个东西,试一下跑大批量的东西


class EveryFenghuang:
    def getEveryFenghuang(self):
        dbhelper = DB()
        dateurl = fenghuangDateUrls()
        oneContent = fenghuangPageContent()
        print("共提取到新闻url的数量有")
        now_date = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")  # 昨天日期
        print(now_date)

        # print(dateurl.getOneDayNewUrl("2018-07-03"))
        #1.页面新闻url写入数据库
        todayNewUrl = dateurl.getUrlLists(now_date)   #1.这个就是当天的
        urlNumer = len(todayNewUrl)

        todayNewUrl = dbhelper.__query__("select url from tengxun where urlState='False' and fromWhere='fenghuang'")  #只要数据库中未填补内容的url
        print(type(todayNewUrl))
        print(len(todayNewUrl))
        # for dic in todayNewUrl:
        #     dic['url']

        print("")

        # 这儿才是把东西提取出来
        count = 1                                                             #计数，每100个就休息1分钟
        print(todayNewUrl)
        flagNumber = 1
        mixNumber = 0
        for dic in todayNewUrl:
            newUrl = dic['url'] #2.把写入数据库的这几个新闻url的内容提取出来
            if newUrl.find("pl.ifeng.com")!=-1:
                title, Hcontent, Tcontent, Acontent = oneContent.getPlContent(newUrl)
                if (title != "凤凰没有找到标题" and title != None and Hcontent != ""):  # 有内容的时候就更新这条数据
                    dbhelper.updateContent(newUrl, title, Hcontent, Tcontent, Acontent)

                    print("正在生成新混合新闻。。。")  # 3. 然后是把页面页写入数据库，再然后是随机生成相同数量的
                    mixNews = MixNews()
                    if mixNews.__startToMix__() != True:  # 调用一次就执行一次，可以修改返回的状态
                        print("生成失败，已经没有刚填满的未用过的文章了")
                        print(newUrl)
                        dbhelper.deleteUrl(newUrl)  # 如何这个内容为空也要删除，（可能前面一个步骤更新的时候发现相同的标题，所以插入不了），
                    else:
                        mixNumber+=1    #成功就生成一个累加
                else:
                    print("更新失败，标题提取失败，为空")
                    dbhelper.deleteUrl(newUrl)  # 按url把这条记录删除掉咯
            else:    #这个就是默认的那个新闻news.ifeng.com
                title, Hcontent, Tcontent, Acontent =oneContent.getNewsContent(newUrl)
                if (title != "凤凰没有找到标题" and title != None and Hcontent != ""):  # 有内容的时候就更新这条数据
                    dbhelper.updateContent(newUrl, title, Hcontent, Tcontent, Acontent)

                    print("正在生成新混合新闻。。。")  # 3. 然后是把页面页写入数据库，再然后是随机生成相同数量的
                    mixNews = MixNews()
                    if mixNews.__startToMix__() != True:  # 调用一次就执行一次，可以修改返回的状态
                        print("生成失败，已经没有刚填满的未用过的文章了")
                        print(newUrl)
                        dbhelper.deleteUrl(newUrl)  # 如何这个内容为空也要删除，（可能前面一个步骤更新的时候发现相同的标题，所以插入不了），
                    else:
                        mixNumber+=1    #成功就生成一个累加
                else:
                    print("更新失败，标题提取失败，为空")
                    dbhelper.deleteUrl(newUrl)  # 按url把这条记录删除掉咯
        print("目前生成了 共有那么多个混合的新闻  "+str(mixNumber))   #普遍存在

        #可以改成改完一个就生成一个嘛
        # print(urlNumer)
        # print("正在生成新混合新闻。。。")  #3. 然后是把页面页写入数据库，再然后是随机生成相同数量的
        # for i in range(0,urlNumer):
        #     mixNews = MixNews()
        #     mixNews.__startToMix__()  #调用一次就执行一次，可以修改返回的状态


if __name__ == "__main__":  #这个就是url的东西#   这部分是插入操作的东西，提交后
    chak = EveryFenghuang()
    chak.getEveryFenghuang()
    print("finish!")