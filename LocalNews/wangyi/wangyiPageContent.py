#coding =utf-8
import os
import time



#这儿要分三种网址进行打开处理，待会继续写这个打开网页的
from DBcontrol import DB
from downloadPic import Download
from makebeautifulSoup import makeBS
from wangyi.wangyiUrls import DateUrl
import traceback


class wangyiPageContent:
    def __init__(self):
        self.dbhelper=DB()
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

    def fixCssdot(self,pContent):
        # print(pContent)
        if(pContent.find("'"))!=-1:                    #找到有单引号的，这种多是样式的东西
            replaceString = pContent.replace("'",'"')
            # print(replaceString)
            return replaceString
        elif pContent.find("\n"):
            return pContent.replace("\n","")

        else:
            return pContent
    # def getPageContent(self,url): #输入一个url获得这个页面的本地化后的文章
    #     t = time.time()
    #     timeStamp =str(int(round(t * 1000)))  # 毫秒级时间戳
    #     time.sleep(1)
    #     downhelp = Download(r'/home/default/images') #设置下载路径
    #
    #     dbhelper = DB()
    #
    #     title,Hcontent,Tcontent,Acontent="","","",""  #要返回的这几个东西
    #     simpleP = []
    #     soup =makeBS().makesoup(url)
    #     # print(soup.prettify())
    #     title = soup.find("h1",attrs={"class":True})
    #     print("标题 ",title)
    #     if (title!=None):
    #         title  = title.text
    #         if(title.find(":")!=-1):
    #             title = title.replace(":","")
    #
    #     main_content =  soup.find("div",attrs={"class":"post_text"})
    #     if (main_content != None):
    #         allPP = main_content.find_all("p")
    #         for p in range(0, len(allPP)):
    #             localImgList = allPP[p].find_all("img", attrs={"src": True})  # 每个p标签内的img提取和修改链接本地化
    #             if (p == 0):
    #                 Hcontent = allPP[p]
    #             if (localImgList != None):  # 找到有的话就遍历
    #                 for img in localImgList:
    #                     if img != None:
    #                         print(img)
    #                         print(img['src'])
    #                         if (img['src'].find("//") == 0):  # 什么都没有，协议路径改成https
    #                             imgSrc = "https:" + img['src']
    #                             # filename = os.path.basename(imgSrc)
    #                             print(imgSrc)
    #                             # imgName = timeStamp + self.stripImgUrl(imgSrc)
    #                             now = time.strftime('%Y%m%d', time.localtime(time.time()))
    #                             now_date = now + "/"  # 后面下载的文件名是不需要带杠的，后面就不需要带杠杠
    #                             imgName = now_date + self.stripImgUrl(imgSrc)
    #
    #                             print("文件名是" + imgName)
    #                             downhelp.downloadImg(imgSrc, imgName=imgName, referer=None,now_date=now)  # 下载这个是没问题的
    #                             img['src'] = "/images/" + imgName + ".jpg"  # 修改完后的img
    #                             print(img['src'])
    #
    #                             simpleP.append(allPP[p])
    #                             Acontent += str(allPP[p])
    #
    #                             # Acontent += str(allcontent[i])
    #                         elif (img['src'].find("https:") == 0):  # 本来就有找到有https协议
    #                             imgSrc = img['src']
    #                             # filename = os.path.basename(imgSrc)
    #                             # print(imgSrc)
    #
    #                             now = time.strftime('%Y%m%d', time.localtime(time.time()))
    #                             now_date = now + "/"  # 后面下载的文件名是不需要带杠的，后面就不需要带杠杠
    #                             imgName = now_date + self.stripImgUrl(imgSrc)
    #
    #                             print("文件名是" + imgName)
    #                             downhelp.downloadImg(imgSrc, imgName=imgName, referer=None,now_date=now)
    #                             img['src'] = "/images/" + imgName + ".jpg"
    #                             print(img['src'])
    #                             simpleP.append(allPP[p])
    #                             Acontent += str(allPP[p])
    #
    #                         else:  # 那这个就是http协议了
    #                             imgSrc = img['src']
    #                             # filename = os.path.basename(imgSrc)
    #                             # print(imgSrc)
    #
    #                             now = time.strftime('%Y%m%d', time.localtime(time.time()))
    #                             now_date = now + "/"  # 后面下载的文件名是不需要带杠的，后面就不需要带杠杠
    #                             imgName = now_date + self.stripImgUrl(imgSrc)
    #
    #                             print("文件名是" + imgName)
    #                             downhelp.downloadImg(imgSrc, imgName=imgName, referer=None,now_date=now)
    #                             img['src'] = "/images/" + imgName + ".jpg"
    #                             print(img['src'])
    #                             simpleP.append(allPP[p])
    #                             Acontent += str(allPP[p])
    #
    #         for p in simpleP:  #耦合性极高
    #             dbhelper.insertSimpleP(p) #这儿这个是一样的
    #         print(title, Hcontent, Tcontent, Acontent)
    #         return title, Hcontent, Tcontent, Acontent
    #
    #
    #     else:
    #         title ="网易没找到标题"
    #         return title, Hcontent, Tcontent, Acontent

