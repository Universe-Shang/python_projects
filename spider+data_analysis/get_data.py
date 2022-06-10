# 爬取武汉链家网房价信息
import requests
from bs4 import BeautifulSoup
import pymysql
import pymssql


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

    def create(self,location):
        # 创建数据库表
        sql = """
        create table housedata_{}(
        name varchar(60),
        price float(10),
        space varchar(10),
        area float(10),
        head varchar(5),
        price_single float(50),
        community varchar(50),
        street varchar(20),
        photo_src varchar(500)
        )
        """.format(location)
        self.cursor.execute(sql)
        self.db.commit()  # 提交操作

    def insert(self, list1,location):
        # 将数据添加到数据库中的movie表中
        sql = "insert into housedata_{} (name,price,space,area,head,price_single,community,street,photo_src) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(location)
        for li in list1:
            data = [li['简介'], li['房价'], li['厅室'], li['面积'], li['朝向'], li['每平米价格'],li['小区'],li['街道'],li['照片地址']]
            self.cursor.execute(sql, data)
        self.db.commit()  # 提交操作



def get_area(area):
    if area == 'hongshan':
        return '洪山'
    elif area == 'wuchang':
        return '武昌'
    elif area == 'dongxihu':
        return '东西湖'
    elif area == 'jianghan':
        return '江汉'
    elif area == 'huangbei':
        return '黄陂'

zone_list=['hongshan','wuchang','dongxihu','jianghan','huangbei']
for location in zone_list:
    # 对首页的页面数据进行爬取
    url = 'https://wh.lianjia.com/'
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
    }
    i = 1
    housedata_list = []
    while i < 50:
        if i == 1:
            new_url = url + "ershoufang/" + location + "/"
        else:
            new_url = url + "ershoufang/" + location + "/" + "pg" + str(i) + "/"
        # 更新到下一页
        i += 1
        page_text = requests.get(url=new_url, headers=header)
        # 在首页中解析出每个房子的url
        # 1.实例化BeautifulSoup对象，需要将页面源码数据加载到该对象中
        soup = BeautifulSoup(page_text.content, 'lxml', from_encoding='utf-8')
        soup.encoding = 'UTF-8'
        # 解析每个房子的位置，房价及型号
        li_list = soup.select('.sellListContent>li')
        # print(li_list, end=" ")
        fp = open('./ershoufang.txt', 'w', encoding='utf-8')
        for li in li_list:
            name = li.find('div', {'class': 'title'}).find('a').get_text()
            price = li.find('div', {'class': 'priceInfo'}).find('div', {'class', 'totalPrice'}).find('span').get_text()
            huxing = li.find('div', {'class': 'houseInfo'}).get_text()
            price_single = li.find('div', {'class': 'unitPrice'}).find('span').get_text()
            price_single=price_single.replace(',','')
            pos_list = li.find('div',{'class':'positionInfo'}).find_all(name = 'a')
            pos1 = pos_list[0].get_text()
            pos2 = pos_list[1].get_text()
            photo_src = li.find('img',{'class':'lj-lazy'}).get('data-original')
            # 将户型，面积，朝向，装修，楼层高低从属性里面分割出来
            hx = huxing.split()
            hx = [temp for temp in hx if temp != '|']
            houseInfo = {
                "简介": name,
                "房价":float( price.replace(',','')),
                "厅室": hx[0],
                "位置": get_area(location),
                "面积": float(hx[1].replace('平米','')),
                "朝向": hx[2],
                "每平米价格": float(price_single.replace('元/平',"")),
                '小区':pos1,
                '街道':pos2,
                '照片地址':photo_src
            }
            housedata_list.append(houseInfo)

    # 连接数据库
    my_sql = ConnMysql()
    my_sql.create(location)
    my_sql.insert(housedata_list,location)
    print(get_area(location)+"正在载入，请稍等")
print("数据加载完成！")

