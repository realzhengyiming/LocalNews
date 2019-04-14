#coding =utf-8
import os
import time


# 腾讯这儿有一个滚动的新闻查看，我要爬取3333 篇文章，不知道要爬取多少天的东西啊,包括图片
#http://news.qq.com/articleList/rolls/
#腾讯新闻的,单个页面的东西放在这里了
#然后还有就是包括每篇文章中的图片下载的，每个段落中的，py3的图片下载的东西，下载到某个地方，然后再存起来
#这一页负责本地化一个页面
import chardet

from DBcontrol import DB
from downloadPic import Download
from makebeautifulSoup import makeBS

# todo 凤凰的会乱码的
class fenghuangPageContent:
    def stripImgUrl(self,replacedSrc):
        if(replacedSrc.find(":")!=-1):
            replacedSrc = replacedSrc.replace(":","_")
        if(replacedSrc.find("：")!=-1):
            replacedSrc = replacedSrc.replace("：","_")
        if(replacedSrc.find(".")!=-1):
            replacedSrc=replacedSrc.replace(".", "_")
        if(replacedSrc.find("/")!=-1):
            replacedSrc = replacedSrc.replace("/","_")
        if(replacedSrc.find("-")!=-1):
            replacedSrc = replacedSrc.replace("-","_")
        if(replacedSrc.find("?")!=-1):
            replacedSrc =replacedSrc.split("?")[0]
        if (replacedSrc.find("？") != -1):
            replacedSrc = replacedSrc.replace("？","_")
        if (replacedSrc.find("！") != -1):
            replacedSrc = replacedSrc.replace("！", "_")
        if (replacedSrc.find("\"") != -1):
            replacedSrc = replacedSrc.replace("\"","_")
        if (replacedSrc.find(" ") != -1):
            replacedSrc = replacedSrc.replace(" ","")
        if (replacedSrc.find("“") != -1):
            replacedSrc = replacedSrc.replace("“","")
        if (replacedSrc.find("”") != -1):
            replacedSrc = replacedSrc.replace("”","")
        if (replacedSrc.find("：") != -1):
            replacedSrc = replacedSrc.replace("：", "")
        if (replacedSrc.find("|") != -1):
            replacedSrc = replacedSrc.replace("|", "_")
        return replacedSrc

