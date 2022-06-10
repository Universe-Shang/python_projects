import pymysql
import jieba
from wordcloud import WordCloud, wordcloud


class ConnMysql(object):
    def __init__(self):
        # 连接数据库
        self.db = pymysql.connect(host="127.0.0.1",
                                  port=3306,
                                  database="mysql",
                                  user="root",
                                  password="123456",
                                  charset='utf8')
        self.cursor = self.db.cursor()

    def select_message(self):
        datalist = []
        for name in ["housedata_dongxihu","housedata_wuchang","housedata_jianghan","housedata_hongshan"]:
            sql = 'select name from {}'.format(name)
            self.cursor.execute(sql)
            alldata = self.cursor.fetchall()
            for s in alldata:
                datalist.append(s[0])
        return datalist


my_sql = ConnMysql()
data = my_sql.select_message()
print(data)
#将数据写到文件中
with open('cloud.txt','w',encoding='utf-8') as f:
    for i in data:
        f.write(i)
    f.close()

f=open("cloud.txt","r",encoding='utf-8')
t=f.read()
for ch in ' 。，!"#$%&()*+,-./:;<=>?@[\\]^_‘{|}~abcdefghijklmnopqrstuvwxtzABCDEFGHIJKLMNOPQRSTUVWXYZ':
    t = t.replace(ch, " ")
    t = t.replace(" ","")
f.close()
ls=jieba.lcut(t)#列表
counts={}
for word in ls:
    if len(ls)==1:
        continue
    else:
        counts[word]=counts.get(word,0)+1
items=list(counts.items())
items.sort(key=lambda x:x[1],reverse=True)
p=dict(items)
w=wordcloud.WordCloud(width=1000,height=700,background_color='white',font_path="msyh.ttc")
w.generate(str(p.keys()-"dict_keys"))
w.to_file("cnwordcloud2.png")



