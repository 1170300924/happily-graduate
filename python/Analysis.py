# -*- coding: utf-8 -*-
"""
Created on Mon May 17 15:00:41 2021

@author: MECHREV
"""
import MySQLdb
from pyltp import SentenceSplitter, Segmentor,Postagger
from datetime import datetime,timedelta
import math
from sklearn.feature_extraction.text import TfidfVectorizer
import csv
import random

# 打开数据库连接
db = MySQLdb.connect("localhost", "root", "123456", "test", charset='utf8' )
# 使用cursor()方法获取操作游标 
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print ("Database version : %s " % data)
segmentor = Segmentor()
segmentor.load(r"ltp_data\cws.model")
postagger = Postagger()
postagger.load(r"ltp_data\pos.model")

def st():
    for i in range(1170300101,1170301099):
        sql="INSERT INTO `test`.`myout` (`studentid`) VALUES ('"+str(i)+"');"
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
def analysis_read():
    sql = "SELECT * FROM test.bookbac;"
    bookbac={}
    bookname={}
    stopwords=[" ","介绍","本书","方法","解释","部分","基础"]
    try:
       # 执行SQL语句
       cursor.execute(sql)
       # 获取所有记录列表
       results = cursor.fetchall()
    except:
        print("Error: unable to fecth data")
    for line in results:
        sentence = SentenceSplitter.split(line[2])
        word2=[]
        for sen in sentence:
            words = segmentor.segment(sen)
            word1=list(words)
            for word in word1:
                if word not in stopwords:
                    word2.append(word)
        
        bookbac[line[1]]=word2
        sentence = SentenceSplitter.split(line[1])
        word2=[]
        for sen in sentence:
            words = segmentor.segment(sen)
            word1=list(words)
            for word in word1:
                if word not in stopwords:
                    word2.append(word)
        bookname[line[1]]=word2
    X=[]
    readanl=[]
    for i in range(1170300101,1170301099):
        wordlist=[]
        sql = "SELECT * FROM test.book where studentid="+str(i)+";"
        try:
           # 执行SQL语句
           cursor.execute(sql)
           # 获取所有记录列表
           results = cursor.fetchall()
        except:
            print("Error: unable to fecth data")
        results=list(results)
        results.sort(key=lambda line: line[3],reverse=True)
        tmp=[i,len(results),0,[results[0][2],results[1][2],results[2][2]]]
        for line in results:
            date = line[3]
            datenow = datetime.strptime('2021-05-30 00:00:00','%Y-%m-%d %H:%M:%S')        
            if datenow-date<timedelta(days=7):
                tmp[2]=tmp[2]+1
            wordlist.extend(bookbac[line[2]])
            wordlist.extend(bookname[line[2]])
        X.append(wordlist)
        readanl.append(tmp)
    document = [" ".join(sent0) for sent0 in X]
    tfidf = TfidfVectorizer().fit(document)
    words=tfidf.get_feature_names()
    n=len(words)
    answers=tfidf.transform(document).todense().tolist()
    ret=[]
    p=0
    for line in answers:
        ti=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        ind=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        for i in range(10):
            for j in range(n):
                if (line[j] > ti[i]) and (j not in ind):
                    ti[i]=line[j]
                    ind[i]=j
        for i in range(10):
            ind[i]=words[ind[i]]
        ret.append(ind)
        readanl[p].append(ret[p])
        p=p+1
    for ans in readanl:
        s=str(ans[1])+"@@"+str(ans[2])+"@@"+"@@".join(ans[3])+"@@"+" ".join(ans[4])
        sql="UPDATE `test`.`myout` SET `readword` = '"+s+"' WHERE (`studentid` = '"+str(ans[0])+"');"
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
        sql="UPDATE `test`.`myout` SET `reading` = '"+str(ans[1]*10)+"' WHERE (`studentid` = '"+str(ans[0])+"');"
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
    return readanl
