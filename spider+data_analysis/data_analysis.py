import matplotlib.pyplot as plt
import pandas as pd
import pymysql
import numpy as np
import matplotlib
# 绘制雷达图
import pygal

# 显示中文
font = {'family': 'MicroSoft Yahei',
        'weight': 'bold'}
matplotlib.rc("font", **font)


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

    def select_message1(self):
        datalist = []
        for name in ["housedata_dongxihu", "housedata_wuchang", "housedata_jianghan", "housedata_hongshan",
                     "housedata_huangbei"]:
            sql = 'select MAX(price) from {}'.format(name)
            cur = self.db.cursor(pymysql.cursors.DictCursor)
            cur.execute(sql)
            alldata = cur.fetchone()
            print(alldata)
            mes = {
                'name': name,
                'price': alldata['MAX(price)']
            }
            datalist.append(mes)
        return datalist

    def select_message2(self):
        datalist = []
        for name in ["housedata_dongxihu", "housedata_wuchang", "housedata_jianghan", "housedata_hongshan",
                     "housedata_huangbei"]:
            sql = 'select MIN(price) from {}'.format(name)
            cur = self.db.cursor(pymysql.cursors.DictCursor)
            cur.execute(sql)
            alldata = cur.fetchone()
            mes = {
                'name': name,
                'price': alldata['MIN(price)']
            }
            datalist.append(mes)
        return datalist

    # 返回平均房价
    def select_message3(self):
        datalist = []
        for name in ["housedata_dongxihu", "housedata_wuchang", "housedata_jianghan", "housedata_hongshan",
                     "housedata_huangbei"]:
            sql = 'select AVG(price) from {}'.format(name)
            cur = self.db.cursor(pymysql.cursors.DictCursor)
            cur.execute(sql)
            alldata = cur.fetchone()
            print(alldata)
            mes = {
                'name': name,
                'price': alldata['AVG(price)']
            }
            datalist.append(mes)
        return datalist

    def select_message4(self):
        # 返回房产信息记录和房价
        datalist = []
        for name in ["housedata_dongxihu", "housedata_wuchang", "housedata_jianghan", "housedata_hongshan",
                     "housedata_huangbei"]:
            sql = 'select price from {}'.format(name)
            num = self.cursor.execute(sql)
            alldata = self.cursor.fetchall()
            pricelist = []
            for s in alldata:
                pricelist.append(s[0])
            datalist.append(pricelist)
        return datalist

    def selct_area(self):
        area_list = []
        sql = 'select area from housedata_huangbei'
        num = self.cursor.execute(sql)
        alldata = self.cursor.fetchall()
        for s in alldata:
            if s[0]>270:
                continue
            area_list.append(s[0])
        return area_list

    def select_radar(self):
        # 查询洪山区均价前五的小区的信息
        datalist = []
        sql = """
        select community,AVG(price) from housedata_huangbei
        group by community
				HAVING COUNT(*) >= 10
				ORDER BY AVG(price) DESC
        """

        num = self.cursor.execute(sql)
        alldata = self.cursor.fetchall()
        print(alldata)
        return alldata[0:6]


def maxprice():
    # 绘制
    my_sql = ConnMysql()
    data = my_sql.select_message1()
    name = ['东西湖区', '武昌区', '江汉区', '洪山区', '黄陂区']
    price = [mes['price'] for mes in data]
    # 设置图形大小
    plt.figure(figsize=(20, 15), dpi=80)
    # 绘制条形图
    plt.bar(name, price, width=0.2)
    # 设置字符串到x轴
    plt.xticks(range(len(name)), name)
    plt.title("各个区的最高房价", fontsize=30)
    plt.xlabel("区名", fontsize=20)
    plt.ylabel("房价/万元", fontsize=20)

    # 在柱状图上显示数据
    for a, b, i in zip(name, price, range(len(name))):  # zip 函数
        plt.text(a, b + 0.01, "%.2f" % price[i], ha='center', fontsize=25)  # plt.text 函数
    plt.savefig(r'C:\Users\42552\PycharmProjects\flask_WTF_test\static\maxprice.jpg')
    plt.show()


