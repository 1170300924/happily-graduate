# -*- coding: utf-8 -*-
"""
Created on Mon May 24 15:19:09 2021

@author: MECHREV
"""


import MySQLdb
from pyltp import SentenceSplitter, Segmentor,Postagger
from datetime import datetime,timedelta
import math
from sklearn.feature_extraction.text import TfidfVectorizer
import csv
import random
from sklearn.metrics.pairwise import cosine_similarity

# 打开数据库连接
db = MySQLdb.connect("localhost", "root", "123456", "test", charset='utf8' )
# 使用cursor()方法获取操作游标 
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print ("Database version : %s " % data)
segmentor = Segmentor()
segmentor.load(r"ltp_data\cws.model")



def grade_warning():
    courseifo={}
    course=[]
    X=[]
    sql = "SELECT * FROM test.courseifo;"
    stopwords=["学部","学院"]
    try:
       # 执行SQL语句
       cursor.execute(sql)
       # 获取所有记录列表
       results = cursor.fetchall()
    except:
        print("Error: unable to fecth data")
    for result in results:
        course.append(result[1])
        courseifo[result[1]]=result[1]+" "+result[2]+" "+result[3]
    for cou in course:
        sentence = SentenceSplitter.split(courseifo[cou])
        word2=[]
        for sen in sentence:
            words = segmentor.segment(sen)
            word1=list(words)
            for word in word1:
                if word not in stopwords:
                    word2.append(word)
        X.append(word2)
    document = [" ".join(sent0) for sent0 in X]
    tfidf = TfidfVectorizer().fit(document)
    words=tfidf.get_feature_names()
    n=len(words)
    answers=tfidf.transform(document).todense().tolist()
    with open("grade_warning1.csv","w",encoding="gbk",newline='') as f:
        writer = csv.writer(f)
        title=["coursename"]
        title.extend(words)
        writer.writerow(title)
        for i in range(len(course)):
            data=[course[i]]
            data.extend(answers[i])       
            writer.writerow(data)
    cos=cosine_similarity(answers).tolist()
    with open("grade_warning2.csv","w",encoding="gbk",newline='') as f:
        writer = csv.writer(f)
        title=[" "]
        title.extend(course)
        writer.writerow(title)
        for i in range(len(course)):
            data=[course[i]]
            data.extend(cos[i])       
            writer.writerow(data)
    index={}
    for i in range(len(course)):
        index[course[i]]=i
    grade={}
    sql = "SELECT * FROM test.grade;"
    try:
       # 执行SQL语句
       cursor.execute(sql)
       # 获取所有记录列表
       results = cursor.fetchall()
    except:
        print("Error: unable to fecth data")
    for result in results:
        if result[1] not in grade.keys():
            grade[result[1]]=[0]*len(course)
        grade[result[1]][index[result[2]]]=result[3]
    dev=[[0 for i in range(len(course))] for j in range(len(course))]
    avg=[0 for i in range(len(course))]
    for i in grade.keys():
        for j in range(len(course)):
            avg[j]=avg[j]+grade[i][j]
    for i in range(len(course)):
        avg[i]=avg[i]/len(grade.keys())
    for i in range(len(course)):
        for j in range(len(course)):
            dev[i][j]=avg[i]-avg[j]
    return course,index,cos,grade,dev
def pred(coursename,mygrade,cos,dev,course):
    n=len(course)
    pre=0
    fenzi=0
    fenmu=0
    for i in range(n):
        if course[i] is coursename:
            target=i
    for i in range(n):
        if mygrade[i] is not -1 and i is not target:
            fenzi=fenzi+(mygrade[i]+dev[target][i])*(1+cos[target][i])
            fenmu=fenmu+(1+cos[target][i])
    pre=fenzi/fenmu
    return pre
def test(course,index,cos,grade,dev):
    tp=0
    tn=0
    fp=0
    fn=0
    coun=len(course)
    for i in grade.keys():
        for j in range(coun):
            mygrade=list(grade[i])
            mygrade[j]=-1
            ans=pred(course[j],mygrade,cos,dev,course)
            if ans<60 and grade[i][j]<60:
                tp=tp+1
            elif ans>=60 and grade[i][j]<60:
                fn=fn+1
            elif ans<60 and grade[i][j]>=60:
                fp=fp+1
            else:
                tn=tn+1
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
def Analysis(course,index,cos,grade,dev):
    for i in grade.keys():
        word=" "
        for j in (1,8,16):
            mygrade=list(grade[i])
            mygrade[j]=-1
            ans=pred(course[j],mygrade,cos,dev,course)
            if ans<60:
                word=word+"@@"+course[j]+"挂科预警，预测成绩"+str(round(ans,3))
        sql="UPDATE `test`.`myout` SET `alertgk` = '"+word+"' WHERE (`studentid` = '"+str(i)+"');"
        
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
            
course,index,cos,grade,dev=grade_warning()
test(course,index,cos,grade,dev)
Analysis(course,index,cos,grade,dev)
    
    
    