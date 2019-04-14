#下载到的一个路径中去，把图片下载下来，并且把新闻里面的
import os
import time

import requests ##导入requests
# url = '//www.jb51.net/images/logo.gif'
# filename = os.path.basename(url)
# print(filename)

#这儿是python 3 的一个下载没有防止盗链的东西的一个小demo
# for page in range(1, int(max_span) + 1):  ##不知道为什么这么用的小哥儿去看看基础教程吧
# page_url = href + '/' + str(page)  ##同上

class Download:
    def __init__(self,path): #先设置好下载的路径
        self.path = path

    def downloadImg(self,img_url,imgName,referer,now_date):   #这个下载的模块是没有返回值的
        # referer = "http://www.meizitu.net/"
        headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",'Referer':referer}   ##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
        # img_url = "http://i.meizitu.net/2018/02/13d01.jpg"
        # print("下载的图片的url是"+img_url)
        # now_date = time.strftime('%Y%m%d', time.localtime(time.time()))
        try:
            img = requests.get(img_url, headers=headers)
            if(False==os.path.exists(self.path + '/'+now_date)):  #不存在这个目录的话
                os.makedirs(self.path + '/'+now_date)


        # filename = os.path.basename(img_url)
        #     print()
        #     print("图片的文件名"+self.path +"/"+imgName+'.jpg')
            f = open(self.path + '/'+imgName+'.jpg', 'ab')  ##写入多媒体文件必须要 b 这个参数！！必须要！！   这儿这里面自己带有了jpg，所以没什么问题
            f.write(img.content)  ##多媒体文件要是用conctent哦！
            f.close()
            # print("下载成功")
        except Exception as e:
            print(e)



        # print("写入成功")
if __name__=="__main__":
    imgUrl = "http://inews.gtimg.com/newsapp_match/0/5403685404/0"


# downloadTool  = Download(r'D:\pyfile\ProxySpider\newMission\images')
# downloadTool.downloadImg(img_url="http://cms-bucket.nosdn.127.net/2018/07/29/781d26ecf75c492e9604a3f531e79a58.jpeg",imgName="zhangfei",referer="http://www.meizitu.net/")