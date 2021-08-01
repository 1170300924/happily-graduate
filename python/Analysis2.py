# -*- coding: utf-8 -*-
"""
Created on Sat May 29 14:56:06 2021

@author: MECHREV
"""

import MySQLdb
from sklearn.cluster import KMeans

# 打开数据库连接
db = MySQLdb.connect("localhost", "root", "123456", "test", charset='utf8' )
# 使用cursor()方法获取操作游标 
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print ("Database version : %s " % data)


def analysis():
    sql = "SELECT * FROM test.myout "
    try:
       # 执行SQL语句
       cursor.execute(sql)
       # 获取所有记录列表
       results = cursor.fetchall()
    except:
        print("Error: unable to fecth data")
    X=[]
    for result in results:
        x=list(result[1:7])
        X.append(x)
    kmeans = KMeans(n_clusters=3).fit(X)
    n=len(X)
    print(kmeans.cluster_centers_)
    labels=list(kmeans.labels_)
    labelnum=[[0 for col in range(3)] for row in range(3)]
    for i in range(n):
        labelnum[i%3][labels[i]]=labelnum[i%3][labels[i]]+1
    r1=max(labelnum[0][0]+labelnum[1][1]+labelnum[2][2],labelnum[0][0]+labelnum[2][1]+labelnum[1][2])
    r2=max(labelnum[0][1]+labelnum[1][0]+labelnum[2][2],labelnum[0][1]+labelnum[1][2]+labelnum[2][0])
    r3=max(labelnum[0][2]+labelnum[1][0]+labelnum[2][1],labelnum[0][2]+labelnum[1][1]+labelnum[2][0])
    r=max(r1,r2,r3)
    acc=r/n
    print(acc)
    print(labelnum)
    return labelnum
analysis()