#---------------------------------------------------这儿的这个是新的了——----------------------------------------------


    def getNewsContent(self,url):  #解析图片类的,可以都放到类构造函数中去的
        title,Hcontent,Tcontent,Acontent ="","","",""   #初始化一下
        allP = []  # 这个是装所有的段落
        simplePList = []  # 中间的段落
        downloadTool = Download(r'/home/default/images')  # 设置下载路径
        cooker = makeBS()
        soup = cooker.makesoup(url)  #soup 可能已经是空的了
        if soup==None:
            print("出现空的url ",url)
            return title,Hcontent,Tcontent,Acontent
        try :
            title = soup.find("head")    # 这个其实是head，是头部。
            # print(title)
            # time.sleep(60)
        except Exception as e:
            print(e)
            traceback.print_exc()  #这句用来告诉自己这儿需要跳出



            # print(title)
        # print("标题是")
        if title != None:  # 如果找到的话
            title = title.text.split("_")[0]
            print(title)
            # time.sleep(60)
            # title=self.fixCssdot(title)
            if self.dbhelper.ifExists(title):
                return title,Hcontent,Tcontent,Acontent  #存在的话，就不用再解析和下载图片了
            # print(title)
        else:
            print("没能找到标题，请检查网址 "+url)
            # print(soup)
            # print()
            return title, Hcontent, Tcontent, Acontent  # 不行就返回空的回去

        if url.find("photoview")!=-1:  #===============================解析图片滚动的页面的
            print("是图片集合的页面")
            # print(soup)
            for span in soup.find_all("img",attrs={"src":True}):
                print(span)
            return                               #返回空白的回去，不要这个图

        else:     #--===================================================普通的文本图文的新闻
            pass #这种是常规的新闻页面的解析
            # print(soup)

            pList=soup.find_all("p")
            checkLen = len(pList)

            for p in pList:   #解析常规的这几个东西
                # print(p)
                if p.img!=None:
                    # print("图片段落")
                    # print(p)
                    try:
                        imgSrc=p.img['src']
                        imgName = imgSrc.replace("https://inews.gtimg.com/", "").replace("/", "_")
                        now = time.strftime('%Y%m%d', time.localtime(time.time()))
                        now_date = now + "/"  # 后面下载的文件名是不需要带杠的，后面就不需要带杠杠
                        imgName = now_date + self.stripImgUrl(imgName)  # 这儿已经是添加了时间的 了

                        # print("文件名是" + imgName)                                # 这儿下载这个图片到服务器指定的地址上 # 这儿下载这个图片到服务器指定的地址上
                        downloadTool.downloadImg(imgSrc, imgName=imgName, referer=None, now_date=now)

                        imgPScr = "/images/" + imgName + ".jpg"  # 这个html格式图片地址
                        HtmlImg = '<p><img src="' + imgPScr + '"/></p>'
                        # print(HtmlImg)                                          #这个是修好的图片的文本的
                        allP.append(HtmlImg)                                   #放入列表中去

                    except Exception as e:
                        print(e)
                        print("找不到图片的地址")
                        print(p)
                        print()


                else:  #这就是普通的段落
                    if p.text!="用微信扫码二维码" and p.text!="分享至好友和朋友圈" and p.text!="" and p.text!="\n":
                        # print("普通段落")
                        if p.a==None:  #这儿开始判断是不是第一段
                            # print(p)
                            allP.append( '<p>' + p.text + '</p>' )      #只要文字进来，不要样式之类的

        # 最后再来判断首尾，这个也行的哈，对吧
        for p in allP:
            if(len(allP))>=2:
                Acontent=Acontent+str(p)
                if allP.index(p) == 0:  # 如果发现索引值是第一个的话，那就是开头了
                    Hcontent = p
                elif allP.index(p) == len(allP) - 1:  # 如果是最后一个句子，那么你就是结尾了
                    Tcontent = p
                else:  # 不是首段和尾端的端口才加入到零散的段落中去
                    simplePList.append(p)            #这儿存各种各样的列表

            else:  #如果这个也是一整段的新闻的话
                Acontent = Acontent + str(p)
                try:
                    Tcontent = "<p>" + p.split("。")[-2] + "</p>"  # 最后一句作为 结尾的句子，句号前面那个才是
                except Exception as e:
                    Tcontent = "<p>" + p.split("。")[0] + "</p>"  # 无法分的话，比如一句话，那就头尾都一样把
                Hcontent = "<p>" + p.split("。")[0] + "</p>"  # 这儿是开头的第一句的句子  ,
                simplePList.append(p)
        # print("title")
        # print(title)
        # print("Hcontent")
        # print(Hcontent)
        # print("Tcontent")
        # print(Tcontent)
        # print("Acontent")
        # print(Acontent)
        return self.fixCssdot(title), self.fixCssdot(Hcontent), self.fixCssdot(Tcontent), self.fixCssdot(Acontent)           #最后进行返回这些东西进来这儿


if __name__ == "__main__":
    url = "https://news.163.com/18/1003/08/DT691P530001875P.html"
    url = "https://news.163.com/18/1003/06/DT62OM890001875P.html"
    url = "https://news.163.com/18/1003/01/DT5I827P0001875P.html"
    url = "http://news.163.com/air/photoview/56NT0001/2296761.html"
    # url = ""
    pContent = wangyiPageContent()
    dateurl = DateUrl()
    # pContent.getPageContent( 'http://ent.163.com/18/0924/18/DSG55IQP00038FO9.html')  网易的昨天做到哪儿了
    # number10 = dateurl.getRollUrlList("2018-10-04")
    # print(len(number10))
    pContent.getNewsContent( 'https://news.163.com/19/0405/07/EBVV48JJ00018AP2.html')   #wangyi news page content here



