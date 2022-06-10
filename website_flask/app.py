from flask import Flask, render_template, request, flash, redirect
import pymysql
# 导入wtf扩展的表单类
from flask_wtf import FlaskForm, form
# 导入自定义表单需要的字段
from wtforms import SubmitField, StringField, PasswordField
# 导入wtf扩展提供的表单验证器
from wtforms.validators import DataRequired, EqualTo, Length

app = Flask(__name__)
app.secret_key = 'sxz'
# 给模板传递一个消息用
# flash-->需要对一个内容进行加密，因此需要设置secret_key,做一个加密消息的混淆
# 模板中需要遍历消息

is_login = False
user_list = []


# 创建数据库来存储登录信息
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

    def create(self):
        # 创建数据库表
        sql = """
        create table userInfo(
        id varchar(10) primary key,
        passwd varchar(10) not null
        )
        """
        self.cursor.execute(sql)
        self.db.commit()  # 提交操作

    def insert(self, list1):
        # 将数据添加到数据库中的movie表中
        sql = "insert into userInfo (id,passwd) values(%s,%s)"
        for li in list1:
            data = [li['id'], li['passwd']]
            self.cursor.execute(sql, data)
        self.db.commit()  # 提交操作

    def select_user(self, id):
        sql = """
        select passwd from userinfo
        where id = '{}'
        """.format(id)
        cur = self.db.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql)
        result = cur.fetchone()
        return result

    def select_house_text(self, info):
        # 当“%s”前后有“%”的时候，想要将其当做“%”的字符使用，需要用“%%”表示
        house_street = ["housedata_dongxihu",'housedata_hongshan','housedata_huangbei','housedata_jianghan','housedata_wuchang']
        house_list = []
        for name in house_street:
            sql = """
            select  distinct * from {}
            where name like %s 
            """.format(name)
            house_list = []
            cur = self.db.cursor(pymysql.cursors.DictCursor)
            # 通过字典向sql语句中传递参数
            # response1中存储的是数据的个数,response2中存储的是数据的信息
            response1 = cur.execute(sql, '%{}%'.format(info))
            response2 = cur.fetchall()
            for response in response2:
                house_list.append(response)
            return house_list


"""
使用WTF实现表单
需要自定义一个表单类
"""


@app.route('/', methods=['GET', 'POST'])
def login():
    # 1.判断请求方式
    if request.method == 'POST':
        # 2.获取请求的参数
        username = request.form.get('username')
        passwd = request.form.get('password')

        # 3.验证参数是否相同
        if not all([username, passwd]):
            # 加u解决编码问题
            flash(u'密码不正确')
        else:
            if my_sql.select_user(username) is None:
                flash(u'密码不正确')
            else:
                password = my_sql.select_user(username)['passwd']
                if passwd != password:
                    flash(u'密码不正确')
                else:
                    global is_login
                    is_login = True
                    return redirect('/main_page')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # 1.判断请求方式
    if request.method == 'POST':
        # 2.获取请求的参数
        username = request.form.get('username')
        passwd = request.form.get('password1')
        passwd2 = request.form.get('password2')

        # 3.验证参数是否相同
        if not all([username, passwd, passwd2]):
            # 加u解决编码问题
            flash(u"消息不完整")
        elif passwd != passwd2:
            flash(u"密码不一致！")
        elif len(passwd) < 6:
            flash(u'密码小于六位！')
        else:
            mes = {
                'id': username,
                'passwd': passwd
            }
            user_list.append(mes)
            my_sql.insert(user_list)
            return render_template('login.html')
    return render_template('register.html')


@app.route('/main_page', methods=['GET', 'POST'])
def main_page():
    if is_login:
        return render_template('main_page.html')
    else:
        return '请先登录！'


@app.route('/search', methods=['POST', 'GET'])
def search():
    global product, name
    name = request.form.get('info')
    if is_login:
        # 根据用户的输入来筛选条件
        # 1.判断请求方式

        # 2.获取请求的参数
        if name is None:
            product = [{
                'name': '',
                'price': '',
                'space': '',
                'area': '',
                'head': '',
                'community': '',
                'street': '',
                'photo_src': ''
            }]
            kwargs = {
                "products": product
            }
            return render_template('search.html', **kwargs)
        else:
            product = my_sql.select_house_text(name)
            kwargs = {
                "products": product
            }
            print(kwargs)
            return render_template('search.html', **kwargs)


# 目的：实现一个简单的登录逻辑处理
# 1.路由需要有get和post两种请求方式 --》需要判断请求方式
# 2.获取请求的参数
# 3.判断参数填写和密码是否相同
# 4.如果判断都没有问题，就返回一个success

my_sql = ConnMysql()
app.run()
