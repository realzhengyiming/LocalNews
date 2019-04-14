import datetime
import multiprocessing
import os
import threading
import time

from DBcontrol import DB
from config import startTime

from fenghuang.everyDayFenghuang import EveryFenghuang
from tengxun.everyDayTengxun import EveryTengxun
from wangyi.everyDayWangyi import EveryWangyi
import schedule
import time

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


class AutoRunAtTime:              #这儿应该是三个线程的
    def job(self,name):   #这个是主线程把
        dbhelper = DB()                    #todo 每个线程的异常处理需要单独的进行，后续可能需要主线程来管理子线程的异常梳理才可以
        print("正在爬取今天的新闻内容")
        print('这里是进程: %sd   父进程ID：%s' % (os.getpid(), os.getppid()))
        p1 = multiprocessing.Process(target=worker_1, args=(6,))
        p2 = multiprocessing.Process(target=worker_2, args=(3,))  #腾讯
        p3 = multiprocessing.Process(target=worker_3, args=(4,))

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
        p3.join()  # 直接不等待吧

        # print("The number of CPU is:" + str(multiprocessing.cpu_count()))  #结束了后就无法读取进程号了，使用了join的话
        # for p in multiprocessing.active_children():
        #     print("child   p.name:" + p.name + "\tp.id" + str(p.pid))
        print("today work done ND!!!!!!!!!!!!!!!!!")  # 这是是主线程，如何让主线程等待子线程结束后才输出呢
        print("all over !")
        print("正在去重。。。")
        dbhelper.quchong()  # 执行去重的东西
        print("正在等待明天的到来，")
        dbhelper.getAllTitle()
        # time.sleep(60 * 60 * 24)  # 要加一个排错的东西


    def startAutoRun(self,timeSet):         #24小时制的时间输入，传入一个时间的字符串
        name = "hello"
        # schedule.every(10).minutes.do(job, name)
        # schedule.every().hour.do(job, name)
        schedule.every().day.at(timeSet).do(self.job, name)  # 应该也是24小时制的，记得  “输入24小时制的时间字符串
        # schedule.every(5).to(10).days.do(job, name)
        # schedule.every().monday.do(job, name)
        # schedule.every().wednesday.at("13:15").do(job, name)

        while True:
            schedule.run_pending()
            time.sleep(1)





if __name__=="__main__":    # todo 程序需要改写成多进程的程序，充分的调动多核的能力
                             #todo 还有一个问题就是如何才能让主进程等待子进程都完成任务后退出呢，也使用进程检查的那种方法吗，像checkprocess那样
    autoRun = AutoRunAtTime()
    print(time.strftime('%Y.%m.%d', time.localtime(time.time())))  #每天这个时候就把这个东西下载下来
    print("现在的时间是")
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    #设置时间请去config中设置
    # autoRun.startAutoRun(startTime['time'])    #1:00原来时间是1点  todo 改成多进程的，多线程还是和单线程一样的因为GIP锁的原因
    autoRun.startAutoRun("12:56")  # 1:00原来时间是1点  todo 改成多进程的，多线程还是和单线程一样的因为GIP锁的原因

# print(schedule)   Todo 记得待会把这个改回来   这样就是改好了。检查排错的那个怎么办。check的那个不用改,跑完这儿以后把时间修改回去，并且重新启动


# while(1):







