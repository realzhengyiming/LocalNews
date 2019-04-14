#coding=utf-8
import os
import time
from datetime import date, timedelta
from multiprocessing import Process #这种方式是都可以使用的

from tools.QQemailSent import EMail

from DBcontrol import DB



'''
@author: Jacobpc
'''

import os
import sys
import subprocess


def get_process_id(name):
    child = subprocess.Popen(["ps aux | grep" +name+'| grep -v grep'], stdout=subprocess.PIPE, shell=False)
    print(child)
    print(type(child))
    response = child.communicate()[0]
    return response


def isRunning(process_name):
    try:
        process = len(os.popen('ps aux | grep "' + process_name + '" | grep -v grep').readlines())
        if process >= 1:
            return True
        else:
            return False
    except:
        print("Check process ERROR!!!")
        return False

def readfile(tfile):
    with open(tfile, 'r') as f:
        lines = f.readlines()
        return lines[-50:]

#a;lskdjf a;f dsf;ds f;f f
# todo 所有的错误提示中加上那个可以确定错误位置的东西
if __name__=="__main__":
    dbhelper = DB()
    tempNumber =  len(dbhelper.__query__("select * from c_title"))  # 先检测一下多少，变了多少
    email = EMail()
    timeSleep=60*60*6   #这个是发右键的休眠的时间
    while(1):
        now_date = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")  # 具体昨天日期的三个东西的结果
        tengxunNumber = len(dbhelper.__query__(
            "select * from tengxun where newdate='%s' and fromwhere='%s'" % (now_date, "tengxun")))  # 先检测一下多少，变了多少
        wangyiNumber = len(
            dbhelper.__query__("select * from tengxun where newdate='%s' and fromwhere='%s'" % (now_date, "wangyi")))
        fenghuangNumber = len(
            dbhelper.__query__("select * from tengxun where newdate='%s' and fromwhere='%s'" % (now_date, "fenghuang")))

        tengxunTrue = len(dbhelper.__query__(
            "select * from tengxun where newdate='%s' and fromwhere='%s' and urlState='True'" % (now_date, "tengxun")))  # 先检测一下多少，变了多少
        wangyiTrue = len(
            dbhelper.__query__("select * from tengxun where newdate='%s' and fromwhere='%s' and urlState='True'" % (now_date, "wangyi")))
        fenghuangTrue = len(
            dbhelper.__query__("select * from tengxun where newdate='%s' and fromwhere='%s' and urlState='True' " % (now_date, "fenghuang")))


        if isRunning("python everydaynews.py"):
            print("程序还在运行中。。。12小时后继续检查")
            nonNumber = len(dbhelper.__query__("select * from c_title"))  # 先检测一下多少，变了多少
            print(str(nonNumber-tempNumber))

            alltext = ""
            face ="🤔我该以什么表情来表示呢,如果不是崩了，那就待机中，6小时后我再来看看"
            if(nonNumber-tempNumber)>800:
                face="\n🤣今天的量还不错😘"
            elif ((nonNumber-tempNumber))>600 and ((nonNumber-tempNumber))<=800:
                face ="🤗今天的量还算正常哈"
            elif (nonNumber -tempNumber)==0:
                for text in readfile('/root/newsSpider/normal.out'):
                    alltext = alltext + text + "\n"
                print("000000")
            else:
                pass
            text = "今天为止总共爬取到的数量有:"+str(tengxunTrue+fenghuangTrue+wangyiTrue)+"\n🤔目前的数量有🎆 "+str(nonNumber)+" ✨"+face+"  ，比6 小时前增加 "+\
                   str(nonNumber-tempNumber)  +"\n 这三个是提取到的连接的数量"+"\ntengxun->"+\
                   str(tengxunNumber)+"\nwangyi->"+\
                   str(wangyiNumber)+"\nfenghuang"+\
                   str(fenghuangNumber)+"\n这三个是提取完连接读取到的具体的数量"+"\ntengxun->"+\
                   str(tengxunTrue)+"\nwangyi->"+\
                   str(wangyiTrue)+"\nfenghuang->"+\
                   str(fenghuangTrue)+"\n"+alltext
            # text = "😍成功了拉，以后自动检测后就可以定时的向手机汇报程序中断了的消息拉"


            email.SendEmail(1, text)
            time.sleep(timeSleep)  #每两小时检查一下是否还在运行，如果没在运行的话那就跳过
            tempNumber = nonNumber  # 先检测一下多少，变了多少
        else:  #发送邮件通知我程序已经出问题了 utf-8bianma todo晚点再部署上去
            alltext = ""
            for text in readfile('/root/newsSpider/error.out'):
                alltext = alltext + text + "\n"
            # print(alltext)
# nohup python everydaynews.py 1 >normal.out 2>error &
            text = "今天为止总共爬取到的数量有:"+str(tengxunTrue+fenghuangTrue+wangyiTrue)+"\n你的爬虫已经中断，不知道为什么😀请回新闻爬虫服务器检查你的爬虫output错误原因,当前的总数量为--》"+"\n这三个是提取完连接读取到的具体的数量"+"\ntengxun->"+\
                   str(tengxunTrue)+"\nwangyi->"+\
                   str(wangyiTrue)+"\nfenghuang"+\
                   str(fenghuangTrue)+"\n"+alltext
            email = EMail()
            nonNumber = len(dbhelper.__query__("select * from c_title"))  # 先检测一下多少，变了多少

            email.SendEmail(1,"目前总数为"+str(nonNumber)+text)
            time.sleep(timeSleep)  # 每两小时检查一下是否还在运行，如果没在运行的话那就跳过
            pass

