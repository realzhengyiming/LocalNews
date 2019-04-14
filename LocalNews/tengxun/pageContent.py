#coding =utf-8
# 腾讯这儿有一个滚动的新闻查看，我要爬取3333 篇文章，不知道要爬取多少天的东西啊,包括图片
#http://news.qq.com/articleList/rolls/
#腾讯新闻的,单个页面的东西放在这里了
#然后还有就是包括每篇文章中的图片下载的，每个段落中的，py3的图片下载的东西，下载到某个地方，然后再存起来
#这一页负责本地化一个页面
import json
import time
import traceback

from DBcontrol import DB
from downloadPic import Download  #这些就是导入的类啊
from makebeautifulSoup import makeBS
from bs4 import BeautifulSoup
import pprint


class pageContent:
    def __init__(self):
        self.dbhelper = DB()
    def stripImgUrl(self,replacedSrc):
        if(replacedSrc.find(":")!=-1):
            replacedSrc = replacedSrc.replace(":","")
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


    # def getPageContent(self,url): #输入一个url获得这个页面的本地化后的文章，  这个好像是没有保存东西进来这里面
    #     # time.sleep(1)
    #
    #     t = time.time()
    #     Acontent = ""
    #     Hcontent,Tcontent = "",""
    #     timeStamp =str(int(round(t * 1000)))  # 毫秒级时间戳
    #
    #     dbhelper = DB()
    #     simpleP = []
    #
    #     soup =makeBS().makesoup(url)
    #     if soup==None:
    #         title ="这个网页打开超时了"
    #         return  title, Hcontent, Tcontent, Acontent
    #     # print(soup.prettify())
    #     title = soup.find("h1")
    #     if(title!=None):
    #         title = title.text
    #     # print("标题 ",title)  #找不到标题的话说明是
    #     # if (title.find(":")!=-1):
    #     #     title  = title.replace(":","")
    #     downloadTool = Download(r'/home/default/images') #设置下载路径
    #
    #     totalLong = 0
    #     mainDiv =  soup.find("div",attrs={"class":"qq_innerMain clearfix"})
    #     # print(mainDiv)
    #     if(mainDiv==None):
    #         dbhelper.deleteUrl(url)  #如果无法找到标题，那么就是图文新闻，舍弃因为文字太少，不要了
    #         title = "腾讯没找到标题"  #直接就全部置空，当作没访问过这个就可以了
    #         print("错误，此网页是图文网页 "+url)
    #         return title, Hcontent, Tcontent, Acontent
    #     allcontent = mainDiv.find_all("p")
    #     # print(allcontent)
    #     for i in range(len(allcontent)):  #这里面这个是p
    #         # print(i)
    #         if(i==0):
    #             Hcontent =allcontent[i]
    #         localImgList = allcontent[i].find_all("img",attrs={"src":True}) #每个p标签内的img提取和修改链接本地化
    #         if(localImgList!=None):  #找到有的话就遍历
    #             for img in localImgList:
    #                 if img!=None:
    #                     # print(img['src'])
    #                     if(img['src'].find("//")==0):  #什么都没有，协议路径改成https
    #                         imgSrc  = "https:"+img['src']
    #                         # filename = os.path.basename(imgSrc)
    #                         # print(imgSrc)
    #                         imgName = imgSrc.replace("https://inews.gtimg.com/","").replace("/","_")
    #
    #                         now = time.strftime('%Y%m%d', time.localtime(time.time()))
    #                         now_date = now+"/"   #后面下载的文件名是不需要带杠的，后面就不需要带杠杠
    #                         imgName = now_date+self.stripImgUrl(imgName)
    #
    #                         # print("文件名是 " + imgName)
    #                         #这儿这个是图片的格式
    #                         newImgName = downloadTool.downloadImg(imgSrc,imgName=imgName,referer=None, now_date=now)  #下载这个是没问题的
    #                         img['src']="/images/"+imgName+".jpg"  #以这个文件名下载，以这个文件名src
    #                         # print(img['src'])
    #                         # print("图片的链接有"+imgSrc)
    #                         # print(allcontent[i])
    #                         simpleP.append(allcontent[i])
    #                         Acontent += str(allcontent[i])
    #                     elif(img['src'].find("https:")==0):   #本来就有找到有https协议,   3选1 而不是反复操作
    #                         imgSrc = img['src']
    #                         # filename = os.path.basename(imgSrc)
    #                         # print(imgSrc)
    #                         imgName = imgSrc.replace("https://inews.gtimg.com/", "").replace("/", "_")
    #
    #                         now = time.strftime('%Y%m%d', time.localtime(time.time()))
    #                         now_date = now+"/"   #后面下载的文件名是不需要带杠的，后面就不需要带杠杠
    #                         imgName = now_date+self.stripImgUrl(imgName)
    #
    #                         print("文件名是" + imgName)
    #                         downloadTool.downloadImg(imgSrc, imgName=imgName, referer=None, now_date=now)
    #                         img['src'] = "/images/" + imgSrc.replace("https://inews.gtimg.com/", "").replace("/","_") + ".jpg"
    #                         # print(img['src'])
    #                         # print("图片的链接有"+imgSrc)
    #                         # print(allcontent[i])
    #                         simpleP.append(allcontent[i])
    #                         Acontent += str(allcontent[i])
    #                     else:   #那这个就是http协议了
    #                         imgSrc = img['src']
    #                         # filename = os.path.basename(imgSrc)
    #                         # print(imgSrc)
    #                         imgName = imgSrc.replace("http://inews.gtimg.com/", "").replace("/", "_")
    #
    #
    #                         now = time.strftime('%Y%m%d', time.localtime(time.time()))
    #                         now_date = now+"/"   #后面下载的文件名是不需要带杠的，后面就不需要带杠杠
    #                         imgName = now_date+self.stripImgUrl(imgName)
    #
    #                         # print("文件名是" + imgName)
    #                         downloadTool.downloadImg(imgSrc, imgName=imgName, referer=None, now_date=now)
    #                         img['src'] = "/images/" + imgSrc.replace("http://inews.gtimg.com/", "").replace("/","_") + ".jpg"
    #                         # print(img['src'])
    #                         # print("图片的链接有"+imgSrc)
    #                         # print(allcontent[i])
    #                         simpleP.append(allcontent[i])
    #                         Acontent += str(allcontent[i])
    #
    #
    #
    #         if (allcontent[i].string=="更多新闻" or allcontent[i].string =="扫一扫，用手机看新闻！"):
    #             Tcontent =allcontent[i-1]
    #             break
    #         else:
    #             Tcontent = allcontent[-1 ]  #要么是倒数第一位要么是截断的那一位
    #         if (allcontent[i].string!=None and allcontent[i].string!="扫一扫，用手机看新闻！"):
    #             # print(allcontent[i])
    #             Acontent += str(allcontent[i])
    #             simpleP.append(allcontent[i])
    #             totalLong = len(allcontent[i].string) + totalLong
    #
    #     # for p in simpleP:
    #     #
    #     #     dbhelper.insertSimpleP(p)  #插入段落，但是没有更新标题还有那些东西，发现没有，对啊，这个东西要修改好，这儿转移出去处理把，逻辑分明一点而
    #
    #
    #     print("此文章总共多少个字"+str(totalLong))
    #     return title,Hcontent,Tcontent,Acontent
    #
    # #——————————————下面开始是全新的使用转化成wx 手机端页面的爬取，和前面的区别开来---------------------------前面的没有用对吧。



    def findVideo(self,dic):    #传入解析到一半的
        if dic.find("ext_data: ")!=-1:  #有视频的时候才来解析这个东西
            try:
                if dic.find("vid")!=-1:     #找到这个字段
                # dic = dic.replace('"',"'").replace(",","")
                    dic = dic.split("ext_data: ")[1].split("fisoriginal")[0]
                    vid = dic.split("vid")[1].split(",")[0]
                    vid  = vid.split('"')[2]
                    # print(vid)
                    return vid
            except Exception as e:
                print(e)
                return
            return dic
        else:
            return





    def fixUrl(self,url):
        url = url.replace("////","//")
        # print(url)
        return url

    def changeNewToWx(self,url):  #把链接转化成手机端的，微信的，然后返回合成的微信的链接，或者直接通过请求头来自动跳到手机端
        #提取到的两杠的要换成一杠才可以的。
        # print(url)
        if url.find("////")!=-1:
            url = self.fixUrl (url)
            # print(url)
        rawWxUrl = "https://xw.qq.com/"

        if url.find("qq.com/")!=-1:
            splitUrl = url.split(".qq.com/")
            tailUrl = splitUrl[1].replace(".htm","")
            headUrl = splitUrl[0]           #为了提取出主题theme

            if headUrl.find("//")!=-1:   #提取主题
                theme=headUrl.split("//")[1]
                tailUrl = tailUrl.split("//")[0]+"/"+theme+"/"+tailUrl.split("//")[1]+tailUrl.split("//")[2]
            else:
                return                                                                 #如果不是的话，那就返回空值把
            # print("转化后url为 -"+rawWxUrl+tailUrl)
            sumUrl = rawWxUrl+tailUrl
            # print(sumUrl)
            # print(rawWxUrl)
            # print(tailUrl)
            #为了让这个不影响之前的，那就先检查一下第二个位置是否为“//”是的话就改成/就可以了

            if len(sumUrl.split("//"))>1: #为1就没问题
                tempUrl = sumUrl.split("//")
                totalUrl = tempUrl[0]+"//"+ "/".join(tempUrl[1:])
                # print(totalUrl)
                return(totalUrl)


            # tempWxUrl = rawWxUrl + tailUrl
            # print(tempWxUrl)

            return sumUrl

    def getWxContentNew(self,url):
        wxUrl = self.changeNewToWx(url)
        Cooker = makeBS()
        title, Hcontent, Tcontent, Acontent = "", "", "", ""  # 最后一个参数好像没什么用
        downloadTool = Download(r'/home/default/images')  # 设置下载路径
        BS = Cooker.makesoup(wxUrl) #传进来是微信的才可以一


    def getWxContent(self,wxUrl):#  先提取出里面的那个，然后再看看什么情况  ----这个是主要解析的函数
        time.sleep(1)

        title, Hcontent, Tcontent, Acontent = "", "", "", ""  # 最后一个参数好像没什么用
        downloadTool = Download(r'/home/default/images')  # 设置下载路径
        simplePList = []

        Cooker = makeBS()
        BS = Cooker.makesoup(wxUrl) #传进来是微信的才可以一
        # print(BS)
        if BS==None:
            return title, Hcontent, Tcontent, Acontent
        # print(BS)
        try:
            title = BS.find("head").title    #直接选用head这儿的title标签里面的东西
        except Exception as e:
            print(e)
            traceback.print_exc()  # 貌似这个，一个错，各个错。
            return title, Hcontent, Tcontent, Acontent

        # print("输出title")

        #todo 这儿插入一个检查一下标题是否存在的东西的

        # print(title.text)                 #todo 改变成手机的ua，让服务器发来手机端页面来给我, 我怀疑现在ua打开的还是电脑版本的
        if(title!=None and title.text!="404 - 腾讯网"):
            title=title.text
            if self.dbhelper.ifExists(title):  #如果标题为空那就直接删除这条了。 ，所以就是因为已经存在，所以后面都不进行读取了对吧
                print("已经存在了这个")
               #这儿也是返回空值的。
                return title,Hcontent,Tcontent,Acontent  #存在的话，就不用再解析和下载图片了  ,如果只有标题没有别的，很可能是这个新闻标题已经存在
        else:
            print("此新闻可能已经被删除，提取失败")
            return title,Hcontent,Tcontent,Acontent

        dicString = ""
        '''
        测试区域
        '''
        print(BS)

        for script in BS.find_all("script", attrs={"async": False}):  # 这边应该找内容不为空的
            if script.text!=None and script.text!="":
                print(script.text)
                dicString = script.text
                break



        # dicString = BS.find("script", attrs={"async": False}).text  #这边应该找内容不为空的
        # print(dicString)
        print(dicString)
        dic = dicString.replace("var globalConfig =", "").replace(";", "")
        # print(dic)
        tempDic = dic
        print("解析的文章的部分-》")  # 这边已经是空的了//todo 把腾讯的这个分析的东西再搞一下，应该还是解析页面里面除到问题就是这个文件里面的。
        print(tempDic)
        if dic.find("contents: ") != -1:

            datalist = dic.split("contents: ")[1].split("ext_data")[0].replace("[", "").replace("],", "")
            # print("这边开始这样")
            #这个是新加的。
            print(datalist)

            try:
                dic = eval("(" + datalist + ")")  #因为加了这个才能转化成那样,这个应该也是没问题才对。
                # print(dic)
            except Exception as e:
                print("转化成json出错")
                print(e)
                traceback.print_exc()  # 貌似这个，一个错，各个错。
                return title,Hcontent,Tcontent,Acontent  #存在的话，就不用再解析和下载图片了

                #return #返回空内容给他们咯，自动舍弃这个东西，然后那边要处理了一下，空内容的情况，这个不对啊。
            checkLen = len(dic)
            pprint.pprint(dic)
            print(checkLen)  #这儿需要考虑只有一个句子的情况，这个情况下是长度为2，这个情况下不是列表了，只是一个字典
            if(checkLen>2):
                for p in dic:   #遍历每一个，然后尽心判断应该也是没问题才对的。
                    try:  #traceback.print_exc()
                        if p['type'] == 1:  # 这个是一个句子，那就直接插进去就可以了
                            # 当成句子插入

                            pContent = p['value']
                            phtml='<p>'+pContent+"</p>"

                            Acontent =Acontent+phtml

                            if dic.index(p)==0:                      #如果发现索引值是第一个的话，那就是开头了
                                Hcontent= phtml
                                # print("find the header p")
                                # print(phtml)
                            elif dic.index(p)==checkLen-1 :            #同理如果是最后一个句子，那么你就是结尾了
                                Tcontent = phtml
                            else:  # 不是首段和尾端的端口才加入到零散的段落中去
                                simplePList.append(phtml)



                        # print(phtml)
                        if p['type'] == 2:
                            imgSrc = p['value'].replace("\/", "/")                    #图片的真实下载地址
                            # print(imgSrc)
                            imgName = imgSrc.replace("https://inews.gtimg.com/", "").replace("/", "_")
                            now = time.strftime('%Y%m%d', time.localtime(time.time()))
                            now_date = now + "/"  # 后面下载的文件名是不需要带杠的，后面就不需要带杠杠
                            imgName = now_date + self.stripImgUrl(imgName)   #这儿已经是添加了时间的 了

                            # print("文件名是" + imgName)                                # 这儿下载这个图片到服务器指定的地址上 # 这儿下载这个图片到服务器指定的地址上
                            downloadTool.downloadImg(imgSrc, imgName=imgName, referer=None, now_date=now)

                            # now_date = now + "/"                                     # 后面下载的文件名是不需要带杠的，后面就不需要带杠杠
                            # imgName = now_date + self.stripImgUrl(imgName)   #已经处理好了
                            imgPScr = "/images/" + imgName + ".jpg"                 # 这个html格式图片地址
                            HtmlImg = '<p><img src="'+imgPScr+'"/></p>'

                            # print(imgPScr)

                            Acontent = Acontent + HtmlImg
                            # print("这个是图片了 "+HtmlImg)

                            if dic.index(p)==0:                      #如果发现索引值是第一个的话，那就是开头了
                                # print("find the header p")
                                # print(HtmlImg)
                                Hcontent= HtmlImg
                            elif dic.index(p)==checkLen-1 :            #如果是最后一个句子，那么你就是结尾了
                                Tcontent = HtmlImg
                            else:  # 不是首段和尾端的端口才加入到零散的段落中去
                                simplePList.append(HtmlImg)

                        if p['type'] == 3:  # 这个是视频的情况，直接提取出来当成句子好了，这儿还有图片的，先不管了
                            try:
                                pContent = p['value']['desc']
                                pContent = "<p>"+ pContent+"</p>"
                                # 解析视频
                                vid = self.findVideo(tempDic)
                                rawVideoString = ""
                                if vid != None:
                                    rawVideoString = '<p><iframe frameborder="0" src="https://v.qq.com/txp/iframe/player.html?vid=' + vid + '" allowFullScreen="true"></iframe></p>'

                                if dic.index(p) == 0:  # 如果发现索引值是第一个的话，那就是开头了
                                    # print("find the header p")
                                    # print(pContent)
                                    Hcontent = pContent+rawVideoString
                                elif dic.index(p) == checkLen - 1:  # 如果是最后一个句子，那么你就是结尾了
                                    Tcontent =pContent+rawVideoString
                                else:                              #不是首段和尾端的端口才加入到零散的段落中去
                                    simplePList.append(pContent)

                            except Exception as e:
                                pass  #舍弃这个段落
                    except Exception as e:
                        print(e)
                        traceback.print_exc()   #貌似这个，一个错，各个错。
                #插入数据库先
                # for p in simplePList:
                #     self.dbhelper.insertSimpleP(p)  #插入段落，但是没有更新标题还有那些东西

                Tcontent = "".join(BeautifulSoup(Acontent, 'lxml').text)
                return title, Hcontent, Tcontent, Acontent

            else :                                                         #这儿是只有一个句子的网页的情况下  ，这边的一个大段落的，首段尾段的拆分是没问题的
                p= dic                                                    #这样转换一下就可以了
                # print(type(dic))
                # print(dic)
                # print(p)
                if type(p)==tuple:
                    print("是tuple")
                    try:
                        # print("长度是")
                        # print(len(p))
                        if(len(p)==1):         #又加了一种，怕不够长的处理
                            p=p[0] # 如果是里面只有一个的话，那就提取出里面的一个元素就可以了，
                        if(len(p)==2):
                            p=p[1] # 如果是里面只有一个的话，那就提取出里面的一个元素就可以了，
                        else:                           #长度为空，里面除了标题，连文字内容都没有的这种。。。
                            p={'type':3}                     #开头结尾都是自己了，标题就也当成是这个来处理了

                    except Exception as e:
                        print(e)           #https://xw.qq.com/a/house/20180928003713  对付这个网页的情况
                        title,Hcontent,Tcontent,Acontent="","","",""   #这样就可以拉
                        return  title, Hcontent, Tcontent, Acontent#直接不要这个url的内容了

                # print(p)
                if p['type'] == 1:                                       # 这个是一个句子，那就直接插进去就可以了
                    # 当成句子插入
                    pContent = p['value']                                   #提取出句子来作为首段尾端还有   中间的段落
                    # print("长度有")
                    # print(pContent.split("。"))
                    # print(len(pContent.split("。")))
                    try:
                        Tcontent = "<p>"+pContent.split("。")[-2] +"</p>"           #最后一句作为 结尾的句子，句号前面那个才是
                    except Exception as e:
                        Tcontent="<p>"+pContent.split("。")[0] +"</p>"   #无法分的话，比如一句话，那就头尾都一样把
                    Hcontent = "<p>"+pContent.split("。")[0] +"</p>"            #这儿是开头的第一句的句子  ,
                    simplePList.append(pContent)                                 #整个把，没办法了饿

                    phtml = '<p>' + pContent + "</p>"
                    Acontent = Acontent + phtml
                    # print(phtml)

                if p['type'] == 2:
                    imgSrc = p['value'].replace("\/", "/")  # 图片的真实下载地址
                    # print(imgSrc)
                    imgName = imgSrc.replace("https://inews.gtimg.com/", "").replace("/", "_")
                    now = time.strftime('%Y%m%d', time.localtime(time.time()))
                    now_date = now + "/"  # 后面下载的文件名是不需要带杠的，后面就不需要带杠杠
                    imgName = now_date + self.stripImgUrl(imgName)

                    # print("文件名是" + imgName)  # 这儿下载这个图片到服务器指定的地址上 # 这儿下载这个图片到服务器指定的地址上
                    downloadTool.downloadImg(imgSrc, imgName=imgName, referer=None, now_date=now)


                    # now_date = now + "/"  # 后面下载的文件名是不需要带杠的，后面就不需要带杠杠
                    # imgName = now_date + self.stripImgUrl(imgName)
                    imgPScr = "/images/" + imgName + ".jpg"  # 这个html格式图片地址

                    # print(imgPScr)
                    HtmlImg = '<p><img src="' + imgPScr + '"/></p>'
                    Acontent = Acontent + HtmlImg
                    # print("这个是图片了 " + HtmlImg)

                if p['type'] == 3  :                  #只有一个视频的时候，解析视频
                    pContent = title
                    # print(pContent)

                    #解析视频
                    vid = self.findVideo(tempDic)
                    rawVideoString =""
                    if vid!=None:
                        rawVideoString='<p><iframe frameborder="0" src="https://v.qq.com/txp/iframe/player.html?vid='+vid+'" allowFullScreen="true"></iframe></p>'


                    #只有一个句子的东西是没有这个索引值的
                    # if dic.index(p) == 0:  # 这种情况就是只有一个视频的网页，标题就是唯一的开头了，那结尾呢，已经不能分了把，视频又没找到
                    #     print("find the header p")
                    #     print(pContent)
                    Hcontent = pContent                  #头是描述
                    Tcontent = rawVideoString            #尾是视频作为一个独立的一个段落
                #插入数据库先
                for p in simplePList:
                    self.dbhelper.insertSimpleP(p)  #插入段落，但是没有更新标题还有那些东西
                Tcontent = "".join(BeautifulSoup(Acontent, 'lxml').text)
                return title, Hcontent, Tcontent, Acontent                  #返回了后就可以写入数据库了把
            # else:   #这儿是真的只有一个句子的时候
            #     pass



    def getPageContentMain(self,sportsUrl):
        print(sportsUrl)

        title, Hcontent, Tcontent, Acontent = self.getWxContent(self.changeNewToWx(sportsUrl))  #直接打开手机端的getWxContent这儿

        print(title)
        # print(Hcontent)
        # print(Tcontent)
        # print(Acontent)
        return title, Hcontent, Tcontent, Acontent