def analysis_grade():
    sql = "SELECT * FROM test.courseifo;"
    try:
       # 执行SQL语句
       cursor.execute(sql)
       # 获取所有记录列表
       results = cursor.fetchall()
    except:
        print("Error: unable to fecth data")
    ifo={}
    for line in results:
        ifo[line[1]]=line[2]
    for i in range(1170300101,1170301099):
        courseifo=["理学院","计算学部","外国语学院","人文社科与法学学院","马克思主义学院"]
        coursenum=[6,8,4,4,5,27]
        grade=[0,0,0,0,0,0]
        
        sql = "SELECT * FROM test.grade where studentid="+str(i)+";"
        try:
           # 执行SQL语句
           cursor.execute(sql)
           # 获取所有记录列表
           results = cursor.fetchall()
        except:
            print("Error: unable to fecth data")
        gradeall=[]
        for line in results:
            grade[5]=grade[5]+line[3]
            gradeall.append([line[2],line[3]])
            for j in range(5):
                if ifo[line[2]] == courseifo[j]:
                    grade[j]=grade[j]+line[3]
        for j in range(6):
            grade[j]=str(round(grade[j]/coursenum[j],2))
        gradeall.sort(key=lambda x:x[1],reverse=True)
        s="@@".join(grade)+"@@"+gradeall[0][0]+":"+str(gradeall[0][1])+"@@"+gradeall[1][0]+":"+str(gradeall[1][1])+"@@"+gradeall[2][0]+":"+str(gradeall[2][1])
        sql="UPDATE `test`.`myout` SET `grade` = '"+str(grade[5])+"',`gradeword` = '"+s+"' WHERE (`studentid` = '"+str(i)+"');"
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
def analysis_reg():
    for i in range(1170300101,1170301099):
        meal1=[0 for x in range(0,25)]
        meal2=[0 for x in range(0,26)]
        meal3=[0 for x in range(0,26)]
        xz=[0 for x in range(0,26)]
        ret=[]
        ret2=[]
        timel1=[]
        timel2=[]
        timel3=[]
        timex=[]
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
                xz[time2-14*6+1]=xz[time2-14*6+1]+1
                timex.append(time1)
            elif time2<10*6:
                meal1[time2-6*6+1]=meal1[time2-6*6+1]+1
                timel1.append(time1)
            elif time2<15*6:
                meal2[time2-11*6+1]=meal2[time2-11*6+1]+1
                timel2.append(time1)
            else:
                meal3[time2-17*6+1]=meal3[time2-17*6+1]+1
                timel3.append(time1)
        timel1.sort()
        timel2.sort()
        timel3.sort()
        timex.sort()
        mcount=0
        en=0
        for m in meal1:
            mcount=mcount+m
        for j in range(len(meal1)):
            meal1[j]=meal1[j]/mcount
        for m in meal1:
            if m >0:
                en=en+m*math.log(m)
        en=en*(-1)
        ret2.append(en)
        en=str(round(en,5))
        ret.append(en)
        mcount=0
        en=0
        for m in meal2:
            mcount=mcount+m
        for j in range(len(meal2)):
            meal2[j]=meal2[j]/mcount
        for m in meal2:
            if m >0:
                en=en+m*math.log(m)
        en=en*(-1)
        ret2.append(en)
        en=str(round(en,5))
        ret.append(en)
        mcount=0
        en=0
        for m in meal3:
            mcount=mcount+m
        for j in range(len(meal3)):
            meal3[j]=meal3[j]/mcount
        for m in meal3:
            if m >0:
                en=en+m*math.log(m)
        en=en*(-1)
        ret2.append(en)
        en=str(round(en,5))
        ret.append(en)
        mcount=0
        en=0
        for m in xz:
            mcount=mcount+m
        for j in range(len(xz)):
            xz[j]=xz[j]/mcount
        for m in xz:
            if m >0:
                en=en+m*math.log(m)
        en=en*(-1)
        ret2.append(en)
        en=str(round(en,5))
        ret.append(en)
        date11=datetime.strptime("05:50","%H:%M")
        date21=datetime.strftime(date11+timedelta(minutes=10*meal1.index(max(meal1))),"%H:%M")+"-"+datetime.strftime(date11+timedelta(minutes=10*(1+meal1.index(max(meal1)))),"%H:%M")
        date12=datetime.strptime("10:50","%H:%M")
        date22=datetime.strftime(date12+timedelta(minutes=10*meal2.index(max(meal2))),"%H:%M")+"-"+datetime.strftime(date12+timedelta(minutes=10*(1+meal2.index(max(meal2)))),"%H:%M")
        date13=datetime.strptime("16:50","%H:%M")
        date23=datetime.strftime(date13+timedelta(minutes=10*meal3.index(max(meal3))),"%H:%M")+"-"+datetime.strftime(date13+timedelta(minutes=10*(1+meal3.index(max(meal3)))),"%H:%M")
        date14=datetime.strptime("13:50","%H:%M")
        date24=datetime.strftime(date14+timedelta(minutes=10*xz.index(max(xz))),"%H:%M")+"-"+datetime.strftime(date14+timedelta(minutes=10*(1+xz.index(max(xz)))),"%H:%M")
        s="@@".join(ret)+"@@"+str(timel1[0])+"@@"+str(timel1[len(timel1)-1])
        s=s+"@@"+str(timel2[0])+"@@"+str(timel2[len(timel2)-1])
        s=s+"@@"+str(timel3[0])+"@@"+str(timel3[len(timel3)-1])
        s=s+"@@"+str(timex[0])+"@@"+str(timex[len(timex)-1])
        s=s+"@@"+date21+"@@"+date22+"@@"+date23+"@@"+date24
        retmean=sum(ret2)/4
        s=str(round(retmean,5))+"@@"+s
        retmean=(int)((retmean)*50)
        if retmean>100:
            print(retmean)
        sql="UPDATE `test`.`myout` SET `regular` = '"+str(retmean)+"',`regularword` = '"+s+"' WHERE (`studentid` = '"+str(i)+"');"
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
def analysis_hobby():
    weibo={}
    users=[]
    with open("microblogPCU/user_post.csv","r",encoding="gbk",errors="ignore") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] not in weibo.keys():
                weibo[row[0]]=[]
            if len(weibo[row[0]])>100:
                continue
            if "http" not in row[2]:
                weibo[row[0]].append(row[2])
    for word in weibo.keys():
        if len(weibo[word])>6 and word is not "":
            users.append(word)
    random.shuffle(users)
    userl={}
    with open("microblogPCU/userlist.csv","w",encoding="gbk") as f:
        writer = csv.writer(f)
        writer.writerow(["studentid","weibo_name"])
        for i in range(1170300101,1170301099):
            userl[i]=users[i-1170300101]
            writer.writerow([i,users[i-1170300101]])
    X=[]
    for i in range(1170300101,1170301099):
        user=userl[i]
        file=""
        for w in weibo[user]:
            file=file+" "+w
        stopwords=[" "]
        sentence = SentenceSplitter.split(file)
        word2=[]
        for sen in sentence:
            words = segmentor.segment(sen)
            word1=list(words)
            postags = postagger.postag(words)
            pos=list(postags)
            for word in zip(word1,pos):
                if word[0] not in stopwords and ('v' in word[1] or 'n' in word[1]):
                    word2.append(word[0])
        X.append(word2)
    document = [" ".join(sent0) for sent0 in X]
    tfidf = TfidfVectorizer().fit(document)
    words=tfidf.get_feature_names()
    n=len(words)
    answers=tfidf.transform(document).todense().tolist()
    readanl=[]
    for line in answers:
        ti=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        ind=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        for i in range(10):
            for j in range(n):
                if (line[j] > ti[i]) and (j not in ind):
                    ti[i]=line[j]
                    ind[i]=j
        for i in range(10):
            ind[i]=words[ind[i]]
        tmp=ind
        readanl.append(tmp)
    for i in range(1170300101,1170301099):
        s="@@".join(readanl[i-1170300101])
        sql="UPDATE `test`.`myout` SET `hobbyword` = '"+s+"' WHERE (`studentid` = '"+str(i)+"');"
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
    return readanl
