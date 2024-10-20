import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings()
from models import *
import time
import pandas as pd

session = requests.session()

url_1 = 'https://piao.qunar.com/'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
}
h = session.get(url=url_1,headers=headers,verify=False)
print(h)



url = 'https://piao.qunar.com/ticket/list.htm'
for ii in range(5,20):
    time.sleep(1)
    m = {
        "keyword": "中国",
        "region": "",
        "from": "mpl_search_suggest",
        "sort": "",
        "page": ii,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
        "Referer": "https://piao.qunar.com/ticket/list.htm?keyword=%E5%8C%97%E4%BA%AC&region=&from=mpl_search_suggest"
    }

    h = session.get(url=url,headers=headers,verify=False,params=m)
    print(h)
    soup = BeautifulSoup(h.text,'html.parser')
    result_list = soup.select('div.result_list > div')
    for result in result_list:
        name = result.select('h3.sight_item_caption')[0].text.strip()
        print(name)
        price = result.select('span.sight_item_price > em')[0].text.strip()
        print(price)
        product_star_level = result.select('span.product_star_level > em')[0].text.strip()
        print(product_star_level)
        xiaoliang = result.select('span.hot_num')[0].text.strip()
        print(xiaoliang)
        try:
            level = result.select('span.level')[0].text.strip()
        except:
            level = ''
        print(level)
        city = result.select('span.area > a')[0].text.strip()
        print(city)
        address_color999 = result.select('p.address.color999 > span')[0].text.strip()
        print(address_color999)
        jieshao = result.select('div.intro.color999')[0].text.strip()
        print(jieshao)
        jindians = result.select('div.relation-subsight > span')
        strs = []
        for jindian in jindians:
            strs.append(jindian.text.strip())
        print(strs)
        pingfen = 0
        product_star_level = str(product_star_level).replace('热度 ','')
        if product_star_level:
            pingfen = product_star_level.strip()
        xingji = '0A'
        level = str(level).replace('景区','')
        if level:
            xingji = level.strip()




        if not Case_item.query.filter(Case_item.name==name.strip()).all():

            db.session.add(Case_item(name=name.strip(), price=price,pingfen=pingfen,xiaoliang=xiaoliang.strip(),xingji=xingji,
                                     shengfen = str(city).split('·')[0],dizi=str(address_color999).replace('地址：','').strip(),
                                     text=jieshao,jingdian=','.join(strs)[:100]
                                     ))
            db.session.commit()