#-----------------------------------------------我是不是变了，变得越来越精神紧张-----------------------------------------


    def getPlContent(self,url):    #打开pl.ifenghxxx的东西
        title, Hcontent, Tcontent, Acontent = "", "", "", ""
        t = time.time()
        timeStamp = str(int(round(t * 1000)))  # 毫秒级时间戳
        time.sleep(1)
        print("现在网页是：" + url)
        downloadTool = Download(r'/home/default/images')  # 设置下载路径
        dbhelper = DB()

        title, Hcontent, Tcontent, Acontent = "", "", "", ""
        simpleP = []
        soup = None
        soup = makeBS().makesoup(url)
        if soup!=None:
            title = soup.find("head")
        else:
            return title, Hcontent, Tcontent, Acontent

        # print(title)
        # print("标题是")
        if title != None:  # 如果找到的话
            title = title.text.split("_")[0]
            # title=self.fixCssdot(title)
            # print(title)
        else:
            print("没能找到标题，请检查网址 " + url)
            # print(soup)
            # print()
            return title, Hcontent, Tcontent, Acontent  # 不行就返回空的回去


        flag = False     #遇到之前先不写入
        pList = []
        simplePList = [ ]   #这个是
        for p in soup.find_all("p"):
            # print(type(p))
            # print(p)
            try:
                # print(p['class'])
                if p['class'][0]=="f14":
                    # print(p)
                    pList.append(p)
                    flag = True
                if p['class'][0]=="IphoneNone":
                    # print(p['class'])
                    flag = False     #结束跳出
            except Exception as e:
                    if flag:
                        # print("正在添加")
                        pList.append(p)
                    else:
                        # print("停止添加这一条")
                        break

        print(len(pList))  #这个最后一个句子是尾句，
        Plen = len(pList)

        if(len(pList)==1):
            #一个句子的话，首段和尾端都统一起来好了
            print("这个文章只有一个句子 "+url )
            return title,pList[0],pList[0],pList[0]     #这样的话，就不插入


        for  p in pList:
            # print(p)
            if p.text!="":
                pHtml = "<p>"+p.text  + "</p>"
                if pList.index(p) == 0:  # 如果发现索引值是第一个的话，那就是开头了
                    Hcontent = pHtml
                    Acontent=Acontent + pHtml
                    # print("find the header p")
                    # print(phtml)
                elif pList.index(p) == len(pList) - 1:  # 同理如果是最后一个句子，那么你就是结尾了
                    Acontent=Acontent + pHtml
                    Tcontent = pHtml
                else:  # 不是首段和尾端的端口才加入到零散的段落中去
                    Acontent=Acontent + pHtml
                    simplePList.append(pHtml)
            else:    #可能是有图片的这个东西，如果有图片那就这百年这样操作
                if p.find("img")!=None:
                    print("发现图片的段落")
                    for img in p.find_all("img"):    #修改图片路径和下载图片这两个操作
                        #修改里面的图片的地址的东西，然后还有别的什么的
                        imgSrc = img['src']
                        now = time.strftime('%Y%m%d', time.localtime(time.time()))
                        now_date = now + "/"  # 后面下载的文件名是不需要带杠的，后面就不需要带杠杠

                        imgName = self.stripImgUrl(imgSrc)
                        print(imgName)

                        imgName = now_date + self.stripImgUrl(imgName)  # 这儿已经是添加了时间的 了

                        # print("文件名是" + imgName)                                # 这儿下载这个图片到服务器指定的地址上 # 这儿下载这个图片到服务器指定的地址上
                        downloadTool.downloadImg(imgSrc, imgName=imgName, referer=None, now_date=now)

                        imgPScr = "/images/" + imgName + ".jpg"  # 这个html格式图片地址
                        HtmlImg = '<p><img src="' + imgPScr + '"/></p>'

                        if pList.index(p) == 0:  # 如果发现索引值是第一个的话，那就是开头了
                            Hcontent = HtmlImg
                            Acontent = Acontent + HtmlImg

                        elif pList.index(p) == len(pList) - 1:  # 同理如果是最后一个句子，那么你就是结尾了
                            Acontent = Acontent + HtmlImg

                            Tcontent = HtmlImg
                        else:  # 不是首段和尾端的端口才加入到零散的段落中去
                            Acontent = Acontent + HtmlImg

                            simplePList.append(HtmlImg)

        # print("开头结尾是这个")
        # print(Hcontent)
        # print(Tcontent)
        # print("各个分句子在这儿")
        for simpleP in simplePList:    #这儿直接写入进去就可以了
            dbhelper.insertSimpleP(simpleP)  # 这儿这个是一样的
            # print(simpleP)
        return title,Hcontent,Tcontent,Acontent
        # todo 把句子和句子的图片提取出来   完成
        # todo 把这些东西，句子分成 Hcontent 和Tcontent 还有Acontent来进行处理，
        # todo 需要特殊处理的是  图片的链接地址的修改，还有图片的本地化处理，然后就没有别的东西了    ；如果是单个句子的话，还需要单独的进行句子的划分、

        # print("这个是所有的句子的")
        # print(Acontent)
        # print(title)


    def download(self,imgUrl )   :
        pass  #这个函数要做的是下载图片，然后修改图片

    def getNewsContent(self, url):  # 打开news.ifenghxxx的东西，只要打开文章后，然后解析出 首段，尾段，还有中间的普通段落就可以了
        title, Hcontent, Tcontent, Acontent = "", "", "", ""
        t = time.time()
        timeStamp = str(int(round(t * 1000)))  # 毫秒级时间戳
        time.sleep(1)
        print("现在网页是：" + url)
        downloadTool = Download(r'/home/default/images')  # 设置下载路径
        dbhelper = DB()

        title, Hcontent, Tcontent, Acontent = "", "", "", ""
        simpleP = []

        soup = makeBS().makesoup(url)
        if soup ==None:
            return  title, Hcontent, Tcontent, Acontent

        try:
            title = soup.find("head").title
            if dbhelper.ifExists(title):  #如果找到已经存在那就不用再写的拉
                return title,Hcontent,Tcontent,Acontent  #存在的话，就不用再解析和下载图片了
        except Exception as e:
            #一般提示没找到都是
            return   title, Hcontent, Tcontent, Acontent  #也当成没有处理掉就可以了

        # print(title)
        # print("标题是")
        if title != None:  # 如果找到的话
            title = title.text.split("_")[0]
            # title=self.fixCssdot(title)
            # print(title)
        else:
            print("没能找到标题，请检查网址 " + url)
            # print(soup)
            return title, Hcontent, Tcontent, Acontent  # 不行就返回空的回去

        flag = False  # 遇到之前先不写入
        pList = []
        simplePList = []  # 这个是

        for p in soup.find_all("p"):  #找到p就输出来就可以了        你好啊，大哥，我是你的第一个机械硬盘，感觉还行哈，灯光效果怎么样，不怎么会   # print(p.text)
            try:
                if p['class'][0]=="p_time":
                    flag=True
                    continue  #跳过这个的下面的，继续走
                if p['class'][0]=="detailPic":

                    #这儿找到后就下载图片，并且，修改src然后写入进去，就是那个模块了， todo 有空变成模块
                    imgSrc = p.img['src']
                    imgName = imgSrc.replace("https://inews.gtimg.com/", "").replace("/", "_")
                    now = time.strftime('%Y%m%d', time.localtime(time.time()))
                    now_date = now + "/"  # 后面下载的文件名是不需要带杠的，后面就不需要带杠杠
                    imgName = now_date + self.stripImgUrl(imgName)  # 这儿已经是添加了时间的 了

                    # print("文件名是" + imgName)                                # 这儿下载这个图片到服务器指定的地址上 # 这儿下载这个图片到服务器指定的地址上
                    downloadTool.downloadImg(imgSrc, imgName=imgName, referer=None, now_date=now)

                    # now_date = now + "/"                                     # 后面下载的文件名是不需要带杠的，后面就不需要带杠杠
                    # imgName = now_date + self.stripImgUrl(imgName)   #已经处理好了
                    imgPScr = "/images/" + imgName + ".jpg"  # 这个html格式图片地址

                    #传进来是img的url下载并且修改后当成普通的段落进行处理
                    pList.append('<img src=' + imgPScr + '/>')  # 统一起来把，后面会有加东西
                    # print("<p><img src='"+p.img['src']+"'/></p>")
                if p.text=="用微信扫描二维码分享至好友和朋友圈":
                    flag=False    #找到了这个就是到结尾了
                    pass
            except Exception as e:
                pass
                if flag:
                    # print("正在添加")
                    pList.append(p)
                else:
                    # print("停止添加这一条")
                    break
        # print(len(pList))  # 这个最后一个句子是尾句，
        Plen = len(pList)
        if (len(pList) == 1):
            # 一个句子的话，首段和尾端都统一起来好了
            print("这个文章只有一个句子 " + url)
            return title, pList[0], pList[0], pList[0]  # 这样的话，就不插入

        PPlist =[]
        continueFlag =False
        for pOne in pList:
            try:
                p=pOne.text
            except Exception : #那就是图片的那个了，我知道是什么来的
                p= pOne
            # print(pOne)
            if(p!=""):
                # print(p.strip("\n"))
                if p.strip("\n")=="用微信扫描二维码分享至好友和朋友圈" and continueFlag==False:   #有些有有些没有的
                    # print("找到第一个这个东西")
                    # continue
                    continueFlag=True
                elif p.strip("\n")=="用微信扫描二维码分享至好友和朋友圈" and continueFlag==True:   #有些有有些没有的
                    # print("这儿是结束的地方")
                    continueFlag="break"
                if continueFlag==True:
                    if(p!="用微信扫描二维码分享至好友和朋友圈"):
                        p = "<p>"+p+"</p>"
                        #这儿是把"'"  这个东西替换成'"'   这个东西
                        # if p.find("'")!=-1:
                        #     print("找到了这个东西")


                        PPlist.append(p)
                if continueFlag=='break':
                    break

            else:
                pass  #图片都会在前面进行处理才对的
                #检查一下是不是图片的
                # print("文字卫空空那")
                # if pOne.find("img")!=None:  #因为图片是处理过的了，那么就直接加入进去就可以了
                #     print(p)


        # print(PPlist)


        if(len(PPlist))==1 and len(PPlist)==2: #还有2都是这种情况
            Hcontent= PPlist[0]
            Tcontent= PPlist[0]
            Acontent = PPlist[0]
        if(len(PPlist))>2:
            Hcontent = PPlist[0]
            Tcontent= PPlist[-1]
            for i in PPlist:
                Acontent = Acontent + i
                # print(i)  # 你好啊
            # Acontent = PPlist

        # print("普通的段落有")
        simplePList = PPlist[1:-1]





            # print(p)
        # print("开头结尾是这个")
        # print(Hcontent)
        # print(Tcontent)
        # print("各个分句子在这儿")
        for simpleP in simplePList:  # 这儿直接写入进去就可以了
            dbhelper.insertSimpleP(simpleP)  # 这儿这个是一样的
            # print(simpleP)
        return title, Hcontent, Tcontent, Acontent
        # todo 把句子和句子的图片提取出来   完成
        # todo 把这些东西，句子分成 Hcontent 和Tcontent 还有Acontent来进行处理，

