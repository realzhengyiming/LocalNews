## -*- coding: utf-8 -*-


#2018/9/8 修改成使用连接池的方式来进行数据库的链接
import random
from datetime import date, timedelta

import pymysql as pymysql
import time
from DBUtils.PooledDB import PooledDB


from config import mysqlInfo

#提取返回数据的全部变成了返回字典类型
#这个是连接数据库的东西,这次使用数据库连接池把，使用连接池可以避免反复的重新创建新连接
#todo 这儿有一个问题关于插入失败的，1.是插入的字符串中文gbk编码的，需要转换，2.就是可能会遇到emoji表情嘛？有可能的
# todo 还有一个问题就是就是api （腾讯）字典key突然读取为空，没有这个key出现错误，什么鬼，健壮性要搞一下
# todo 执行sql的时候就需要try catch 不然就崩溃了

class DB:  #一个对象一个数据库连

    __pool = None   #这个也是静态的属性

    def __init__(self):
        # 构造函数，创建数据库连接、游标，默认创建一个对象就获得一个连接，用完后就关闭就可以了
        self.coon = DB.getmysqlconn()  #这个是默认创建出来的东西
        self.cur = self.coon.cursor(cursor=pymysql.cursors.DictCursor)

    # 数据库连接池连接
    @staticmethod   #这个是静态的方法可以直接调用的
    def getmysqlconn():  #从连接池里面获得一个连接
        if DB.__pool is None:
            __pool = PooledDB(creator=pymysql, mincached=2, maxcached=20, host=mysqlInfo['host'],
                                  user=mysqlInfo['user'], passwd=mysqlInfo['passwd'], db=mysqlInfo['db'],
                                  port=mysqlInfo['port'], charset=mysqlInfo['charset'])
            # print(__pool)

        return __pool.connection()

        # 释放资源
    def dispose(self): #这儿只能断默认初始化的那个连接
        self.coon.close()
        self.cur.close()





    # def refreshConnection(self):  #晚点再改成连接池的形式
    #     self.db = pymysql.connect(host="localhost", user="root", charset='utf8', password="Z123321#", db="caiji",port=3306)
    #     #再设置一次

    def __query__(self,sql):  #自定义查询
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)  #这儿这个选项是设置返回结果为字典的类型，如果默认的话，那就是列表i
        cur.execute(sql)
        URLs = cur.fetchall()
        cur.close()
        coon.close()
        return URLs

    def ifExists(self,webTitle):
        coon = DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "SELECT * FROM tengxun WHERE title='%s'and urlState='True';"
        #因为这儿没有加上try，catch，所以出问题
        try:
            cur.execute(sql%(webTitle))
        except Exception as e:
            print(e)
            print("函数ifExists出问题了，你检查一下")
            print(sql%(webTitle))
        rowNumber = cur.rowcount
        if rowNumber>0:
            return True
        else:
            return False




    def __randomP__(self):
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        # sql = "insert into tengxun (Acontent) values( '" + content + "') where url=%s;"% url
        sql = "SELECT * FROM simpleP WHERE id>= ((SELECT MAX(id) FROM simpleP )-(SELECT MIN(id) FROM simpleP )) * RAND() + (SELECT MIN(id) FROM simpleP ) LIMIT 10;"
        cur.execute(sql)
        URLs = cur.fetchall()
        allHtml = ""
        # print(URLs)
        for row in URLs:
            # print(row)
            # print(type(row))
            # print(type(row['oneP']))
            
            allHtml=allHtml+row['oneP']
        if (len(allHtml)<800):
            allHtml=allHtml+self.__randomP__()  #递归算法
        # print('共查找出', cur.rowcount, '条数据')
        # self.__close__()
        cur.close()
        coon.close()
        return allHtml

    def updateMixState(self,id):
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
        # print(url)  之前是这儿的语句错了嘛，还以为哪儿的问题
        # print(id)
        sql = "update tengxun set hadmix='True' where id = %d;" % int(id)   #就只是更新一下相应的url的状态就可以了
        # print(sql)
        try:  #像这样容易出问题的
            cur.execute(sql)
            # 提交
            coon.commit()
        except Exception as e:
            # 错误回滚
            print("更新hadmix失败，请检查updateMixState")
            print(e)
            coon.rollback()

        finally:
            # print("插入成功")
            coon.commit() #提交这个事务
            cur.close()
            coon.close()
        
    def updateState(self,id):   #混合过一个就用那个urlstate这个字段，这样不就不会重复了嘛，随机的是段落不是标题和开头
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        # print(url)  之前是这儿的语句错了嘛，还以为哪儿的问题
        # print(id)
        sql = "update tengxun set urlState='True' where id = %d;" % int(id)   #就只是更新一下相应的url的状态就可以了
        # print(sql)
        try:  #像这样容易出问题的
            cur.execute(sql)
            # 提交
            coon.commit()
        except Exception as e:
            # 错误回滚
            print("更新失败，请检查updateState")
            print(e)
            coon.rollback()

        finally:
            # print("插入成功")
            coon.commit() #提交这个事务
            cur.close()
            coon.close()
        
        

    def __randomHandT__(self):   #这个是随机抽出一个标题，和开头可结
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        #lists = self.__query__("select * from tengxun where title!='' ;")
        #maxId = len(lists)
        #number = random.randint(1,maxId)
        # sql = "insert into tengxun (Acontent) values( '" + content + "') where url=%s;"% url
        #sql ="SELECT * FROM tengxun WHERE title!=''and id>= ((SELECT MAX(id) FROM tengxun where title!='' )-(SELECT MIN(id) FROM tengxun where title!='' )) * RAND() + (SELECT MIN(id) FROM tengxun where title!=''  )   LIMIT %d;" % 1
        #sql1 = "select * from tengxun where title!='' and id <=%d limit 1" % number
        #urlState 是有没有用过这个新闻的标题的东西来的，然后还要有开头段落
        sql1= "select * from tengxun  where title!='' and hadmix = 'False'  limit 0,1;"
        #这儿出了点问题，就是这个检测的这个其实是用来验证有没有生成mix

        cur.execute(sql1)
        lists = cur.fetchall()
        # print(lists[0])
        # print("查找到的结果有那么多哈")
        # print(cur.rowcount)
        if(cur.rowcount==1):
            # print("剩下的结果是1")
            # print(type(cur.fetchall()[0]))
            # print(lists[0]['title'])
            onePart = lists[0]['title'] #选出里面的一个元素

            # print(type(onePart[0]))
            # print(onePart)


            self.updateState(lists[0]['id'])  #更新这个状态的东西就可以了，所以才需要这个东西,这儿应该传的是id，list ，dic嵌套
            # print(onePart)

            # print(onePart[2],onePart[4],onePart[6])
            title,header,tail,id =lists[0]['title'],lists[0]['Hcontent'],lists[0]['Tcontent'],lists[0]['id']

            if(title==None):
                title =self.__randomHandT__()  #继续递归
            cur.close()
            coon.close()
            return title,header,tail,id
        else:
            cur.close()
            coon.close()
            return "","","",0



        # return db,cur #返回两个东西来接应它

    def saveListToMysql(self,urlList ,date,fromWhere):               #逐条调用把list写入数据库而已拉
        for url in urlList:
            # if self.checkWhetherInDB(url):   #如果没有这条数据，那么就写入，并且提取出页面
            self.insertTenxun(url,date,fromWhere)          #去重，不重复写入数据库
            # else:
            #     urlList.remove(url)          #删掉这个url元素，不用插入的话
        return urlList





    def insertTenxun(self,url,date,fromWhere): #这个是把网址先存到里面去url，这儿的意思是插入tengxun那个表
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        sql = "insert into tengxun (url,newdate,fromWhere) values( '" + url + "','" + date + "','"+fromWhere+"');"
        # print(sql)
        try:
            cur.execute(sql)
            # 提交
            coon.commit()
            print("插入成功。")
        except Exception as e:
            # 错误回滚
            print("数据表中已经有此url，跳过插入此")
            print(sql)
            print(e)
            coon.rollback()
        finally:
            # print("插入成功")
            coon.commit() #提交这个事务
            cur.close()
            coon.close()

            # self.__close__()

    def updateContent(self,url,title,Hcontent,Tcontent,Acontent):  #这三个都看成一部分，一次性的存进去好吧
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        Hcontent = str(Hcontent)
        Tcontent = str(Tcontent)
        Acontent = str(Acontent) #beautiful标签转制一下不然就是tag

        # print(url)  之前是这儿的语句错了嘛，还以为哪儿的问题
        sql = "update tengxun set  title='"+title+"' , Acontent = '" + Acontent + "' ,Hcontent = '"+Hcontent+"' , Tcontent = '"+Tcontent+"' ,hadmix='False'  where url='%s';"% url   #能填成功那就说明可以，可以用这个新的来合成新的混合文章
        # print(sql)
        try:
            cur.execute(sql)
            # 提交
            coon.commit()
            return True   #更新成功，返回这个
        except Exception as e:
            # 错误回滚
            print("更新失败，请检查updateContent,标题或者 url已经存在了拉")
            print(sql)
            '''   上次的错误提示
            更新失败，请检查updateContent
            update tengxun set  title='习近平对政法工作作出重要指示' , Acontent = '' ,Hcontent = '视频：习近平对政法工作作出重要指示，时长约1分43秒' , Tcontent = '<p><iframe frameborder="0" src="https://v.qq.com/txp/iframe/player.html?vid=h0025szp8ya" allowFullScreen="true"></iframe></p>'   where url='http://news.qq.com/a/20180122/022335.htm';
            http://news.qq.com/a/20180122/022335.htm
            (1062, "Duplicate entry '习近平对政法工作作出重要指示' for key 'title'")
            '''
            print(url)  #url不同，但是呢，同样标题的新闻已经有了，获取，其实url也相同，那就把这个id删掉好了
            print(e)
            coon.rollback()
            return False             #更新失败的话，比如重复了标题这种，那就删除这个url
        finally:
            # print("插入成功")
            coon.commit() #提交这个事务
            # self.__close__()
            cur.close()
            coon.close()

    def insertWangyi(self,url):
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        now_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 获取当前日期,每次执行操作的时候都这样
        sql = "insert into tengxun (url,newdate,fromWhere) values( '" + url + "','" + now_date + "','wangyi');"
        # print(sql)
        try:
            cur.execute(sql)
            # 提交
            coon.commit()
        except Exception as e:
            # 错误回滚
            print("插入wangyi出现问题")
            print(e)
            coon.rollback()
        finally:
            # print("插入成功")
            coon.commit() #提交这个事务
            cur.close()
            coon.close()



    def getLimitUrl(self,start,end,fromWhere):   #提取url然后进行提取段落处理
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        # sql = "insert into tengxun (Acontent) values( '" + content + "') where url=%s;"% url
        sql = "SELECT url ,newdate FROM tengxun where fromWhere='"+fromWhere+"' and  isNull(title) LIMIT %d,%d;" % ( start ,end )  #只选出空的
        # print(sql)
        cur.execute(sql)
        URLs = cur.fetchall()
        for row in URLs:
            # print(row)
            print("url:%s  日期：%s" % ( row['url'],row['newdate']))
        print('共查找出', cur.rowcount, '条数据')
        # self.__close__()
        cur.close()
        coon.close()

        return URLs

    def checkWhetherInDB(self,url):
        # url = "http://news.ifeng.com/a/20180820/59909441_0.shtml"
        # url = "dadafdads"
        sql = "select * from tengxun where url='%s'"
        result = self.__query__(sql % url)
        if len(result)==0: #说明没有数据
            return True  # 可以插入：
        else:
            return False  #不用再插入进去了

        # return False

    def insertSimpleP(self,Pcontent):
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        Pcontent = str(Pcontent)
        sql = "insert into simpleP (oneP,number) value( '" + Pcontent + "'," + str(len(Pcontent)) + ");"
        # print(sql)
        try:
            cur.execute(sql)
            # 提交
            coon.commit()
        except Exception as e:
            # 错误回滚
            print("插入simpleP出现问题")
            print(sql)
            print(e)
            coon.rollback()
        finally:
            # print("插入成功")
            coon.commit() #提交这个事务
            cur.close()
            coon.close()


    def insertMixP(self,title,mixP):


        if(title !="" and mixP !=""):
            coon = DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
            cur = self.coon.cursor(cursor=pymysql.cursors.DictCursor)

            sql = "insert into c_title  ( title ,content,yuan_id,object_id,caiji_id ) values ( '" + title + "','" + mixP + "',1,0,1 );"
            # print(sql)
            try:
                cur.execute(sql)
                # 提交
                coon.commit()
            except Exception as e:
                # 错误回滚
                print("插入c_title出现问题")
                print(sql)
                print(e)
                coon.rollback()
            finally:
                # print("插入成功")
                coon.commit() #提交这个事务
                # self.__close__()
                cur.close()
                coon.close()
        else:
            print("插入的为空，跳过插入")
            pass

    def deleteUrl(self,url):
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        sql = "delete from tengxun where url ='%s';" % url
        try:
            # 执行SQL语句
            cur.execute(sql)
            # 提交修改
            coon.commit()
            print("删除成功哈 "+url)
        except Exception as e:
            print(e)
            # 发生错误时回滚
            print("删除失败，查看deleteUrl")
            print(sql)
            coon.rollback()
        # 关闭连接
        finally:
            coon.commit()
            cur.close()
            coon.close()


    def quchong(self):  #这个是用来去重的，
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
        sql ='DELETE FROM simpleP WHERE id NOT IN(SELECT * FROM(SELECT id FROM simpleP GROUP BY oneP )AS b);'
        # print(sql)
        try:
            cur.execute(sql)
            # 提交
            coon.commit()
        except Exception as e:
            # 错误回滚
            print("数据库取出url相同的重复，title相同的重复自动跳过")
            print(sql)
            print(e)
            coon.rollback()
        finally:
            # print("插入成功")
            coon.commit() #提交这个事务
            # self.__close__()
            cur.close()
            coon.close()

    def testDB(self):
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        # self.db.close()
        sql = "select * from tengxun ;"
        cur.execute(sql)
        URLs = cur.fetchall()
        for row in URLs:
            print("url:%s  日期：%s" % (row[0], row[1]))
        print('共查找出', cur.rowcount, '条数据')
        # self.__close__()
        cur.close()
        coon.close()
        return URLs

    def updateSimpleP(self,id,oneP):
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "update simpleP set oneP ='%s' where  id =%d" % (oneP,id)
        try:
            cur.execute(sql)
            coon.commit()
        except Exception as e:
            # 错误回滚
            print(e)
            coon.rollback()
        finally:
            coon.commit()  # 提交这个事务
            cur.close()
            coon.close()

    def updateHTMA(self,id,h,t,A):
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
        # print(url)  之前是这儿的语句错了嘛，还以为哪儿的问题
        sql = "update tengxun set Hcontent ='%s' ,Tcontent='%s',Acontent='%s' where  id=%d ;" % (h,t,A,id)
        try:
            cur.execute(sql)
            coon.commit()
        except Exception as e:
            # 错误回滚
            print(e)
            coon.rollback()
        finally:
            coon.commit()  # 提交这个事务
            cur.close()
            coon.close()

    def updateCtitle(self,id,content):
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
        # print(url)  之前是这儿的语句错了嘛，还以为哪儿的问题
        sql = "update c_title set content ='%s'  where  id=%d ;" % (content,id)
        try:
            cur.execute(sql)
            coon.commit()
        except Exception as e:
            # 错误回滚
            print(e)
            coon.rollback()
        finally:
            coon.commit()  # 提交这个事务
            cur.close()
            coon.close()



    #这个几个是当时临时修改src用的
    def changeSrc(self):   #自动遍历这个东西，记得带上检查是否断开的东西,这个已经处理后就不用再管了
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "select * from tengxun  where title!='' and Hcontent!='' ;" #遍历这里面整个的数据库的东西

        print(sql)
        cur.execute(sql)
        URLs = cur.fetchall()
        for row in URLs:  #字段是 id - oneP  - 字数，就用第一个和第二个就可以了
            id =row[0]
            h = row[4]
            t = row[6]
            A = row[7]
            if(h.find('images/')!=-1):  #有这种的一定是路径来的
                print("找到了images需要修改")
                # src = "images/newsapp_bt_0_2636735713_641.jpg"
                h = h.replace('images/','''/images/''')
            if (t.find('images/') != -1):  # 有这种的一定是路径来的
                print("找到了images需要修改")
                    # src = "images/newsapp_bt_0_2636735713_641.jpg"
                t = t.replace('images/', '''/images/''')
                # self.updateHTMA(id, h, t, m, A)
            if (A.find('images/') != -1):  # 有这种的一定是路径来的
                print("找到了images需要修改")
                # src = "images/newsapp_bt_0_2636735713_641.jpg"
                A = A.replace('images/', '''/images/''')

            self.updateHTMA(id, h, t, A)
            print("修改后为： "+h,t,A)
        cur.close()
        coon.close()

        def changeSrc(self):  # 自动遍历这个东西，记得带上检查是否断开的东西
            coon = DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
            cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
            sql = "select * from tengxun  where title!='' and Hcontent!='' ;"  # 遍历这里面整个的数据库的东西

            print(sql)
            cur.execute(sql)
            URLs = cur.fetchall()
            for row in URLs:  # 字段是 id - oneP  - 字数，就用第一个和第二个就可以了
                id = row[0]
                h = row[4]
                t = row[6]
                A = row[7]
                if (h.find('images/') != -1):  # 有这种的一定是路径来的
                    print("找到了images需要修改")
                    # src = "images/newsapp_bt_0_2636735713_641.jpg"
                    h = h.replace('images/', '''/images/''')
                if (t.find('images/') != -1):  # 有这种的一定是路径来的
                    print("找到了images需要修改")
                    # src = "images/newsapp_bt_0_2636735713_641.jpg"
                    t = t.replace('images/', '''/images/''')
                    # self.updateHTMA(id, h, t, m, A)
                if (A.find('images/') != -1):  # 有这种的一定是路径来的
                    print("找到了images需要修改")
                    # src = "images/newsapp_bt_0_2636735713_641.jpg"
                    A = A.replace('images/', '''/images/''')

                self.updateHTMA(id, h, t, A)
                print("修改后为： " + h, t, A)
            cur.close()
            coon.close()


    def changCaiji(self):  # 自动遍历这个东西，记得带上检查是否断开的东西
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "select * from c_title ;"  # 遍历这里面整个的数据库的东西

        # print(sql)
        cur.execute(sql)
        URLs = cur.fetchall()
        for row in URLs:  # 字段是 id - oneP  - 字数，就用第一个和第二个就可以了
            id = row[0]
            content = row[2]
            # t = row[6]
            # A = row[7]
            if (content.find('images/') != -1):  # 有这种的一定是路径来的
                print("找到了images需要修改")
                # src = "images/newsapp_bt_0_2636735713_641.jpg"
                content = content.replace('images/', '''/images/''')

            self.updateCtitle(id,content)
            print("修改后为： " + content)
        cur.close()
        coon.close()



        print('共查找出', cur.rowcount, '条数据')
        print("数据库中的数据已经修改完毕，谢谢你的使用")
        # self.__close__()
        # return URLs

    def getAllTitle(self):  #自动获取昨天的所有的标题，然后进行去重处理。按照标题去重
        allTogether = ""
        coon =DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
        cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

        # self.db.close()
        now_date = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")  # 昨天日期
        print(now_date)
        sql = "select * from tengxun where newdate='%s';"%now_date   #使用sql拼接是很不安全的啊。
        cur.execute(sql)
        URLs = cur.fetchall()
        for row in URLs:
            # print(row)
            print(row['title'])
            allTogether+=row['title']
            # print("url:%s  日期：%s" % (row[0], row[1]))
        print('共查找出', cur.rowcount, '条数据')
        # self.__close__()
        cur.close()
        coon.close()
        return allTogether



    #迭代时间2019-03-16 14:48 新增之后整理的函数
    def saveDicToMysql(self, urlList, date, fromWhere):  #[{}]的嵌套的结构，这个是存如tengxun表中的，未整理前
        # dictList = dict(urlList)
        dictList = urlList
        for category in dictList:
            # print(category)
            for url in dictList[category]:
                self.insertTengxunTheme(url,date,fromWhere,category)   #四个参数都有了这样。

        print("finish!good!")




    def insertTengxunTheme(self, url, date, fromWhere ,category):  #[{}]的嵌套的结构
        def insertTenxun(self, url, date, fromWhere):  # 这个是把网址先存到里面去url，这儿的意思是插入tengxun那个表
            coon = DB.getmysqlconn()  # 每次都默认获得一个新连接来进行相关的操作
            cur = coon.cursor(cursor=pymysql.cursors.DictCursor)

            sql = "insert into tengxun (url,newdate,fromWhere,category) values( '" + url + "','" + date + "','" + fromWhere + "','" + category + "');"
            print(sql)
            try:
                cur.execute(sql)
                # 提交
                coon.commit()
                print("插入成功！")
            except Exception as e:
                # 错误回滚
                print("数据表中已经有此url，跳过插入此")
                print(sql)
                print(e)
                coon.rollback()
            finally:
                # print("插入成功")
                coon.commit()  # 提交这个事务
                cur.close()
                coon.close()



if __name__ == "__main__":  #下面都是用来测试用的。
    chak = DB()
    chak.getAllTitle()
    # chak.__randomHandT__()
    # chak.__randomP__()

    # all =chak.__query__("select * from tengxun  where title!='' and urlState = 'True'  limit 0,1")

    # all = chak.getLimitUrl(0,6,"tengxun")
    # print(all)
    # print("finish!")


    # url  ="http://news.ifeng.com/a/20180820/59909441_0.shtml"
    # url = "dadafdads"
    # sql = "select * from tengxun where url='%s'"
    # result = chak.__query__(sql%url)
    # print(result)
    # print(len(result))

    # todayNewUrl = chak.__query__("select url from tengxun where urlState='False'")
    # if chak.ifExists("WAHT DEHDA"):
    #     print(True)
    # else:
    #     print(False)
    # allTogether = chak.getAllTitle()

    print("finish!")


# 关闭游标


