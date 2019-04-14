#coding=utf-8
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

from DBcontrol import DB

d = path.dirname(__file__)

# Read the whole text.
# text = open(path.join(d, 'test.text'),encoding='utf-8').read()

chak = DB()
allTogether = chak.getAllTitle()

import jieba


wordlist = jieba.cut(allTogether, cut_all=True)   #直接切换成了这个数据
wl = " ".join(wordlist)
print(wl)#输出分词之后的txt

coloring = np.array(Image.open(path.join(d, "test.jpg")))

# 设置停用词
# stopwords = set(STOPWORDS)
# stopwords.add("said")

# 你可以通过 mask 参数 来设置词云形状
wc = WordCloud(background_color="white",
               max_words=2000,
               # mask=coloring,
scale=32,

                max_font_size=120,
               # random_state=42,
               font_path='fangsong_GB2312.ttf')

wc.generate(wl)

# create coloring from image
image_colors = ImageColorGenerator(coloring)

# show
# 在只设置mask的情况下,你将会得到一个拥有图片形状的词云
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
# plt.savefig("result.png")
wc.to_file("result.png")

plt.figure()

plt.show()
