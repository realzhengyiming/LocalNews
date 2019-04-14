#这个这个是启动各个，主要是用来填充完里面有的内容的，让他们慢慢的爬就好了，爬完了就不管，跳出都没问题
import time

from DBcontrol import DB
from fenghuang.fenghuangPageContent import fenghuangPageContent
from mixP import MixNews
from tengxun.pageContent import pageContent
from wangyi.wangyiPageContent import wangyiPageContent
import threading
#现在这个情况时填充多少篇那就生成多少篇东西出来



#先获取腾讯的所有出来，然后获取凤凰的出来，然后再获取网易的出来，然后获取到一定程度的时候才开始mixP，生成的东西扔到
#那个数据库就可以了
class myThread(threading.Thread):
    def __init__(self, method, method_arge,fromWhere):
        threading.Thread.__init__(self)
        self.method = method
        self.method_arge = method_arge
        self.fromWhere = fromWhere

    def run(self):
        print("开启一个线程来运行一个填充"+self.fromWhere)
        self.method(self.method_arge)

class doMixP(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)


    def run(self):
        print("startTOmix")
        while(1): #每次都是这样
            for number in range(1,5):
                mixNews = MixNews()
                mixNews.__startToMix__()  #里面已经有那种写入数据库的操作了
            time.sleep(30)

#                      发现问题，遇到开头只能提取到标题，然后内容为空的这种，其实后面还有有内容的，存起来，然后再次打开
def tengxunFill(tengxunUrls):
    datehelper = DB()
    flag = 1
    for url in tengxunUrls:
        print(url[0])
        print(url)
        flag += 1
        if flag%50==0: #每30个休息一下子这个样子，
            print("正在进入休眠")
            time.sleep(60*2)
            # datehelper.refreshConnection()
        title, Hcontent, Tcontent, Acontent = fillTengxun.getPageContent(url[0])  #我要做的是把内容填上去，然后再更新
        if(title!="" and Hcontent!=""):
            print(url[0])
            print(url)
            datehelper.updateContent(url[0], title, Hcontent, Tcontent, Acontent)
            mixNews = MixNews()
            state = mixNews.__startToMix__()  #返回是否生成成功，
            if(state):  # 里面已经有那种写入数据库的操作了
                print("混合生成生成成功！")
                datehelper.updateState(url[0])
            # else:  #生成失败就删除掉



def wangyiFill(wangyiUrls):
    datehelper = DB()
    flag =1
    for url in wangyiUrls:
        flag += 1
        if flag%50==0: #每30个休息一下子这个样子，
            time.sleep(60*3)
            datehelper.refreshConnection()
        title, Hcontent, Tcontent, Acontent = fillWangyi.getPageContent(url[0])  #但是如果是title=''这种就会遇到那种可能是格式不支持的那种
        if(title!="" and Hcontent!=""):
            datehelper.updateContent(url[0], title, Hcontent, Tcontent, Acontent)  #这个打开更新东西进去是需要title不等于空的才可以
            mixNews = MixNews()
            state = mixNews.__startToMix__()
            if(state):  # 里面已经有那种写入数据库的操作了
                datehelper.updateState(url[0])

def fenghuangFill(tengxunUrls):
    datehelper = DB()
    flag = 1
    for url in tengxunUrls:
        flag+=1
        if flag%50==0: #每30个休息一下子这个样子，打开多少个页面后休息一下
            time.sleep(60*3)  #每次休眠后都重来一个新的数据库连接
            datehelper.refreshConnection()


        title, Hcontent, Tcontent, Acontent = fillFenghaung.getPageContent(url[0])
        if(title!="" and Hcontent!=""):
            datehelper.updateContent(url[0], title, Hcontent, Tcontent, Acontent)
            mixNews = MixNews()
            state = mixNews.__startToMix__()
            if(state):  # 里面已经有那种写入数据库的操作了
                datehelper.updateState(url[0])


        



if __name__ == "__main__":  #这个就是url的东西
    fillTengxun = pageContent()
    fillFenghaung = fenghuangPageContent()
    fillWangyi = wangyiPageContent()

    datehelper = DB()
  
    # tengxunUrls = datehelper.__query__('select url from tengxun where fromWhere ="tengxun" and url!="" and isNull(title) and urlState="False";')
    # fenghuangUrls = datehelper.__query__('select url from tengxun where fromWhere ="fenghuang" and url!="" and isNull(title) and urlState="False" ;')
    wangyiUrls = datehelper.__query__('select url from tengxun where fromWhere ="wangyi" and url!="" and isNull(title) and urlState="False" ;')

    # print(len(tengxunUrls))
    # print(len((fenghuangUrls)))
    print(len((wangyiUrls)))



    # tengxun = myThread(tengxunFill,tengxunUrls,"tengxun")
    # tengxun.run()
    #
    wangyi = myThread(wangyiFill,wangyiUrls,"wangyi")
    wangyi.run()

    # fenghuang = myThread(fenghuangFill,fenghuangUrls,"fenghuang")
    # fenghuang.run()

