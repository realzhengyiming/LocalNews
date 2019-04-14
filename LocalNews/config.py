#这个是配置文件
'''
目前有需要的设置
1.数据库的配置设置

'''

mysqlInfo = {
    "host": '127.0.0.1',
    "user": 'root',
    "passwd": 'Z123321#',
    "db": 'caiji',
    "port": 3306,
    "charset": 'utf8'  #这个是数据库的配置文件
}


startTime ={   #设定的运行时间，测试的话请输入大于你当前计算机时间的1分钟，如16：53-》16:54
    "time":""  #请用24小时制的字符串，win下如 '01:10'表示每天1点10分开始；如果是linux，'1:10'这样都可以
}

serverName  = "测试用爬虫服务器"

#这儿目前只支持QQ邮箱，授权码这个config自己手动的设置就可以了，自动化的配置的文件都在这儿了
EmailAdress ={
        'fromAdd' : "1403459511@qq.com",  # 你的邮箱   发件地址
        # to_ = input('Please input Recipient:')  # 收件地址
        'toAdd' : "1403459511@qq.com",
        # subject = input('Please input title:')  # 邮件标题

        'pwd' : "urckpwbbgbeqhdec",  # 授权码  nkijfhnodibbiifb  smtp tmap

        #报告的主题分级
        'serverName':'测试用爬虫服务器',

        'ordernaryReport':serverName+"-"+"服务器爬虫日常数据汇报" , #这个是用来发送平时的每日数据汇报的情况的
        'ordernaryDeadlyReport': serverName+"-"+"服务器爬虫崩溃检修报告" ,#这个用于日常的服务器中爬虫死亡了提供崩溃信息还有数据汇报总结




}