#-------------------------------这边开始不是这样的了-------------------------------------------------------------

    def getPageContent(self,url): #输入一个url获得这个页面的本地化后的文章   ,其实分这个应该是不需要那么麻烦的把，，，，
        t = time.time()
        timeStamp =str(int(round(t * 1000)))  # 毫秒级时间戳
        time.sleep(1)

        downhelp = Download(r'/home/default/images') #设置下载路径
        dbhelper = DB()

        title,Hcontent,Tcontent,Acontent="","","",""
        simpleP =[]
        soup = None
        try:
            soup = makeBS().makesoup(url)

            # print(soup)

            title =soup.find("head").title
            # print(chardet.detect(title.text))   测不准的这个东西
            # print(title)

            if title!=None:
                title = title.text
                print("标题是" + str(title))
            main_content = soup.find("div",attrs={"id":"main_content"})
            flag = 1
            if(main_content!=None):
                allPP =main_content.find_all("p")
                for p in range(0,len(allPP)):
                    # print()
                    # print(allPP[p])
                    # print(p)
                    if allPP[p].find_all("a")!=None:
                        # print("找到了有链接的东西")
                        # print(allPP[p])
                        allPP[p].a.extract()
                        # print(allPP[p])


                    localImgList = allPP[p].find_all("img",attrs={"src":True})  # 每个p标签内的img提取和修改链接本地化

                    if (localImgList != None):  # 找到有的话就遍历，并且本地化还有修改src的东西
                        for img in localImgList:
                            if img != None :
                                # print("发现图片")
                                # print(img)
                                # print(img['src'])
                                if (img['src'].find("//") == 0):  # 什么都没有，协议路径改成https
                                    imgSrc = "https:" + img['src']
                                    # print(imgSrc)

                                    now = time.strftime('%Y%m%d', time.localtime(time.time()))
                                    now_date = now + "/"  # 后面下载的文件名是不需要带杠的，后面就不需要带杠杠
                                    imgName = now_date + self.stripImgUrl(imgSrc)

                                    # print("文件名是" + imgName)

                                    # print(imgName)
                                    downhelp.downloadImg(imgSrc, imgName=imgName,referer=None,now_date=now)  # 下载这个是没问题的
                                    img['src'] = "/images/" + imgName + ".jpg"  #修改完后的img
                                    # print(img['src'])

                                    simpleP.append(allPP[p])
                                    Acontent += str(allPP[p])

                                    # Acontent += str(allcontent[i])
                                elif (img['src'].find("https:") == 0):  # 本来就有找到有https协议
                                    imgSrc = img['src']
                                    # print(imgSrc)

                                    now = time.strftime('%Y%m%d', time.localtime(time.time()))
                                    now_date = now + "/"  # 后面下载的文件名是不需要带杠的，后面就不需要带杠杠
                                    imgName = now_date + self.stripImgUrl(imgSrc)

                                    downhelp.downloadImg(imgSrc, imgName=imgName, referer=None,now_date=now)
                                    img['src'] = "/images/" + imgName + ".jpg"
                                    # print(img['src'])
                                    simpleP.append(allPP[p])
                                    Acontent += str(allPP[p])

                                else:  # 那这个就是http协议了
                                    imgSrc = img['src']
                                    # print(imgName)

                                    now = time.strftime('%Y%m%d', time.localtime(time.time()))
                                    now_date = now + "/"  # 后面下载的文件名是不需要带杠的，后面就不需要带杠杠
                                    imgName = now_date + self.stripImgUrl(imgSrc)

                                    downhelp.downloadImg(imgSrc, imgName=imgName, referer=None,now_date=now)
                                    img['src'] = "/images/" + imgName + ".jpg"
                                    # print(img['src'])
                                    simpleP.append(allPP[p])
                                    Acontent += str(allPP[p])
                    if (p == 0):                             #这儿是判断是首段还是尾段
                        Hcontent = allPP[p]    #这个是找标题的,这个是修改后的了
                    elif (p==len(allPP)-1):
                        print("找到尾段了拉")
                        Tcontent = allPP[p]

                # for p in simpleP:
                    # dbhelper.insertSimpleP(p) #这儿这个是一样的  todo 记得改回来这儿的地方
                return title, Hcontent, Tcontent, Acontent
            else:
                title="凤凰没有找到标题"
                return title, Hcontent, Tcontent, Acontent
        except Exception as e:
            print(e)
            print("现在网页是：" + url)
            return title, Hcontent, Tcontent, Acontent
