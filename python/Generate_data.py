# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 16:48:08 2021

@author: MECHREV
"""
import MySQLdb
import random

import logging

from datetime import datetime,timedelta
# 打开数据库连接
db = MySQLdb.connect("localhost", "root", "123456", "test", charset='utf8' )

# 使用cursor()方法获取操作游标 
cursor = db.cursor()

cursor.execute("SELECT VERSION()")

data = cursor.fetchone()

print ("Database version : %s " % data)

def generate_data_basic():
    first_name = ["王", "李", "张", "刘", "赵", "蒋", "孟", "陈", "徐", "杨", "沈", "马", "高", "殷", "上官", "钟", "常","钱","孙","冯","张","吴","郑","魏","秦","汪","肖","何","吕","施","章","苗","姜","孔"]
    second_name = ["伟", "华", "建国", "洋", "刚", "万里", "爱民", "牧", "陆", "路", "昕", "鑫", "兵", "硕", "志宏", "峰", "磊", "雷", "文","明浩", "光", "超", "军", "达","月明","正","金开","梓舟","雨轩","子凯","爱国","冬","小明","宇","静"]
    sexall=["男","女"]
    detailall=["自然语言处理","视听觉信息处理","数据科学与大数据技术","计算机科学","计算机工程","并行与分布式"]
    natall=["汉族","回族","满族","朝鲜族","布依族","蒙古族","汉族","汉族","汉族","汉族"]
    polall=["中共党员","共青团员"]
    homeall=["北京市","上海市","天津市","重庆市","黑龙江省哈尔滨市","吉林省吉林市","辽宁省沈阳市","广东省深圳市","广东省广州市","四川省成都市"]
    for i in range(1170300101,1170301099):
        time1="1999-"+str(random.randint(1,12))+"-"+str(random.randint(1,28))
        date1 = datetime.strptime(time1,"%Y-%m-%d")
        birth=datetime.strftime(date1,"%Y-%m-%d")
        name = random.choice(first_name) + random.choice(second_name)
        detail=random.choice(detailall)
        nat=random.choice(natall)
        pol=random.choice(polall)
        home=random.choice(homeall)
        sex=random.choice(sexall)
        sql="INSERT INTO `test`.`basic` (`name`, `studentid`, `sex`, `institute`, `major`, `detail`, `nat`, `pol`, `birth`, `home`) VALUES ('"+name+"', '"+str(i)+"', '"+sex+"', '计算学部', '计算机科学与技术', '"+detail+"', '"+nat+"', '"+pol+"', '"+birth+"', '"+home+"');"
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
def generate_data_sport():
    for i in range(1170300101,1170301099):
        time1=str(random.randint(4,6))+":"+str(random.randint(0,59))
        date1 = datetime.strptime(time1,"%M:%S")
        thousand=datetime.strftime(date1,"%M:%S")
        time1=str(random.randint(4,6))+":"+str(random.randint(0,59))
        date1 = datetime.strptime(time1,"%M:%S")
        thousand=datetime.strftime(date1,"%M:%S")
        fifty=random.uniform(6,9)
        jump=random.uniform(1.5,2.5)
        yinti=random.randint(1,10)
        qianqu=random.uniform(-15,-1)
        sql="INSERT INTO `test`.`sport` (`testgrade`, `coursegrade`, `thousand`, `fifty`, `jump`, `yinti`, `qianqu`, `studentid`) VALUES ('"+str(random.randint(50,100))+"', '"+str(random.randint(50,100))+"', '"+thousand+"', '"+str(fifty)+"', '"+str(jump)+"', '"+str(yinti)+"', '"+str(qianqu)+"', '"+str(i)+"');"
        print(sql)
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
def generate_data_dorm():
    for i in range(1170300101,1170301099):
        for j in range(random.randint(1,30)):
            ditime="2021-5-"+str(random.randint(1,30))+" "+str(random.randint(6,12))+":"+str(random.randint(0,59))+":"+str(random.randint(0,59))
            date1 = datetime.strptime(ditime,"%Y-%m-%d %H:%M:%S")
            date2=date1+timedelta(hours=random.randint(0,8),minutes=random.randint(0,59))
            dotime=datetime.strftime(date2,"%Y-%m-%d %H:%M:%S")
            sql="INSERT INTO `test`.`dormin` (`studentid`, `intime`) VALUES ('"+str(i)+"', '"+ditime+"')";
            try:
               cursor.execute(sql)
               db.commit()
            except:
               db.rollback()
            sql="INSERT INTO `test`.`dormout` (`studentid`, `outtime`) VALUES ('"+str(i)+"', '"+dotime+"')";
            try:
               cursor.execute(sql)
               db.commit()
            except:
               db.rollback() 
def generate_data_lab():
    for i in range(1170300101,1170301099):
        #将学生分类
        if i %3 ==0:
            p=2
        elif i%3==1:
            p=4
        elif i%3==2:
            p=7
        for j in range(random.randint(2,p*3)):
            
            litime="2021-5-"+str(random.randint(1,30))+" "+str(random.randint(6,12))+":"+str(random.randint(0,59))+":"+str(random.randint(0,59))
            date1 = datetime.strptime(litime,"%Y-%m-%d %H:%M:%S")
            date2=date1+timedelta(hours=random.randint(0,p),minutes=random.randint(0,59))
            lotime=datetime.strftime(date2,"%Y-%m-%d %H:%M:%S")
            sql="INSERT INTO `test`.`labin` (`studentid`, `intime`) VALUES ('"+str(i)+"', '"+litime+"')";
            try:
               cursor.execute(sql)
               db.commit()
            except:
               db.rollback()
            sql="INSERT INTO `test`.`labout` (`studentid`, `outtime`) VALUES ('"+str(i)+"', '"+lotime+"')";
            try:
               cursor.execute(sql)
               db.commit()
            except:
               db.rollback() 
def generate_data_class():
    for i in range(1170300101,1170301099):
        #将学生分类
        if i %3 ==0:
            p=2
        elif i%3==1:
            p=4
        elif i%3==2:
            p=7
        for j in range(random.randint(2,p*3)):
            litime="2021-5-"+str(random.randint(1,30))+" "+str(random.randint(6,12))+":"+str(random.randint(0,59))+":"+str(random.randint(0,59))
            date1 = datetime.strptime(litime,"%Y-%m-%d %H:%M:%S")
            date2=date1+timedelta(hours=random.randint(0,p),minutes=random.randint(0,59))
            lotime=datetime.strftime(date2,"%Y-%m-%d %H:%M:%S")
            sql="INSERT INTO `test`.`classin` (`studentid`, `intime`) VALUES ('"+str(i)+"', '"+litime+"')";
            try:
               cursor.execute(sql)
               db.commit()
            except:
               db.rollback()
            sql="INSERT INTO `test`.`classout` (`studentid`, `outtime`) VALUES ('"+str(i)+"', '"+lotime+"')";
            try:
               cursor.execute(sql)
               db.commit()
            except:
               db.rollback() 
def generate_data_score():
    course1=["微积分1","代数与几何","大学物理","概率论与数理统计","大学物理实验","微积分2"]
    course2=["近世代数","算法设计与分析","软件构造","形式语言与自动机","数据结构与算法","计算机系统","计算机网络","数据库系统"]   
    course3=["	综合英语","	学术英语阅读","国际交流英语","学术英语强化训练"]
    course4=["心理与心理健康","沟通与交流","歌曲演唱技巧与舞台表演实践","文学名篇名著赏析"]
    course5=["思想道德修养与法律基础","中国近现代史纲要","毛泽东思想和中国特色社会主义理论体系概论","马克思主义基本原理概论","习近平新时代中国特色社会主义思想专题辅导"]
    for course in course1:
        sql="INSERT INTO `test`.`courseifo` (`coursename`, `ifo`, `ifo2`) VALUES ('"+course+"', '理学院', '计算学部 机械学院 电气学院 材料学院 航天学院 理学院');"
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
    for course in course2:
        sql="INSERT INTO `test`.`courseifo` (`coursename`, `ifo`, `ifo2`) VALUES ('"+course+"', '计算学部', '计算学部');"
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
    for course in course3:
        sql="INSERT INTO `test`.`courseifo` (`coursename`, `ifo`, `ifo2`) VALUES ('"+course+"', '外国语学院', '计算学部 机械学院 电气学院 材料学院 航天学院 理学院');"
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
    for course in course4:
        sql="INSERT INTO `test`.`courseifo` (`coursename`, `ifo`, `ifo2`) VALUES ('"+course+"', '人文社科与法学学院', '计算学部 机械学院 电气学院 材料学院 航天学院 理学院');"
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
    for course in course5:
        sql="INSERT INTO `test`.`courseifo` (`coursename`, `ifo`, `ifo2`) VALUES ('"+course+"', '马克思主义学院', '计算学部 机械学院 电气学院 材料学院 航天学院 理学院');"
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
    for i in range(1170300101,1170301099):
        #将学生分类
        if i %3== 0 : 
            ave=random.randint(55,65)
        elif i%3==1:
            ave=random.randint(65,75)
        elif i%3==2:
            ave=random.randint(85,90)
        ave1=ave+2
        ave2=ave+5
        ave3=ave+1
        ave4=ave-5
        ave5=ave+5
        for course in course1:
            score=ave1+random.randint(-2,3)
            sql="INSERT INTO `test`.`grade` (`studentid`, `coursename`, `grade`) VALUES ('"+str(i)+"', '"+course+"', '"+str(score)+"');"
            try:
               cursor.execute(sql)
               db.commit()
            except:
               db.rollback()
        for course in course2:
            score=ave2+random.randint(-2,3)
            sql="INSERT INTO `test`.`grade` (`studentid`, `coursename`, `grade`) VALUES ('"+str(i)+"', '"+course+"', '"+str(score)+"');"
            try:
               cursor.execute(sql)
               db.commit()
            except:
               db.rollback()
        for course in course3:
            score=ave3+random.randint(-2,3)
            sql="INSERT INTO `test`.`grade` (`studentid`, `coursename`, `grade`) VALUES ('"+str(i)+"', '"+course+"', '"+str(score)+"');"
            try:
               cursor.execute(sql)
               db.commit()
            except:
               db.rollback()
        for course in course4:
            score=ave4+random.randint(-2,3)
            sql="INSERT INTO `test`.`grade` (`studentid`, `coursename`, `grade`) VALUES ('"+str(i)+"', '"+course+"', '"+str(score)+"');"
            try:
               cursor.execute(sql)
               db.commit()
            except:
               db.rollback()
        for course in course5:
            score=ave5+random.randint(-2,3)
            sql="INSERT INTO `test`.`grade` (`studentid`, `coursename`, `grade`) VALUES ('"+str(i)+"', '"+course+"', '"+str(score)+"');"
            try:
               cursor.execute(sql)
               db.commit()
            except:
               db.rollback()
def generate_data_book():
    book1=[["Python自然语言处理实战","978-7-111-59767-4"],["Python程序设计实用教程","978-7-5635-6065-3"],["Python 项目实战从入门到精通","978-7-111-66307-2"],["数据结构与算法:Python版","978-7-111-66363-8"],["Python神经网络入门与实战","978-7-301-31629-0"],["Python大数据应用基础","978-7-115-54386-8"],["Python大数据分析从入门到精通","978-7-301-31355-8"],["Python程序设计与应用","978-7-115-54187-1"],["Python最优化算法实战","978-7-301-31533-0"],["Django实战:Python Web典型模块与项目开发","978-7-115-54020-1"]]
    book2=[["电化学储能材料与原理","978-7-03-065438-0"],["电化学测量","978-7-122-35219-4"],["电化学储能器件及关键材料","978-7-5024-8141-4"],["电化学氧还原的理论基础和应用技术","978-7-5551-1007-1"],["电化学基础教程.第2版","978-7-122-33356-8"]]
    book3=[["艺术导论.第2版","978-7-302-55265-9"],["艺术哲学","978-7-5217-1276-6"],["艺术大师的绘画技法","978-7-5680-5191-0"],["艺术精神","978-7-5057-4323-6"],["艺术自律性研究","978-7-01-021111-4"],["艺术走入地下:公共艺术与地铁","978-7-5682-7028-1"],["艺术与道德","978-7-5520-2561-3"]]
    book4=[["生物学中的功能语言研究","978-7-5690-3758-6"],["中国近代生物学的发展","978-7-5046-6427-3"],["生物科学的哲学","7-5408-3822-1"],["生物工程学:过去·现在·未来","7-5015-5346-7"],["生物技术概说","7-5025-0110-X"]]
    bookname=book1+book2+book3+book4
    for i in range(1170300101,1170301099):
        #将学生分类
        if i %3 ==0:
            p=random.sample(bookname,random.randint(5,6))
        elif i%3==1:
            p=random.sample(bookname,random.randint(7,8))
        elif i%3==2:
            p=random.sample(bookname,random.randint(9,10))
        for j in p:
            outtime="2021-5-"+str(random.randint(1,30))+" "+str(random.randint(6,12))+":"+str(random.randint(0,59))+":"+str(random.randint(0,59))
            date1 = datetime.strptime(outtime,"%Y-%m-%d %H:%M:%S")
            date2=date1+timedelta(days=random.randint(2,10),hours=random.randint(0,8),minutes=random.randint(0,59))
            intime=datetime.strftime(date2,"%Y-%m-%d %H:%M:%S")
            sql="INSERT INTO `test`.`book` (`studentid`, `bookname`, `outtime`, `intime`,`isbn`) VALUES ('"+str(i)+"', '"+j[0]+"', '"+outtime+"', '"+intime+"', '"+j[1]+"');"
            try:
               cursor.execute(sql)
               db.commit()
            except:
               db.rollback()
def generate_data_bookbac():
    book1=[["Python自然语言处理实战","978-7-111-59767-4"],["Python程序设计实用教程","978-7-302-50047-6"],["Python 项目实战从入门到精通","978-7-111-66307-2"],["数据结构与算法:Python版","978-7-111-66363-8"],["Python神经网络入门与实战","978-7-301-31629-0"],["Python大数据应用基础","978-7-115-54386-8"],["Python大数据分析从入门到精通","978-7-301-31355-8"],["Python程序设计与应用","978-7-115-54187-1"],["Python最优化算法实战","978-7-301-31533-0"],["Django实战:Python Web典型模块与项目开发","978-7-115-54020-1"]]
    book2=[["电化学储能材料与原理","978-7-03-065438-0"],["电化学测量","978-7-122-35219-4"],["电化学储能器件及关键材料","978-7-5024-8141-4"],["电化学氧还原的理论基础和应用技术","978-7-5551-1007-1"],["电化学基础教程.第2版","978-7-122-33356-8"]]
    book3=[["艺术导论.第2版","978-7-302-55265-9"],["艺术哲学","978-7-5217-1276-6"],["艺术大师的绘画技法","978-7-5680-5191-0"],["艺术精神","978-7-5057-4323-6"],["艺术自律性研究","978-7-01-021111-4"],["艺术走入地下:公共艺术与地铁","978-7-5682-7028-1"],["艺术与道德","978-7-5520-2561-3"]]
    book4=[["生物学中的功能语言研究","978-7-5690-3758-6"],["中国近代生物学的发展","978-7-5046-6427-3"],["生物科学的哲学","7-5408-3822-1"],["生物工程学:过去·现在·未来","7-5015-5346-7"],["生物技术概说","7-5025-0110-X"]]
    bookname=book1+book2+book3+book4
    n=len(bookname)
    with open("bookbac.txt","r",encoding="utf-8")as f:
        s=f.read()
    bookbac=s.split("//")
    bookbac=bookbac[1:]
    for i in range(n):
        sql="INSERT INTO `test`.`bookbac` (`book`, `bac`) VALUES ('"+bookname[i][0]+"', '"+bookbac[i]+"');"
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
def generate_data_sportuse():
    sport=["足球","篮球","羽毛球","排球","游泳","乒乓球","网球","运动场"]
    for i in range(1170300101,1170301099):
        for j in range(random.randint(1,30)):
            sitime="2021-5-"+str(random.randint(1,30))+" "+str(random.randint(6,12))+":"+str(random.randint(0,59))+":"+str(random.randint(0,59))
            date1 = datetime.strptime(sitime,"%Y-%m-%d %H:%M:%S")
            date2=date1+timedelta(hours=random.randint(0,8),minutes=random.randint(0,59))
            sotime=datetime.strftime(date2,"%Y-%m-%d %H:%M:%S")
            sql="INSERT INTO `test`.`sportuse` (`studentid`, `sport`, `intime`, `outtime`) VALUES ('"+str(i)+"', '"+random.choice(sport)+"', '"+sitime+"', '"+sotime+"');"
            try:
               cursor.execute(sql)
               db.commit()
            except:
               db.rollback()
def generate_data_trade():
    for i in range(1170300101,1170301099):
        #将学生分类
        if i %3 ==0:
            p=30
        elif i%3==1:
            p=20
        elif i%3==2:
            p=5
        k=random.randint(1,7)
        cost1=random.randint(2,6)
        cost2=random.randint(8,15)
        time1="2021-5-1 "+str(random.randint(6,7))+":"+str(random.randint(0,59))+":"+str(random.randint(0,59))
        time2="2021-5-1 "+str(random.randint(11,12))+":"+str(random.randint(0,59))+":"+str(random.randint(0,59))    
        time3="2021-5-1 "+str(random.randint(17,18))+":"+str(random.randint(0,59))+":"+str(random.randint(0,59))
        
        time4="2021-5-1 "+str(random.randint(14,15))+":"+str(random.randint(0,59))+":"+str(random.randint(0,59))
        for j in range(30):
            if j*k*random.randint(1,7)%3==0:
                date1 = datetime.strptime(time1,"%Y-%m-%d %H:%M:%S")
                date2=date1+timedelta(days=j,minutes=random.randint(0,p))
                time11=datetime.strftime(date2,"%Y-%m-%d %H:%M:%S")
                date1 = datetime.strptime(time2,"%Y-%m-%d %H:%M:%S")
                date2=date1+timedelta(days=j,minutes=random.randint(0,p))
                time21=datetime.strftime(date2,"%Y-%m-%d %H:%M:%S")
                date1 = datetime.strptime(time3,"%Y-%m-%d %H:%M:%S")
                date2=date1+timedelta(days=j,minutes=random.randint(0,p))
                time31=datetime.strftime(date2,"%Y-%m-%d %H:%M:%S")
                date1 = datetime.strptime(time4,"%Y-%m-%d %H:%M:%S")
                date2=date1+timedelta(days=j,minutes=random.randint(0,p))
                time41=datetime.strftime(date2,"%Y-%m-%d %H:%M:%S")
                sql1="INSERT INTO `test`.`trade` (`studentid`, `cost`, `tradetime`, `tradetype`) VALUES ('"+str(i)+"', '"+str(cost1+random.random()*2)+"', '"+time11+"', '吃饭');"
                sql2="INSERT INTO `test`.`trade` (`studentid`, `cost`, `tradetime`, `tradetype`) VALUES ('"+str(i)+"', '"+str(cost2+random.random()*3)+"', '"+time21+"', '吃饭');"
                sql3="INSERT INTO `test`.`trade` (`studentid`, `cost`, `tradetime`, `tradetype`) VALUES ('"+str(i)+"', '"+str(cost2+random.random()*3)+"', '"+time31+"', '吃饭');"
                sql4="INSERT INTO `test`.`trade` (`studentid`, `cost`, `tradetime`, `tradetype`) VALUES ('"+str(i)+"', '"+str(cost1+random.random()*3)+"', '"+time41+"', '洗澡');"
                try:
                   cursor.execute(sql1)
                   cursor.execute(sql2)
                   cursor.execute(sql3)
                   cursor.execute(sql4)
                   db.commit()
                except:
                   db.rollback()
        
def generate_log_network():  
    logger = logging.getLogger()
    logger.setLevel(level = logging.INFO)
    handler = logging.FileHandler("log1.txt")
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    for i in range(1170300101,1170301099):
        for j in range(1,31):
            ip="172.20."+str(random.randint(1,126))+"."+str(random.randint(1,254))
            nitime1="2021-05-"+str(j)+" "+str(random.randint(8,10))+":"+str(random.randint(0,59))+":"+str(random.randint(0,59))
            date1 = datetime.strptime(nitime1,"%Y-%m-%d %H:%M:%S")
            nitime1=datetime.strftime(date1,"%Y-%m-%d %H:%M:%S")
            date2=date1+timedelta(hours=random.randint(0,3),minutes=random.randint(0,59))
            notime1=datetime.strftime(date2,"%Y-%m-%d %H:%M:%S")
            date1 = datetime.strptime(notime1,"%Y-%m-%d %H:%M:%S")
            date2=date1+timedelta(hours=random.randint(0,1),minutes=random.randint(0,59))
            nitime2=datetime.strftime(date2,"%Y-%m-%d %H:%M:%S")
            date1 = datetime.strptime(nitime2,"%Y-%m-%d %H:%M:%S")
            
            
            date2=date1+timedelta(hours=random.randint(0,3),minutes=random.randint(0,59))
            notime2=datetime.strftime(date2,"%Y-%m-%d %H:%M:%S")
            date1 = datetime.strptime(notime2,"%Y-%m-%d %H:%M:%S")
            date2=date1+timedelta(hours=random.randint(0,1),minutes=random.randint(0,59))
            nitime3=datetime.strftime(date2,"%Y-%m-%d %H:%M:%S")
            date1 = datetime.strptime(nitime3,"%Y-%m-%d %H:%M:%S")
            date2=date1+timedelta(hours=random.randint(0,3),minutes=random.randint(0,59))
            notime3=datetime.strftime(date2,"%Y-%m-%d %H:%M:%S")
            logger.info(nitime1+" [INFO] "+str(i)+" Assign IP "+ip)
            logger.info(notime1+" [INFO] "+str(i)+" Recycle IP "+ip)
            ip="172.20."+str(random.randint(1,126))+"."+str(random.randint(1,254))
            logger.info(nitime2+" [INFO] "+str(i)+" Assign IP "+ip)
            logger.info(notime2+" [INFO] "+str(i)+" Recycle IP "+ip)
            ip="172.20."+str(random.randint(1,126))+"."+str(random.randint(1,254))
            logger.info(nitime3+" [INFO] "+str(i)+" Assign IP "+ip)
            logger.info(notime3+" [INFO] "+str(i)+" Recycle IP "+ip)
def generate_data_code():
    for i in range(1170300101,1170301099):
        #将学生分类
        if i %3 ==0:
            p=10
        elif i%3==1:
            p=5
        elif i%3==2:
            p=3
        hard=random.randint(p,2*p)
        medium=random.randint(2*p,4*p)
        easy=random.randint(4*p,8*p)
        sql="INSERT INTO `test`.`code` (`studentid`, `easy`, `medium`, `hard`) VALUES ('"+str(i)+"', '"+str(easy)+"', '"+str(medium)+"', '"+str(hard)+"');"
        try:
           cursor.execute(sql)
           db.commit()
        except:
           db.rollback()
def generate_data_mooc():
    date="2021-5-1"
    date1 = datetime.strptime(date,"%Y-%m-%d")
    for i in range(1170300101,1170301099):
        if i %3 ==0:
            p=range(5)
        elif i%3==1:
            p=[5,6]
        elif i%3==2:
            p=[6]
        for j in range(30):
            if j%7 in p or random.randint(0,7) %7 == 0:
                date2=date1+timedelta(days=j)
                date3=datetime.strftime(date2,"%Y-%m-%d")
                sql="INSERT INTO `test`.`mooc` (`studentid`, `st`) VALUES ('"+str(i)+"', '"+date3+"');"
                try:
                   cursor.execute(sql)
                   db.commit()
                except:
                   db.rollback()
#generate_data_basic()
#generate_data_sport() 
#generate_data_dorm()
#generate_data_lab()      
#generate_data_class()    
#generate_data_score()
#generate_data_book()
#generate_data_bookbac()
#generate_data_sportuse()          
#generate_data_trade()
#generate_log_network()
#generate_data_code()     
generate_data_mooc()
db.close()