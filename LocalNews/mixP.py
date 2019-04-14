#coding=utf-8
#这个是提取出数据库的东西，然后
from DBcontrol import DB

'''
#这儿的逻辑是，首先是插入数据库url 和时间写入回去
然后打开url 把title，Hcontent，Tcontent，Acontent,写入回去
然后

'''

class MixNews:
    def __startToMix__(self):  #每次执行生成一篇
        datahelper = DB()
        allHtml = datahelper.__randomP__()

        title,header,tail,id = datahelper.__randomHandT__()  #没有找到id就变成0了

        # print(title,header,tail)
        #title = "<h1>"+title+"</h1>"
        # print(header)
        # print("合成的html文件在这儿")
        mixP  = title+header+allHtml+tail
        # print("本文总长"+str(len(new_news)))
        # print(title+header+allHtml+tail)

        # f= open(r"D:\pyfile\ProxySpider\newMission\new.html","w")
        # f.write(new_news)  ##多媒体文件要是用conctent哦！
        # f.close()/
        # print("生成的标题是  "+title  )
        # print("生成的内容是 "+mixP)

        if(title!="" and mixP !=""):
            datahelper.insertMixP(title,mixP)  #生成成功的话就是这样
            datahelper.updateMixState(id)  #这儿无法更新的  ,这儿自带更新了
            # print("生成成功")
            return True

        else:
            print("生成混合失败，没有找到title不为空的url")
            # datahelper.deleteUrl()
            return False
        # print(len(datahelper.__query__("select * from tengxun where title!='';")))


if __name__ == "__main__":  #这个就是url的东西
    dbhelper = DB()
    # ddd = MixNews()
    # ddd.__startToMix__()
    title, header, tail, id = dbhelper.__randomHandT__()

    print(title)