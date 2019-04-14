#这儿时打开外面的那个输出文件来看怎么回事的，并且把内容发到邮件去
# -*- coding:utf-8 -*-
def readfile(tfile):
    with open(tfile, 'r') as f:
        lines = f.readlines()
        return lines[-30:]


alltext = ""
someThing = readfile('/root/newsSpider/aaa.text')
print(someThing)
for text in someThing:
    alltext = alltext + text + "\n"
print(alltext)