def minprice():
    # 绘制
    my_sql = ConnMysql()
    data = my_sql.select_message2()
    name = ['东西湖区', '武昌区', '江汉区', '洪山区', '黄陂区']
    price = [mes['price'] for mes in data]
    # 设置图形大小
    plt.figure(figsize=(20, 15), dpi=80)
    # 绘制条形图
    plt.bar(name, price, width=0.2)
    # 设置字符串到x轴
    plt.xticks(range(len(name)), name)
    plt.title("各个区的最低房价", fontsize=30)
    plt.xlabel("区名", fontsize=60)
    plt.ylabel("房价/万元", fontsize=20)

    for a, b, i in zip(name, price, range(len(name))):  # zip 函数
        plt.text(a, b + 0.01, "%.2f" % price[i], ha='center', fontsize=25)  # plt.text 函数
    plt.savefig(r'C:\Users\42552\PycharmProjects\flask_WTF_test\static\minprice.jpg')
    plt.show()


def avgprice():
    # 绘制
    my_sql = ConnMysql()
    data = my_sql.select_message3()
    name = ['东西湖区', '武昌区', '江汉区', '洪山区', '黄陂区']
    price = [mes['price'] for mes in data]
    # 设置图形大小
    plt.figure(figsize=(20, 15), dpi=80)
    # 绘制条形图
    plt.bar(name, price, width=0.2)
    # 设置字符串到x轴
    plt.xticks(range(len(name)), name)
    plt.title("各个区的平均房价", fontsize=30)
    plt.xlabel("区名", fontsize=20)
    plt.ylabel("房价/万元", fontsize=20)

    for a, b, i in zip(name, price, range(len(name))):  # zip 函数
        plt.text(a, b + 0.01, "%.2f" % price[i], ha='center', fontsize=25)  # plt.text 函数
    plt.savefig(r'C:\Users\42552\PycharmProjects\flask_WTF_test\static\avgprice.jpg')
    plt.show()



def sandiantu1():
    # 绘制散点图来展示出每个区的房价分布
    my_sql = ConnMysql()
    data = my_sql.select_message4()
    # name = ['东西湖区', '武昌区', '江汉区', '洪山区', '黄陂区']
    data = my_sql.select_message4()
    x1 = np.array(range(1, 1471))
    # 将python标准列表转化为ndarray类型
    # 东西湖地区房价信息
    y1 = np.array(data[0])
    colors = np.array(["red", "green", "black", "orange", "purple", "beige", "cyan", "magenta"])
    plt.scatter(x1, y1, c=np.squeeze(y1))
    plt.title("东西湖区房价一览")
    plt.ylabel("房价 单位：万元")
    plt.grid(axis='y')  # 设置 x 就在轴方向显示网格线
    # 绘制最大值与最小值的点
    max_indx = np.argmax(y1)  # max value index
    plt.plot(max_indx, y1[max_indx], 'ks')
    show_max = str(y1[max_indx]) + "万元"
    plt.annotate(show_max, xytext=(max_indx, y1[max_indx]), xy=(max_indx, y1[max_indx]))
    plt.savefig(r'C:\Users\42552\PycharmProjects\flask_WTF_test\static\sandiantu1.jpg')
    plt.show()