if __name__ == "__main__":
    url = "http://news.ifeng.com/a/20181010/60101407_0.shtml"
    # url = "https://pl.ifeng.com/a/20181010/60101359_0.shtml"
    url = "https://pl.ifeng.com/a/20181010/60101330_0.shtml"     #纵欲找到一个有图的了 ，这种叫做什么来着，凤凰评论
    # todo 测试多几个这种凤凰评论的东西  news 图片的那个东西给筛选 掉了，要找回来这个东西才可以
    # url ="https://pl.ifeng.com/a/20181011/60103045_0.shtml"
    # url ="https://pl.ifeng.com/opinion/fenghuanglun/382/1.shtml"     #那个国际妇女节的那个版面又不一样了，所以不行的

    # url = "http://news.ifeng.com/a/20180729/59493105_0.shtml#p=2"    #这种是图片新闻，是不行的，不要的。
# url ="http://news.ifeng.com/a/20180729/59493174_0.shtml"
    url = "http://news.ifeng.com/a/20180729/59493013_0.shtml"    #这个 是那个偷手机买酒的那个男的，有图片
    # url ="http://news.ifeng.com/a/20181010/60101370_0.shtml"
    # url ="http://news.ifeng.com/a/20181010/60101321_0.shtml"

    # url ="http://news.ifeng.com/a/20181010/60101441_0.shtml"

    # url = "http://news.ifeng.com/a/20181010/60102248_0.shtml"

    # url ="http://news.ifeng.com/a/20181010/60101407_0.shtml"
    url = "http://news.ifeng.com/a/20181010/60101441_0.shtml"

    url = "http://news.ifeng.com/a/20190120/60244021_0.shtml"





    #这个就是new,里面版面更加不同了,这个需要再写一个解析页面的东西,这个东西.
    #   http://news.ifeng.com/a/20181004/60095007_0.shtml
    #   http://news.ifeng.com/a/20181005/60095977_0.shtml
    #   todo 那个 妇女的东西

    #  todo还有图片  http://news.ifeng.com/a/20181013/60107016_0.shtml#p=1  图片新闻 todo







    pageContent = fenghuangPageContent()
    # print(pageContent.getPageContent(url))
    title, Hcontent, Tcontent, Acontent =pageContent.getNewsContent(url)     #第二种的这个是解析凤凰资讯的页面
    print("标题是")
    print(title)
    print("header p is ")
    print(Hcontent)
    print("完整的文章为")
    print(Acontent)
    print("tail p is ")
    print(Tcontent)

    # pageContent.getPlContent(url)