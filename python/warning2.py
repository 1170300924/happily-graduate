# -*- coding: utf-8 -*-
"""
Created on Fri May 28 17:13:58 2021

@author: MECHREV
"""
import MySQLdb
from pyltp import SentenceSplitter, Segmentor,Postagger
from datetime import datetime,timedelta
import math
from sklearn import tree
import csv
import random
import numpy
# 打开数据库连接
db = MySQLdb.connect("localhost", "root", "123456", "test", charset='utf8' )
# 使用cursor()方法获取操作游标 
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print ("Database version : %s " % data)

def warning2():
    X=[]
    Y=[]
    for i in range(1170300101,1170301099):
        xz=[]
        meal1=[]
        meal2=[]
        meal3=[]
        x=[]
        sql = "SELECT * FROM test.trade where studentid="+str(i)+";"
        try:
           # 执行SQL语句
           cursor.execute(sql)
           # 获取所有记录列表
           results = cursor.fetchall()
        except:
            print("Error: unable to fecth data")
        
        for result in results:
            time1=result[3].time()
            time2=time1.hour*6+(int)(time1.minute/10)
            if result[4] == '洗澡':
                xz.append(result[2])
            elif time2<10*6:
                meal1.append(result[2])
            elif time2<15*6:
                meal2.append(result[2])
            else:
                meal3.append(result[2])
            
        x.append(len(xz))
        x.append(len(meal1))
        x.append(len(meal2))
        x.append(len(meal3))
            
        if len(xz) == 0:
            x.append(3)
        else:
            x.append(sum(xz)/len(xz))
        if len(meal1) == 0:
            x.append(10.1)
        else:
            x.append(sum(meal1)/len(meal1))
        if len(meal2) == 0:
            x.append(10.1)
        else:
            x.append(sum(meal2)/len(meal2))
        if len(meal3) == 0:
            x.append(10.1)
        else:
            x.append(sum(meal3)/len(meal3))
        sql = "SELECT hard,reading FROM test.myout where studentid="+str(i)+";"
        try:
           # 执行SQL语句
           cursor.execute(sql)
           # 获取所有记录列表
           results = cursor.fetchall()
        except:
            print("Error: unable to fecth data")
        x.append(results[0][0])
        x.append(results[0][1])
        sql = "SELECT sex FROM test.basic where studentid="+str(i)+";"
        try:
           # 执行SQL语句
           cursor.execute(sql)
           # 获取所有记录列表
           results = cursor.fetchall()
        except:
            print("Error: unable to fecth data")
        X.append(x)
        if random.randint(1,20)==1:
            Y.append(-1)
        elif random.randint(1,100)==1:
            Y.append(1)
        elif sum(meal1)/len(meal1)<3.5 and len(meal1) >15 and sum(meal2)/len(meal2)<13 and sum(meal3)/len(meal3)<13:
            Y.append(1)
        elif sum(meal1)/len(meal1)<3.5 and x[9] >=70 and sum(meal2)/len(meal2)<13 and sum(meal3)/len(meal3)<13:
            Y.append(1)
        elif sum(meal1)/len(meal1)<3.5 and x[8] >=70 and sum(meal2)/len(meal2)<13 and sum(meal3)/len(meal3)<13:
            Y.append(1)
        elif sum(xz)/len(xz)<3 and sum(meal2)/len(meal2)<11 and sum(meal3)/len(meal3)<11:
            Y.append(1)
        elif sum(meal1)/len(meal1)<3 and sum(meal2)/len(meal2)<11 and sum(meal3)/len(meal3)<11:
            Y.append(1)
        else:
            Y.append(-1)
    clf = tree.DecisionTreeClassifier(criterion="gini",max_depth=4)
    clf = clf.fit(X[500:], Y[500:])
    Y2=clf.predict(X[:500])
    tp=0
    tn=0
    fp=0
    fn=0
    for p in zip(Y2,Y[:500]):
        if p[0]==1 and p[1]==1:
            tp=tp+1
        elif p[0]==-1 and p[1]==-1:
            tn=tn+1
        elif p[0]==-1 and p[1]==1:
            fn=fn+1
        elif p[0]==1 and p[1]==-1:
            fp=fp+1
    
    print("tp: "+str(tp))
    print("fn: "+str(fn))
    print("fp: "+str(fp))
    print("tn: "+str(tn))
    acc=(tp+tn)/(tp+tn+fp+fn)
    p=tp/(tp+fp)
    r=tp/(tp+fn)
    f1=2*p*r/(p+r)
    print("acc: "+str(acc))
    print("p: "+str(p))
    print("r: "+str(r))
    print("f1: "+str(f1))
    with open("out.dot", 'w') as f :
        f = tree.export_graphviz(clf, out_file = f,
                feature_names = ["time_bath","time_breakfast","time_lunch","time_dinner","cost_bath","cost_breakfast","cost_lunch","cost_dinner","reading","hard"])
    return X,clf
def analysis(X,clf):
    Y=clf.predict(X)
    for i in range(1170300101,1170301099):
        if Y[i-1170300101] == 1:
            word="贫困生预警"
            sql="UPDATE `test`.`myout` SET `alertpk` = '"+word+"' WHERE (`studentid` = '"+str(i)+"');"
            try:
               cursor.execute(sql)
               db.commit()
            except:
               db.rollback()
        else:
            sql="UPDATE `test`.`myout` SET `alertpk` = ' ' WHERE (`studentid` = '"+str(i)+"');"
            try:
               cursor.execute(sql)
               db.commit()
            except:
               db.rollback()

X,clf=warning2()
analysis(X,clf)