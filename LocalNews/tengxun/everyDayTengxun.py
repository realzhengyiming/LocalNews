import time



#每日更新之腾讯，这里可以改成多线程的形式来进行操作
from datetime import date, timedelta

'''
1.单线程的话就是


'''
from DBcontrol import DB

from mixP import MixNews                     #生成混合，就这三个操作的了
from tengxun.pageContent import pageContent  # 解析页面

from tengxun.pageUrls import DateUrl        #赫尔是提取当天的url 返回回来，然后逐个打开这样子


class EveryTengxun:
    def getEveryTengxun(self):  #这个其实就是封装在对象里面的一个主函数而已
        #开始之前，先检查有没有序列化的文件在这儿
        dbhelper= DB()
# todo 提取页面失败得这几个可以研究一下  是tuple   网址不同，（网址不同，发布时间的不同，）
        # {'type': 2, 'value': 'http:\\/\\/inews.gtimg.com\\/newsapp_match\\/0\\/5261922136\\/0'}
        # 纪念品牌20周年 smart Forease官图发布
        # 打开页面提取失败,可能是页面为404腾讯，删除这条url
        # 删除成功哈 http:////auto.qq.com//a//20181005//001598.htm
        # http:////news.qq.com//a//20181005//002590.htm
        # qqnews
        # 2
        pcontent = pageContent()
        # print("共提取到新闻url的数量有")
        # now_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 获取当前日期,每次执行操作的时候都这样
        now_date = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")  # 昨天日期
        # time.localtime(time.time())  #暂时是这样，以后的话
        print("昨天的日期是"+now_date+"现在正在爬取昨天的新闻!d😀")
        #1.获取一天的新url

        #爬取昨晚的
        dateUrl = DateUrl()  # 2018-09-27 日编辑  todo 这儿区分开来，不用通过这儿返回的，另外那儿只需要把那些urlState="False"的提取出来就可以
        dateUrl.pageUrlMain(now_date)   #获得今天的，并且写入数据库  todo 待会要把这儿的这个调回去

        todayNewUrl = dbhelper.__query__("select url from tengxun where urlState='False' and fromWhere='tengxun'")  #只要数据库中取出需要读取的url
        # print(type(todayNewUrl))
        print(len(todayNewUrl))
        print("")
        # 这儿才是把东西提取出来
        count = 1                                                             #计数，每100个就休息1分钟
        for dic in todayNewUrl:              #这儿还是需要把
            url = dic['url'] #2.把写入数据库的这几个新闻url的内容提取出来
            if count%200==0:   #突然的中断应该是因为这边连接不上那儿，所以应该问题不大
                time.sleep(60*2)    #每两百个休息4分钟好了
            count+=1

            #这儿的url是未转换成xw。电脑原版页面的url，所以，存的是这种url
            #还是得把这个url打开，才知道是否是title已经存在的


            title, Hcontent, Tcontent, Acontent=pcontent.getPageContentMain(url)  #这儿漏了更新到url中去  ,自动转换成xw的然后再下载
            time.sleep(1)
            # print(title, Hcontent, Tcontent, Acontent)
            if (title !="腾讯没找到标题" and title!=None and Hcontent!="" ):  #有内容的时候就更新这条数据
                # print("要更新的url是 "+url)
                resultState= dbhelper.updateContent(url,title,Hcontent,Tcontent,Acontent)  #要删除的是更新失败的那个
                if resultState==False:  #更新成功
                    print("更新失败，正在删除这个url不同，但是标题相同的新闻")
                    print(url)
                    dbhelper.deleteUrl(url)  # 按url把这条记录删除掉咯,生成失败也不需要删除这个拉，
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
                print("打开页面提取失败,可能是页面为404腾讯，删除这条url")   #为空的话，那么就删除这条把
                dbhelper.deleteUrl(url)  #按url把这条记录删除掉咯
                #要清洗以前的东西，可以不用请求那么多的，还是得请求一次才可以，，


if __name__=="__main__":
    everydayTengxun = EveryTengxun()
    everydayTengxun.getEveryTengxun()


        
