import json
import pprint
data1 = {'b':789,'c':456,'a':123}
data2 = {'a':123,'b':789,'c':456}
jsonString ='''[
    {
        "type": 1,
        "value": "[腾讯汽车 南阳站]编辑从南阳兴源汽车销售服务有限公司了解到，起亚KX3最高优惠1.30万元，促销时间为2019年01月17日--2019年01月18日， 欢迎有意向的朋友到店试乘试驾。"
    },
    {
        "type": 2,
        "value": "http://inews.gtimg.com/newsapp_match/0/7325291233/0"
    },
    {
        "type": 2,
        "value": "http://inews.gtimg.com/newsapp_match/0/3647613251/0"
    },
    {
        "type": 1,
        "value": "起亚KX3外观"
    },
    {
        "type": 2,
        "value": "http://inews.gtimg.com/newsapp_match/0/3647613252/0"
    },
    {
        "type": 1,
        "value": "起亚KX3内饰"
    },
    {
        "type": 2,
        "value": "http://inews.gtimg.com/newsapp_match/0/3647613253/0"
    },
    {
        "type": 1,
        "value": "起亚KX3细节"
    },
    {
        "type": 1,
        "value": "版权声明：本文系腾讯汽车独家稿件，版权为腾讯汽车所有。文章内的价格为编辑在车市第一线真实采集到的当日价格，由于汽车价格变化莫测，同时此价格只是个体经销商的行为，所以价格仅供参考使用。"
    }
]'''

d1 = json.dumps(data1,sort_keys=True)
d2 = json.dumps(data2)
d3 = json.dumps(data2,sort_keys=True)

d5=json.loads(jsonString)

# print(d5)
pprint.pprint(len(d5))   #因为列表只有一组，所以直接测出来的长度就是里面每一个的
# pprint.pprint(d5)
for i in d5:
    pprint.pprint(i)

print("test")
dic = eval("(" + jsonString + ")")  #因为加了这个才能转化成那样
pprint.pprint(dic)
print(len(dic))



