# !/usr/bin/env python
# _*_ coding: utf-8 _*_
from flask import Flask, request, render_template,jsonify,abort,session,redirect, url_for
import os
import time
from models import *
import models
#
# app = Flask(__name__)
app.config['SECRET_KEY'] = 'kyes'

@app.route('/fenxi', methods=['GET', 'POST'])
def fenxi():
    stu_id = session.get('stu_id')
    datas = models.User.query.get(stu_id)
    if not datas:
        return redirect(url_for('login'))
    if request.method == 'GET':
        results = models.Case_item.query.all()

        datas1 = [{'name': resu.name, 'value': resu.xiaoliang} for resu in results]
        datas1.sort(key=lambda x: x['value'], reverse=True)
        names1 = []
        for da1 in datas1[:8]:
            names1.append(da1['name'])
        datas1_value = datas1[:8]

        #各省份月旅客数
        cidys = list(set([resu.shengfen for resu in results]))
        datas2 = []
        for cidy in cidys:
            value = 0
            values = models.Case_item.query.filter(models.Case_item.shengfen == cidy).all()
            for resu in values:
                value += resu.xiaoliang
            datas2.append({'name': cidy, 'value': value})
        datas2.sort(key=lambda x: x["value"], reverse=True)
        names2 = []
        for da1 in datas2:
            names2.append(da1['name'])
        datas2_value = datas2

        #景点数前十省份
        datas3 = []
        for cidy in cidys:
            values = models.Case_item.query.filter(models.Case_item.shengfen == cidy).all()
            datas3.append({'name': cidy, 'value': len(values)})
        datas3.sort(key=lambda x: x["value"], reverse=True)
        names3= []
        for da1 in datas3[:5]:
            names3.append(da1['name'])
        datas3_value = datas3[:5]
        print(datas3_value)

        #各类型景区分布
        xingjis = list(set([resu.xingji for resu in results]))
        datas4 = []
        for xingji in xingjis:
            values = models.Case_item.query.filter(models.Case_item.xingji == xingji).all()
            datas4.append({'name': xingji, 'value': len(values)})


        #各价格区间景区
        a1 = models.Case_item.query.filter(and_(models.Case_item.price >= 0, models.Case_item.price < 50)).all()
        a2 = models.Case_item.query.filter(and_(models.Case_item.price >= 50, models.Case_item.price < 100)).all()
        a3 = models.Case_item.query.filter(and_(models.Case_item.price >= 100, models.Case_item.price < 150)).all()
        a4 = models.Case_item.query.filter(and_(models.Case_item.price >= 150, models.Case_item.price < 200)).all()
        a5 = models.Case_item.query.filter(and_(models.Case_item.price >= 200)).all()
        datas5 = [len(a1),len(a2),len(a3),len(a4),len(a5)]
        names5 = ['0-50','50-100','100-150','150-200','>200']

        #地图
        datas6 = []
        for cidy in cidys:
            values = models.Case_item.query.filter(models.Case_item.shengfen == cidy).all()
            datas6.append({'name': cidy, 'value': len(values)})

        #散点图
        datas7 = [[resu.price,resu.xiaoliang,resu.name] for resu in results]



        return render_template('index.html', results=results,datas1=datas1_value,names1=names1,
                               datas2=datas2_value, names2=names2,
                               datas3=datas3_value, names3=names3,
                               datas4=datas4,
                               datas5=datas5,names5=names5,
                               datas6=datas6,datas7=datas7
                               )

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    stu_id = session.get('stu_id')
    datas = models.User.query.get(stu_id)
    if not datas:
        return redirect(url_for('login'))
    if request.method == 'GET':
        results = models.Case_item.query.all()
        return render_template('projects/table_s.html', datas=datas, results=results)

@app.route('/login', methods=['GET', 'POST'])
def login():
    stu_id = session.get('stu_id')
    datas = models.User.query.get(stu_id)
    if datas:
        return redirect(url_for('index'))
    if request.method=='GET':
        return render_template('apps/login.html')
    elif request.method=='POST':
        name = request.form.get('name')
        password = request.form.get('password')
        data = models.User.query.filter(and_(models.User.name==name,models.User.password==password)).all()
        if not data:
            return render_template('apps/login.html',error='账号密码错误')
        else:
            session['stu_id'] = data[0].name_id
            session.permanent = True
            return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='GET':
        stu_id = session.get('stu_id')
        datas = models.User.query.get(stu_id)
        if datas:
            return redirect(url_for('index'))
        return render_template('apps/signit.html')
    elif request.method=='POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        data = models.User.query.filter(models.User.name==name).all()
        if data:
            return render_template('apps/signit.html',error='账号名已被注册')
        elif name == '' or email == '' or password == '' :
            return render_template('apps/signit.html', error='输入不能为空')
        else:
            models.db.session.add(models.User(name=name, email=email, password=password, itype='vip'))
            models.db.session.commit()
            return redirect(url_for('login'))



@app.route('/loginout', methods=['GET'])
def loginout():
    if request.method=='GET':
        session['stu_id'] = ''
        session.permanent = False
        return redirect(url_for('login'))

def jiequs(li,num=10):
    """自定义的过滤器,截取字符串"""
    if len(li) < num:
        return li[:num]
    else:
        return li[:num] + '...'

app.add_template_filter(jiequs, "jiequ")
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5001)
