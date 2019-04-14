#coding=utf-8
#定时开始工作
''''
这个就是用来设置定时工作的东西的  ，记得服务器的时间比我现在的这儿的时间快两分钟
封装成类

'''


import schedule
import time

class AutoRunAtTime:
    def job(self,name):
        print("her name is : ", name)


    def startAutoRun(self,timeSet):         #24小时制的时间输入
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



if __name__=="__main__":
    autoRun = AutoRunAtTime()
    autoRun.startAutoRun("18:36")
    # print(schedule)