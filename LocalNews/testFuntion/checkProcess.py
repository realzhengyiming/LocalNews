#coding=utf-8
import os
import time
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
        return lines[-20:]

#a;lskdjf a;f dsf;ds f;f f

if __name__=="__main__":
    dbhelper = DB()
    tempNumber =  len(dbhelper.__query__("select * from c_title"))  # 先检测一下多少，变了多少
    email = EMail()
    while(1):
        if isRunning("python everydaynews.py"):
            print("程序还在运行中。。。12小时后继续检查")
            nonNumber = len(dbhelper.__query__("select * from c_title"))  # 先检测一下多少，变了多少
            print(str(nonNumber-tempNumber))
            face ="🤔我该以什么表情来表示呢,如果不是崩了，那就待机中，6小时后我再来看看"
            if(nonNumber-tempNumber)>800:
                face="\n🤣今天的量还不错😘"
            elif ((nonNumber-tempNumber))>600 and ((nonNumber-tempNumber))<=800:
                face ="🤗今天的量还算正常哈"
            else:
                pass
            text = "🤔目前的数量有🎆 "+str(nonNumber)+" ✨"+face+"  ，比6 小时前增加 "+str(nonNumber-tempNumber)  +"\n 这儿是你要的"
            # text = "😍成功了拉，以后自动检测后就可以定时的向手机汇报程序中断了的消息拉"


            email.SendEmail(1, text)
            time.sleep(60*60*6)  #每两小时检查一下是否还在运行，如果没在运行的话那就跳过
            tempNumber = nonNumber  # 先检测一下多少，变了多少
        else:  #发送邮件通知我程序已经出问题了 utf-8bianma
            alltext = ""
            for text in readfile('/root/newsSpider/nohup.out'):
                alltext = alltext + text + "\n"
            print(alltext)

            text = "你的爬虫已经中断，不知道为什么😀请回新闻爬虫服务器检查你的爬虫output错误原因,当前的总数量为--》\n"+alltext
            email = EMail()
            nonNumber = len(dbhelper.__query__("select * from c_title"))  # 先检测一下多少，变了多少

            email.SendEmail(1,text+str(nonNumber))
            time.sleep(60 * 60 * 6)  # 每两小时检查一下是否还在运行，如果没在运行的话那就跳过
            pass