def sandiantu2():
    # 武昌区房价展示
    # 绘制散点图来展示出每个区的房价分布
    my_sql = ConnMysql()
    data = my_sql.select_message4()
    # name = ['东西湖区', '武昌区', '江汉区', '洪山区', '黄陂区']
    data = my_sql.select_message4()
    x1 = np.array(range(1, 1471))
    # 将python标准列表转化为ndarray类型
    # 东西湖地区房价信息
    y1 = np.array(data[1])
    colors = np.array(["red", "green", "black", "orange", "purple", "beige", "cyan", "magenta"])
    plt.scatter(x1, y1, c=np.squeeze(y1))
    plt.title("武昌区房价一览")
    plt.ylabel("房价 单位：万元")
    plt.grid(axis='y')  # 设置 x 就在轴方向显示网格线
    # 绘制最大值与最小值的点
    max_indx = np.argmax(y1)  # max value index
    plt.plot(max_indx, y1[max_indx], 'ks')
    show_max = str(y1[max_indx]) + "万元"
    plt.annotate(show_max, xytext=(max_indx, y1[max_indx]), xy=(max_indx, y1[max_indx]))
    plt.savefig(r'C:\Users\42552\PycharmProjects\flask_WTF_test\static\sandiantu2.jpg')
    plt.show()


def sandiantu3():
    # 江汉区房价信息展示
    # 绘制散点图来展示出每个区的房价分布
    my_sql = ConnMysql()
    data = my_sql.select_message4()
    # name = ['东西湖区', '武昌区', '江汉区', '洪山区', '黄陂区']
    data = my_sql.select_message4()
    x1 = np.array(range(1, 1471))
    # 将python标准列表转化为ndarray类型
    # 东西湖地区房价信息
    y1 = np.array(data[2])
    colors = np.array(["red", "green", "black", "orange", "purple", "beige", "cyan", "magenta"])
    plt.scatter(x1, y1, c=np.squeeze(y1))
    plt.title("江汉区房价一览")
    plt.ylabel("房价 单位：万元")
    plt.grid(axis='y')  # 设置 x 就在轴方向显示网格线
    # 绘制最大值与最小值的点
    max_indx = np.argmax(y1)  # max value index
    plt.plot(max_indx, y1[max_indx], 'ks')
    show_max = str(y1[max_indx]) + "万元"
    plt.annotate(show_max, xytext=(max_indx, y1[max_indx]), xy=(max_indx, y1[max_indx]))
    plt.savefig(r'C:\Users\42552\PycharmProjects\flask_WTF_test\static\sandiantu3.jpg')
    plt.show()


def sandiantu4():
    # 展示洪山区房价信息
    # 绘制散点图来展示出每个区的房价分布
    my_sql = ConnMysql()
    data = my_sql.select_message4()
    # name = ['东西湖区', '武昌区', '江汉区', '洪山区', '黄陂区']
    data = my_sql.select_message4()
    x1 = np.array(range(1, 1471))
    # 将python标准列表转化为ndarray类型
    # 东西湖地区房价信息
    y1 = np.array(data[3])
    colors = np.array(["red", "green", "black", "orange", "purple", "beige", "cyan", "magenta"])
    plt.scatter(x1, y1, c=np.squeeze(y1))
    plt.title("洪山区房价一览")
    plt.ylabel("房价 单位：万元")
    plt.grid(axis='y')  # 设置 x 就在轴方向显示网格线
    # 绘制最大值与最小值的点
    max_indx = np.argmax(y1)  # max value index
    plt.plot(max_indx, y1[max_indx], 'ks')
    show_max = str(y1[max_indx]) + "万元"
    plt.annotate(show_max, xytext=(max_indx, y1[max_indx]), xy=(max_indx, y1[max_indx]))
    plt.savefig(r'C:\Users\42552\PycharmProjects\flask_WTF_test\static\sandiantu4.jpg')
    plt.show()


