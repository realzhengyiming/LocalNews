#多进程的东西放在这儿了

import multiprocessing
import os
import time

import schedule
from fenghuang.everyDayFenghuang import EveryFenghuang

from wangyi.everyDayWangyi import EveryWangyi

from tengxun.everyDayTengxun import EveryTengxun






def worker_1(interval):   #里面的函数改成外面那个就可以了
    print("网易的子进程开始工作")
    everyDayTengxun = EveryWangyi()  # 先这样设置好来就可以了
    one = everyDayTengxun.getEveryDayWangyi()  #这样就行了对吧  #这儿就在执行这个函数了
    print ("网易的完成了今天的爬取")


def worker_2(interval):
    print ("腾讯的子进程开始工作")
    everyDayTengxun = EveryTengxun()  # 先这样设置好来就可以了
    one = everyDayTengxun.getEveryTengxun()  #这样就行了对吧  #这儿就在执行这个函数了
    print ("网易的完成了今天的爬取")

def worker_3(interval):   #多进程的好处就是这样，如果哪部分有问题解决了问题后再重置一下就号了
    print ("凤凰的子进程开始工作")
    everyDayTengxun = EveryFenghuang()  # 先这样设置好来就可以了
    one = everyDayTengxun.getEveryFenghuang()  #这样就行了对吧  #这儿就在执行这个函数了
    print ("网易的完成了今天的爬取")

if __name__ == "__main__":   #主进程每天定时创建子进程来进行新闻的爬取
    #主函数这儿做一个定时，

    print('这里是进程: %sd   父进程ID：%s' % (os.getpid(), os.getppid()))
    p1 = multiprocessing.Process(target = worker_1, args = (6,))
    p2 = multiprocessing.Process(target = worker_2, args = (3,))
    p3 = multiprocessing.Process(target = worker_3, args = (4,))

    p1.daemon = True
    p2.daemon = True
    p3.daemon = True
    #
    p1.start()
    p2.start()
    p3.start()
    print("The number of CPU is:" + str(multiprocessing.cpu_count()))
    for p in multiprocessing.active_children():
        print("child   p.name:" + p.name + "\tp.id" + str(p.pid))

    p1.join()
    p2.join()
    p3.join()  #直接不等待吧

    # print("The number of CPU is:" + str(multiprocessing.cpu_count()))  #结束了后就无法读取进程号了，使用了join的话
    # for p in multiprocessing.active_children():
    #     print("child   p.name:" + p.name + "\tp.id" + str(p.pid))
    print ("today work done ND!!!!!!!!!!!!!!!!!")   #这是是主线程，如何让主线程等待子线程结束后才输出呢