if __name__ == "__main__":  #这个就是url的东西,再统一化后，就确实和框架差不多，只有爬取部分需要自自定义
    '''
    http:////tech.qq.com//a//20190103//007134.htm

    4
    Traceback (most recent call last):
      File "/root/newsSpider/tengxun/everyDayTengxun.py", line 88, in <module>
        everydayTengxun.getEveryTengxun()
      File "/root/newsSpider/tengxun/everyDayTengxun.py", line 61, in getEveryTengxun
        title, Hcontent, Tcontent, Acontent=pcontent.getPageContentMain(url)  #这儿漏了更新到url中去  ,自动转换成xw的然后再下载
      File "/root/newsSpider/tengxun/pageContent.py", line 454, in getPageContentMain
        title, Hcontent, Tcontent, Acontent = self.getWxContent(self.changeNewToWx(sportsUrl))  #直接打开手机端的getWxContent这儿
      File "/root/newsSpider/tengxun/pageContent.py", line 285, in getWxContent
        if p['type'] == 1:  # 这个是一个句子，那就直接插进去就可以了
    TypeError: string indices must be integers
    '''

    url = "https://news.qq.com/a/20180728/004261.htm"
    # url = "https://new.qq.com/omn/20180727/20180727A08F6Q.html"
    # url = "http://news.ifeng.com/a/20180806/59649785_0.shtml"
    # url = "https://news.qq.com/a/20180728/004261.htm"
    # url = "https://news.qq.com/a/20180728/000193.htm"

    tengxun = pageContent()
    url = "https://news.qq.com/a/20180813/039248.htm"
    url = "http:////news.qq.com//a//20180925//000977.htm"  #这儿是时政新闻
    url = "http:////news.qq.com//a//20180925//012219.htm"  #这儿是军事
    url = "http:////ent.qq.com//a//20180925//006046.htm"  # 娱乐 ,还是可以打开，不过好慢的样子，不知道为什么
    url = "http://sports.qq.com/a/20180925/013599.htm"
    # url = "http://"+url.split("////")[1]
    # print(tengxun.fixUrl(url))   #切片是 前面开始保留的位置，后面截至的位置


    # tengxun.getPageContent(url)
    techUrl ="http:////tech.qq.com//a//20180926//001314.htm"  #没问题
    autoUrl ="http:////auto.qq.com//a//20180926//006083.htm"  #没问题
    urlHouse = "http:////house.qq.com//a//20180926//003084.htm"  #没为题
    newUrl = "http:////news.qq.com//a//20180926//000103.htm"  #没问题
    entUrl = "http:////ent.qq.com//a//20180926//000382.htm"   #没问题
    financeUrl="http:////finance.qq.com//a//20180926//001564.htm"   #没问题
    sportsUrl = "http:////sports.qq.com//a//20180926//011501.htm"  #没问题

    urlAuto = "https://xw.qq.com/a/auto/20180929004261"







    #这儿开始测试新的代码
    urlResult = tengxun.changeNewToWx("https://house.qq.com//a//20190315//006126.htm")   #一个视频的页面，还是有问题哈 https://news.qq.com//a//20181004//007938.htm
    print(urlResult)
    # print(tengxun.getWxContent(urlResult))
    title, Hcontent, Tcontent, Acontent =tengxun.getWxContent(urlResult)  #这个的首段是带视频的，这种什么情况
    print()
    print("标题是")
    print(title)
    print("首段是")
    print(Hcontent)
    print("尾段落是")
    print(Tcontent)

    print("全文的内容是：")
    print(Acontent)
    # print("中间段落是")
    # print(simplePlists)

    # print("全文是")
    # print(Acontent)
    # tengxun.getSportContent(url)
    #------------------------------------这儿下面时测试获取手机页面的





