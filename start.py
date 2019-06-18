# -*- coding: utf-8 -*-
# version: python 3.7
# author: Ivy

import json
import requests
import time,sys
import sqlite3,random

################### 自己设置区域 #####################
citycode='021' # 需要爬取的城市代号
keypoolFile='keypool.txt' # key池文件
database='poi.sqlite' # 数据库的文件名
####################################################

def get_data(page_index, url_amap):
    time.sleep(0.5)
    print('解析页码: ' + str(page_index) + '... ...')
    response = requests.get(url_amap)
    poi_json = response.json()

    if poi_json.get("info")=="DAILY_QUERY_OVER_LIMIT":
        print('key超过限制了，换一个')
        print(poi_json)
        return "limit"

    poi_lists = poi_json.get("pois")
    if poi_lists != None or '':
        if len(poi_json.get("pois"))<1:
            return False
        for poi in poi_lists:
            poi_list = []
            poi_list.append(poi.get('id'))
            poi_list.append(poi.get('biz_type'))
            poi_list.append(poi.get('name'))
            poi_list.append(poi.get('type'))
            poi_list.append(poi.get('address'))
            poi_list.append(poi.get('tel'))
            poi_list.append(poi.get('location'))
            poi_list.append(poi.get('pcode'))
            poi_list.append(poi.get('pname'))
            poi_list.append(poi.get('citycode'))
            poi_list.append(poi.get('cityname'))
            poi_list.append(poi.get('adcode'))
            poi_list.append(poi.get('adname'))
            poi_list.append(poi.get('business_area'))
            #print(poi_list)

            try:
                writeDb(poi_list)
                #print('已保存到sqlite')
            except Exception as e:
                print('出错了！')
                print(e)
                print(poi_list)
                sys.exit(1)

    else:
        pass
    return poi_json.get("pois")

def writeDb(poi_list):
    try:
        ins="INSERT or ignore INTO poi VALUES (null,"+",".join(["'%s'" %x for x in poi_list])+")"
        cur.execute(ins)
        conn.commit()
        return True
    except:
        return False

def initDb():
    cre='''Create Table if not exists poi(Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    poi_id INTEGER UNIQUE,
    biz_type TEXT,
    name TEXT,
    type TEXT,
    address text,
    tel text,
    location text,
    pcode text,
    pname text,
    citycode text,
    cityname text,
    adcode text,
    adnametext,
    business_area text)
    '''
    cur.execute(cre)
    conn.commit()
    print('数据库已准备好')

def getKeypool(file):
    with open(file, 'r', encoding='utf-8') as f:
        rows=f.readlines()
        keys=[]
        for row in rows:
            row=row.replace('\n','')
            keys.append(row)
        return keys

def getPOIdata(poicode_now,city):
    global key_pool
    page=1
    while True:
        key=random.choice(key_pool)
        url_amap = 'http://restapi.amap.com/v3/place/text?key={}&types={}&city={}&citylimit=true&children=1&offset=25&page={}&extensions=all'.format(key,poicode_now,city,page)
        json_data = get_data(page, url_amap)

        if json_data=="limit":
            key_pool.remove(key)
            if len(key_pool)<1:
                print('key没存货啦！')
                return False
            continue

        if not json_data:
            print('当前类别爬完了')
            break
        page+=1
    return True


if __name__ == '__main__':

    conn=sqlite3.connect(database)
    cur=conn.cursor()
    initDb()

    # 加载城市列表
    data = open("city.json", encoding="utf-8-sig")
    strJson = json.load(data)

    # 加载获取区域adcode的list
    city = []
    for i in range(len(strJson)): # 获取当前城市所有adcode的列表
        if strJson[i]['citycode']==citycode:
            city.append(strJson[i]['adcode'])

    # 加载key池
    global key_pool
    key_pool=getKeypool(keypoolFile)

    # 获取所有类别的代号
    with open('amap_poicode.CSV','r',encoding='utf-8') as f:
        rows=f.readlines()
        poicode=[]
        for row in rows:
            row.replace('\n','')
            temp_row=row.split(',')
            if temp_row[1]=='NEW_TYPE' or temp_row[1]=='':
                continue
            poicode.append(temp_row[1])

    # 开始一个个爬取
    for y in range(len(city)):
        print('开始第',y+1,'个区域 ','共有',len(city),'个区域')
        for j in range(len(poicode)):
            poicode_now=poicode[j]
            print('爬到第',y+1,'个区域，第',j,'个类别了，代码为',poicode_now)
            result=getPOIdata(poicode_now, city[y])
            if not result: # key的额度不够了，就先退出程序
                print('当前城市序号为',y,'，当前类别序号为',j)
                cur.close()
                conn.close()
                sys.exit(1)

    cur.close()
    conn.close()