def sandiantu5():
    # 展示黄陂区房价信息
    # 绘制散点图来展示出每个区的房价分布
    my_sql = ConnMysql()
    data = my_sql.select_message4()
    # name = ['蔡甸区', '武昌区', '江汉区', '洪山区', '黄陂区']
    data = my_sql.select_message4()
    x1 = np.array(range(1, 1471))
    # 将python标准列表转化为ndarray类型
    # 东西湖地区房价信息
    y1 = np.array(data[4])
    colors = np.array(["red", "green", "black", "orange", "purple", "beige", "cyan", "magenta"])
    plt.scatter(x1, y1, c=np.squeeze(y1))
    plt.title("黄陂区房价一览")
    plt.ylabel("房价 单位：万元")
    plt.grid(axis='y')  # 设置 x 就在轴方向显示网格线
    # 绘制最大值与最小值的点
    max_indx = np.argmax(y1)  # max value index
    plt.plot(max_indx, y1[max_indx], 'ks')
    show_max = str(y1[max_indx]) + "万元"
    plt.annotate(show_max, xytext=(max_indx, y1[max_indx]), xy=(max_indx, y1[max_indx]))
    plt.savefig(r'C:\Users\42552\PycharmProjects\flask_WTF_test\static\sandiantu5.jpg')
    plt.show()


def create_radar():
    my_sql = ConnMysql()
    data = my_sql.select_radar()
    # 用于正常显示中文
    plt.rcParams['font.sans-serif'] = 'SimHei'
    # 用于正常显示符号
    plt.rcParams['axes.unicode_minus'] = False

    # 使用ggplot的绘图风格
    plt.style.use('ggplot')

    # 构造数据
    values1 = [int(data[0][1]), int(data[1][1]), int(data[2][1]), int(data[3][1]), int(data[4][1])]
    feature = [data[0][0], data[1][0], data[2][0], data[3][0], data[4][0]]

    # 设置每个数据点的显示位置，在雷达图上用角度表示
    angles = np.linspace(0, 2 * np.pi, len(feature), endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))
    # 绘图
    fig = plt.figure()
    for values in [values1]:
        # 拼接数据首尾，使图形中线条封闭
        values = np.concatenate((values, [values[0]]))
        # 设置为极坐标格式
        ax = fig.add_subplot(111, polar=True)
        # 绘制折线图
        ax.plot(angles, values, 'o-', linewidth=2)
        # 填充颜色
        ax.fill(angles, values, alpha=0.25)

        # 设置图标上的角度划分刻度，为每个数据点处添加标签
        ax.set_thetagrids(angles[:-1] * 180 / np.pi, feature)

        # 设置雷达图的范围
        ax.set_ylim(0, 1000)
    # 添加标题
    plt.title('黄陂区高端小区房价')
    # 添加网格线
    ax.grid(True)
    plt.savefig(r'C:\Users\42552\PycharmProjects\flask_WTF_test\static\radar_huangbei.jpg')
    plt.show()


# maxprice()
# minprice()
# avgprice()
# sandiantu1()
# sandiantu2()
# sandiantu3()
# sandiantu4()
# sandiantu5()
# create_radar()

def create_bing():
    labels = ['一室', '二室', '三室', '四室','五室及以上']  # 定义标签
    sizes = [59,366,824,156,62]  # 每一块的比例
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral','red']  # 每一块的颜色
    explode = (0, 0.01, 0.05, 0,0)  # 突出显示，这里仅仅突出显示第二块（即'Hogs'）

    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')  # 显示为圆（避免比例压缩为椭圆）
    plt.title("江汉区各房室比例")
    plt.savefig(r'C:\Users\42552\PycharmProjects\flask_WTF_test\static\bing_jianghan.jpg')
    plt.show()

def create_zhifang():
    data=my_sql.selct_area()
    plt.hist(data, bins=40, facecolor="blue", edgecolor="black", alpha=0.7,bottom=True)
    # 显示横轴标签
    plt.xlabel("面积")
    # 显示纵轴标签
    plt.ylabel("频数/频率")
    # 显示图标题
    plt.title("黄陂区面积频数/频率分布直方图")
    plt.savefig(r'C:\Users\42552\PycharmProjects\flask_WTF_test\static\zhifang_huangbei.jpg')
    plt.show()

create_zhifang()