def analysis_hard():
    for i in range(1170300101,1170301099):
        sql = "SELECT * FROM test.labin where studentid="+str(i)+";"
        try:
           # 执行SQL语句
           cursor.execute(sql)
           # 获取所有记录列表
           results = cursor.fetchall()
        except:
            print("Error: unable to fecth data")
        sql = "SELECT * FROM test.labout where studentid="+str(i)+";"
        try:
           # 执行SQL语句
           cursor.execute(sql)
           # 获取所有记录列表
           results2 = cursor.fetchall()
        except:
            print("Error: unable to fecth data")
        intime=[]
        outtime=[]
        for result in results:
            intime.append(result[1])
        for result in results2:
            outtime.append(result[1])
        intime.sort()
        outtime.sort()
        m=len(intime)
        n=len(outtime)
        p=0
        q=0
        studytime=0
        bigtime=0
        while p<n and q<m:
            while intime[p].date()<outtime[q].date():
                p=p+1
            while intime[p].date()>outtime[q].date():
                q=q+1
            studytime=studytime+(outtime[p]-intime[q]).total_seconds()
            if (outtime[p]-intime[q]).total_seconds()>bigtime:
                bigtime=(outtime[p]-intime[q]).total_seconds()
                sttime=intime[p]
                edtime=outtime[q]
            p=p+1
            q=q+1
        hour1=studytime/3600
        sql = "SELECT * FROM test.classin where studentid="+str(i)+";"
        try:
           # 执行SQL语句
           cursor.execute(sql)
           # 获取所有记录列表
           results = cursor.fetchall()
        except:
            print("Error: unable to fecth data")
        sql = "SELECT * FROM test.classout where studentid="+str(i)+";"
        try:
           # 执行SQL语句
           cursor.execute(sql)
           # 获取所有记录列表
           results2 = cursor.fetchall()
        except:
            print("Error: unable to fecth data")
        intime=[]
        outtime=[]
        for result in results:
            intime.append(result[1])
        for result in results2:
            outtime.append(result[1])
        intime.sort()
        outtime.sort()
        m=len(intime)
        n=len(outtime)
        p=0
        q=0
        studytime=0
        bigtime2=0
        while p<n and q<m:
            while intime[p].date()<outtime[q].date():
                p=p+1
            while intime[p].date()>outtime[q].date():
                q=q+1
            studytime=studytime+(outtime[p]-intime[q]).total_seconds()
            if (outtime[p]-intime[q]).total_seconds()>bigtime2:
                bigtime2=(outtime[p]-intime[q]).total_seconds()
                sttime2=intime[p]
                edtime2=outtime[q]
            p=p+1
            q=q+1
        hour2=studytime/3600
        hour=hour1+hour2
        if hour<40:
            score=int(30+hour/2)
        else:
            score=int(30+20+(hour-40)/3)
        if score >100:
            print(score)
        hardword=str(round(hour1,3))+"@@"+str(round(bigtime/3600,3))+"@@"+str(sttime)+"@@"+str(edtime)+"@@"+str(round(hour2,3))+"@@"+str(round(bigtime2/3600,3))+"@@"+str(sttime2)+"@@"+str(edtime2)
        sql="UPDATE `test`.`myout` SET `hard` = '"+str(score)+"',`hardword` = '"+hardword+"' WHERE (`studentid` = '"+str(i)+"');"
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
def analysis_social():
    time=[]
    for i in range(8):
        time.append({})
    for i in range(1170300101,1170301099):
        sql = "SELECT * FROM test.labin where studentid="+str(i)+";"
        time[0][i]=[]
        try:
           # 执行SQL语句
           cursor.execute(sql)
           # 获取所有记录列表
           results = cursor.fetchall()
        except:
            print("Error: unable to fecth data")
        for result in results:
            time[0][i].append(result[1])
        
        sql = "SELECT * FROM test.labout where studentid="+str(i)+";"
        time[1][i]=[]
        try:
           # 执行SQL语句
           cursor.execute(sql)
           # 获取所有记录列表
           results = cursor.fetchall()
        except:
            print("Error: unable to fecth data")
        for result in results:
            time[1][i].append(result[1])
        
        sql = "SELECT * FROM test.classin where studentid="+str(i)+";"
        time[2][i]=[]
        try:
           # 执行SQL语句
           cursor.execute(sql)
           # 获取所有记录列表
           results = cursor.fetchall()
        except:
            print("Error: unable to fecth data")
        for result in results:
            time[2][i].append(result[1])
        
        sql = "SELECT * FROM test.classout where studentid="+str(i)+";"
        time[3][i]=[]
        try:
           # 执行SQL语句
           cursor.execute(sql)
           # 获取所有记录列表
           results = cursor.fetchall()
        except:
            print("Error: unable to fecth data")
        for result in results:
            time[3][i].append(result[1])
        
        sql = "SELECT * FROM test.trade where studentid="+str(i)+";"
        time[4][i]=[]
        time[5][i]=[]
        time[6][i]=[]
        time[7][i]=[]
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
                time[4][i].append(result[3])
            elif time2<10*6:
                time[5][i].append(result[3])
            elif time2<15*6:
                time[6][i].append(result[3])
            else:
                time[7][i].append(result[3])
        time[4][i].sort()
        time[5][i].sort()
        time[6][i].sort()
        time[7][i].sort()
        time[1][i].sort()
        time[2][i].sort()
        time[3][i].sort()
        time[0][i].sort()
    close=[]
    for i in range(8):
        close.append({})
    for i in range(1170300101,1170301099):
        if i%100 == 0:
            print(i)
            print(datetime.now())
        for k in range(8):
            close[k][i]=[]
            for j in range(1170300101,1170301099):
                if j == i :
                    continue
                m=len(time[k][i])
                n=len(time[k][j])
                p=0
                q=0
                while p<m and q<n:
                    if time[k][i][p].date()>time[k][j][q].date():
                        q=q+1
                    elif time[k][i][p].date()<time[k][j][q].date():
                        p=p+1
                    elif -600<(time[k][i][p]-time[k][j][q]).total_seconds()<600:
                        close[k][i].append(j)
                        p=p+1
                        q=q+1
                    else:
                        p=p+1
                        q=q+1 
    ret={}
    for i in range(1170300101,1170301099):
        ret[i]={}
        if i%100 == 0:
            print(i)
            print(datetime.now())
        for j in range(1170300101,1170301099):
            c=0
            for k in range(8):
                n=len(close[k][i])
                show=0
                for p in range(n):
                    if close[k][i][p]==j:
                        show=show+1
                if len(close[k][i]) is not 0 and len(time[k][i]) is not 0:
                    c=c+show*998/len(close[k][i])/len(time[k][i])
            ret[i][j]=c
        ans=sorted(ret[i].items(), key = lambda kv:(kv[1], kv[0]),reverse=True)
        friendn=1
        friendn2=1
        for f in ans:
            if f[1]>20:
                friendn=friendn+1
            elif f[1]>3:
                friendn2=friendn2+1
        score=int(30+math.log(friendn*5+friendn2*3)*10)
        if score >100:
            print(score)
        s=str(ans[0][0])+"@@"+str(round(ans[0][1],3))+"@@"+str(ans[1][0])+"@@"+str(round(ans[1][1],3))+"@@"+str(ans[2][0])+"@@"+str(round(ans[2][1],3))+"@@"+str(ans[3][0])+"@@"+str(round(ans[3][1],3))
        sql="UPDATE `test`.`myout` SET `social` = '"+str(score)+"',`socialword` = '"+s+"' WHERE (`studentid` = '"+str(i)+"');"
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
    return ans
