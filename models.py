# !/usr/bin/env python
# _*_ coding: utf-8 _*_

import flask
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy import or_,and_



app = flask.Flask(__name__)

class Config(object):
    """配置参数"""
    # 设置连接数据库的URL
    user = 'root'
    password = '123456'
    database = 'lvyoukeshihua'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%s:%s@127.0.0.1:3306/%s' % (user, password, database)

    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查询时会显示原始SQL语句
    app.config['SQLALCHEMY_ECHO'] = False

    # 禁止自动提交数据处理
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False


# 读取配置
app.config.from_object(Config)

# 创建数据库sqlalchemy工具对象
db = SQLAlchemy(app)


class User(db.Model):
    # 定义表名
    __tablename__ = 'users'
    # 定义字段
    name_id = db.Column(db.Integer, unique=True, primary_key=True,autoincrement=True)
    name = db.Column(db.String(32),name='用户名')
    email = db.Column(db.String(32),name='邮箱')
    password = db.Column(db.String(32),name='密码')
    itype = db.Column(db.String(32),default='vip',name='权限')
    user_datetime = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now)

    def __repr__(self):
        return "<{}账号>".format(self.email)




class Case_item(db.Model):
    __tablename__ = 'case_item'

    case_id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)

    name = db.Column(db.String(32),name='景区名')
    price = db.Column(db.Float,default=0,name='价格')
    pingfen = db.Column(db.Float,default=0,name='评分')
    xiaoliang = db.Column(db.Float,default=0,name='销量')
    xingji = db.Column(db.String(32),default=0,name='星级')
    shengfen = db.Column(db.String(32),name='地区')
    dizi = db.Column(db.String(520),default='',name='地址')
    text = db.Column(db.String(1240),default='',name='介绍')
    jingdian = db.Column(db.String(520),default='',name='景点')

    case_datetime = db.Column(db.DateTime(), nullable=True, default=datetime.datetime.now)


    def __repr__(self):
        return "<{}景区>".format(self.name)











import base64

if __name__ == '__main__':
    pass
    # db.drop_all()
    # db.create_all()
    # db.session.add(User(name='admin',email='admin@qq.com',password='root123456',itype='admin'))
    # db.session.commit()

    # db.session.add(DiQu(name='广州', text='''传说广州最早的地名为“楚庭”（或“楚亭”）。越秀山上的中山纪念碑下，尚有清人所建一座石牌坊，上面刻着“古之楚亭”四字。不少史籍将“楚庭”视为广州的雏型，是广州最早的称谓，距今已有2847年。传说有五位仙人，身穿五彩衣，骑着五色羊，拿着一茎六穗的优良稻谷种子，降临“楚庭”，将稻穗赠给当地人民，并祝福这里永无饥荒。说完后，五位仙人便腾空而去，五只羊则变成了石头。当地人民为纪念五位仙人，修建了一座五仙观，传说五仙观即为“楚庭”所在。由此，广州又有“羊城”、“穗城”的别名。''',
    #                          image=open('1.jpg','rb').read()))
    # db.session.commit()


    # db.session.add(Case_item(diqu_id=1,name='广州塔', xingji=4,text='''广州塔（英语：Canton Tower）又称广州新电视塔，昵称小蛮腰，其位于中国广东省广州市海珠区（艺洲岛）赤岗塔附近，距离珠江南岸125米，与珠江新城、花城广场、海心沙岛隔江相望。广州塔塔身主体高454米，天线桅杆高146米，总高度600米 [1-2]  。是中国第二高塔，仅次于上海中心大厦 [3]  ，是国家AAAA级旅游景区。''',
    #                          itype='建筑',image=open('2.jpg','rb').read()))
    # db.session.commit()


    # a = Case_item.query.get_or_404(1)
    # print(base64.b64encode(a.image))
    # print()
    # print(User.query.filter(and_(User.email=='admin',User.password=='root123456')).all()[0].name_id)

    # print(User.query.get('1'))