# check = '''ext_data:  {"cnt_attr":{"VIDEO_0":{"vid":"i0553q2yo4f","pic":"http:\/\/inews.gtimg.com\/newsapp_ls\/0\/2887621823_640480\/0","desc":"\u89c6\u9891\uff1a2018\u6625\u8282\u8857\u91c7\u65b0\u65f6\u4ee3\u7684\u5e78\u798f\u751f\u6d3b \u8001\u4eba\u79f0\u73b0\u5728\u6bcf\u5929\u90fd\u662f\u8fc7\u6625\u8282\uff0c\u65f6\u957f\u7ea62\u52063\u79d2"}},"cnt_html":"<!--VIDEO_0-->","htmlIntro":"","cnt_flag":1,"abstract_pad":"","media_id":null,"politicalOption":""},
# '''
# print(tengxun.findVideo(check))





# '<iframe frameborder="0" src="https://v.qq.com/txp/iframe/player.html?vid=q0025s3rrvm" allowFullScreen="true"></iframe>'
# '<embed src="https://imgcache.qq.com/tencentvideo_v1/playerv3/TPout.swf?max_age=86400&v=20161117&vid=q0025s3rrvm&auto=0" allowFullScreen="true" quality="high" width="480" height="400" align="middle" allowScriptAccess="always" type="application/x-shockwave-flash"></embed>'