def analysis_code():
    for i in range(1170300101,1170301099):
        sql = "SELECT * FROM test.code where studentid="+str(i)+";"
        try:
           # 执行SQL语句
           cursor.execute(sql)
           # 获取所有记录列表
           results = cursor.fetchall()
        except:
            print("Error: unable to fecth data")
        hard=results[0][2]
        medium=results[0][3]
        easy=results[0][4]
        score=35+math.log(hard*10+medium*5+easy+1)*10
        s="编码维度评分为： "+str(round(score,3))+"， 共解决hard："+str(hard)+"道，medium："+str(medium)+"道，easy："+str(easy)+"道。"
        sql="UPDATE `test`.`myout` SET `codeword` = '"+s+"' WHERE (`studentid` = '"+str(i)+"');"
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
def analysis_mooc():
    a=[0,0,0]
    for i in range(1170300101,1170301099):
        mooc=[0 for x in range(0,7)]
        sql = "SELECT * FROM test.mooc where studentid="+str(i)+";"
        try:
           # 执行SQL语句
           cursor.execute(sql)
           # 获取所有记录列表
           results = cursor.fetchall()
        except:
            print("Error: unable to fecth data")
        
        for result in results:
            week=result[2].weekday()
            mooc[week]=mooc[week]+1
            mcount=0
        en=0
        for m in mooc:
            mcount=mcount+m
        for j in range(len(mooc)):
            mooc[j]=mooc[j]/mcount
        for m in mooc:
            if m >0:
                en=en+m*math.log(m)
        en=en*(-1)
        en2=round(en,5)
        en=str(round(en,5))
        if en2>1.70 or mcount>15:
            a[0]=a[0]+1
            s="mooc评价：坚持看mooc者，熵值为: "+en+"，累计看mooc天数："+str(mcount)
        elif en2>1.3 and mcount>6:
            a[1]=a[1]+1
            s="mooc评价：集中刷mooc者，熵值为: "+en+"，累计看mooc天数："+str(mcount)
        else:
            a[2]=a[2]+1
            s="mooc评价：较少看mooc者，熵值为: "+en+"，累计看mooc天数："+str(mcount)
        sql="UPDATE `test`.`myout` SET `moocword` = '"+s+"' WHERE (`studentid` = '"+str(i)+"');"
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
    print(a)
#st()
#analysis_read()
#analysis_grade()
#analysis_reg()
#analysis_hobby()
analysis_hard()        
#analysis_social()
#analysis_code()
#analysis_mooc()
segmentor.release()
postagger.release()
db.close()