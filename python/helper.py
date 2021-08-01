# -*- coding: utf-8 -*-
"""
Created on Sun May 16 21:51:14 2021

@author: MECHREV
"""
l=[]
with open("code.txt","r")as f:
    n=int(f.readline().strip())
    for i in range(n):
        l.append(f.readline())
    s=f.read()
for i in range(n):
    s1=l[i].split(" ")[0].strip()
    s2=l[i].split(" ")[1].strip()
    s=s.replace(s1,s2)
with open("code.txt","w")as f:
    f.write(str(n)+"\n")
    f.writelines(l)
    f.write(s)
