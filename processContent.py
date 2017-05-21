#coding:utf-8
import sys
import re
import os
import shutil
import jieba
import thulac

def checkVerb(s):
    verb=["找","寻","for","征","拐"]
    for t in verb:
        if t in s:
            return True
    return False

def checkMale(s):
    male=["gg","男","汉","哥","弟","man","boy","伙","基友"]
    for t in male:
        if(t in s):
            return True
    return False

def checkFemale(s):
    female=["mm","妹","女","姐","woman","girl","姑娘","闺蜜"]
    for t in female:
        if(t in s):
            return True
    return False

def findSex(s):
    for i in range(len(s)):
        s[i]=s[i].lower()
    #print(s)
    if "re" in s[0]:
        return "N"
    flag=False
    for i in range(len(s)):
        if checkVerb(s[i]):
            for j in range(i+1,len(s)):
                if(checkVerb(s[j])):
                    break
                if checkMale(s[j]):
                    return "M"
                if checkFemale(s[j]):
                    return "F"
            flag=True
    if not flag:
        return "N"
    for i in range(len(s)):
        if checkVerb(s[i]):
            break
        if checkMale(s[i]):
            return "F"
        if checkFemale(s[i]):
            return "M"

def checkTurning(s):
    turning=["期待","期望","希望","你","要求","心目","心中","理想"]
    for t in turning:
        if t in s:
            return True
    #if sex=="M" and "他" in s:
     #   return True
    #if sex=="F" and "她" in s:
     #   return True
    return False

def checkMy(s):
    my=["我","个人","基本","自己"]
    for t in my:
        if t in s:
            return True
    return False

def checkInfo(s):
    info=["信息","介绍","简介"]
    for t in info:
        if t in s:
            return True
    return False

def findTurning(s):
    for i in range(len(s)):
        s[i]=s[i].lower()
    p=len(s)
    for i in range(len(s)):
        if checkTurning(s[i]):
            if i*5>=len(s):
                return i
        '''if checkMy(s[i]):
            print("***")
            if checkInfo(s[i]) or (i<len(s)-1 and checkInfo(s[i+1])):
                p=len(s)
                print(s[i],end="")
                print(s[i+1])'''
    for i in range(len(s)):
        if checkTurning(s[i]):
            if i*8>=len(s):
                return i
    return p

def change(s):
    t=0
    for i in s:
        if(i<"0" or i>"9"):
            return t
        t=t*10+int(i)
    return t

a=thulac.thulac()

def findHeight(s):
    tmp=0
    for i in range(len(s)):
        t=a.cut(s[i])
        if len(t)==0:
            continue
        if t[0][1]=="m":
            #print(s[i])
            t=change(s[i])
            if "cm" in s[i]:
                return t
            if t>=100 and t<=200 and s[i-1]!="@":
                for j in range(max(0,i-2),min(len(s),i+3)):
                    if "高" in s[j]:
                        return t;
                #tmp=t
    return tmp

def findWeight(s):
    tmp=0
    for i in range(len(s)):
        t = a.cut(s[i])
        if len(t)==0:
            continue
        if t[0][1] == "m":
            #print(s[i])
            t = change(s[i])
            if "kg" in s[i]:
                return t

            for j in range(i+1,min(len(s),i+3)):
                if "千克" in s[j] or "公斤" in s[j]:
                    return t;

            for j in range(i+1,min(len(s),i+3)):
                if "公斤" not in s[j] and "斤" in s[j]:
                    return t/2;

            if t>=35 and t <=120:
                for j in range(max(0,i-2),min(len(s),i+3)):
                    if "重" in s[j]:
                        return t;
                #tmp = t
    return tmp

def findYear1(s):
    tmp = 0
    for i in range(len(s)):
        t = a.cut(s[i])
        if len(t)==0:
            continue
        if t[0][1] == "m":
            # print(s[i])
            t = change(s[i])
            if i<len(s)-1 and "年" in s[i+1]:
                if t>50 and t<100:
                    return t
                if t>1900 and t<2000:
                    return t-1900

            if i<len(s)-1 and "后" in s[i+1]:
                if t>50 and t<100:
                    return t
                if t>1900 and t<2000:
                    return t-1900

            if i<len(s)-1 and "岁" in s[i+1]:
                if t<50:
                    return 117-t

            if i>0 and "龄" in s[i-1]:
                if t<50:
                    return 117-t
    return tmp


def findYear2(s,age):
    tmp = 0
    for i in range(len(s)):
        t = a.cut(s[i])
        if len(t)==0:
            continue
        if t[0][1] == "m":
            # print(s[i])
            t = change(s[i])
            if t > 1900 and t < 2000:
                t-=1900

            for j in range(i+1,min(i+4,len(s))):
                if("后" in s[j]):
                    if t > 50 and t < 100:
                        return str(t)+"-"

                if("前" in s[j]):
                    if t > 50 and t < 100:
                        return "-"+str(t)

            if i<len(s)-1 and "年" in s[i+1] and t > 50 and t < 100:
                return str(t)+"-"+str(t)

            if i < len(s) - 2 and ("-" in s[i+1] or "~" in s[i+1] or "至" in s[i+1] or "到" in s[i+1]):
                t2=change(s[i+2])
                if t2 > 1900 and t2 < 2000:
                    t2 -= 1900
                if t>50 and t<100 and t2>50 and t2<100:
                    return str(min(t,t2))+"-"+str(max(t,t2))
                if t2<20 and age!=0:
                    for j in range(max(0,i-3),i):
                        if "大" in s[j] or "长" in s[j]:
                            return str(age-t2)+"-"+str(age-t)
                    for j in range(max(0,i-3),i):
                        if "小" in s[j]:
                            return str(min(age+t,99))+"-"+str(min(age+t2,99))
            if age!=0:
                for j in range(max(0, i - 3), i):
                    if "大" in s[j]:
                        return str(age - t) + "-"+str(age)
                    if "小" in s[j]:
                        return str(age)+"-" + str(age + t)
                    if "差" in s[j]:
                        return str(age-t)+"-"+str(min(age+t,99))
    return tmp

def checkDoctor(s):
    for i in range(len(s)):
        if "博士" in s[i] or "直博" in s[i]:
            return True
        if "博" in s[i]:
            if "一" in s[i] or "二" in s[i] or "三" in s[i] or "四" in s[i] or "五" in s[i] or "后" in s[i]:
                return True
            for j in range(max(0,i-2),i):
                t = a.cut(s[i])
                if len(t) == 0:
                    continue
                if t[0][1] == "m":
                    return True
    return False

def checkMaster(s):
    for i in range(len(s)):
        if "硕士" in s[i] or "研究生" in s[i] or "保研" in s[i]:
            return True
        if "研" in s[i] or "硕" in s[i]:
            if "一" in s[i] or "二" in s[i] or "三" in s[i]:
                return True
            for j in range(max(0,i-2),i):
                t = a.cut(s[i])
                if len(t) == 0:
                    continue
                if t[0][1] == "m":
                    return True
    return False

def checkBachelor(s):
    for i in range(len(s)):
        if "本科" in s[i]:
            return True
        if "本" in s[i]:
            for j in range(max(0,i-2),i):
                t = a.cut(s[i])
                if len(t) == 0:
                    continue
                if t[0][1] == "m":
                    return True
        if "大" in s[i]:
            if "一" in s[i] or "二" in s[i] or "三" in s[i]:
                return True
    return False

def check985(s):
    for i in range(len(s)):
        t=change(s[i])
        if t==985:
            return True
    return False

def check211(s):
    for i in range(len(s)):
        t=change(s[i])
        if t==211:
            return True
    return False

def findEducation(s):
    edu=""
    if checkDoctor(s):
        edu="博士"
    elif checkMaster(s):
        edu="硕士"
    elif checkBachelor(s):
        edu="本科"
    else:
        return 0

    if check985(s):
        return "985"+edu
    elif check211(s):
        return "211"+edu
    else:
        return edu

def findInfo(s,age):
    dict={}
    height=findHeight(s)
    if height!=0:
        dict["height"]=height
    weight=findWeight(s)
    if weight!=0:
        dict["weight"]=weight
    education=findEducation(s)
    if education!=0:
        dict["education"]=education
    if age==-1:
        year=findYear1(s)
    else:
        year=findYear2(s,age)
    if year!=0:
        dict["year"]=year
    return dict

def findMail(s):
    #print(s)
    pattern=re.compile('[0-9a-zA-Z]\w*([-.]\w+)*@[0-9a-zA-Z]+([-.][0-9a-zA-Z]+)*\.[a-zA-Z]+')
    t=pattern.search(s)
    #print(t)
    if t==None:
        return t
    return t.group()

male=0
female=0
maleHeight1=[]
maleWeight1=[]
maleHeight2=[]
maleWeight2=[]
maleYear=[]

femaleHeight1=[]
femaleWeight1=[]
femaleHeight2=[]
femaleWeight2=[]
femaleYear=[]

def printInfo(sex,mail,threadid,dict1,dict2,title,content):
    global male,female
    path=""
    if sex=="M":
        male=male+1
        path="./Information/for male/"+str(male)
    else:
        female=female+1
        path = "./Information/for female/" + str(female)

    if not os.path.exists(path):
        os.makedirs(path)
    pic="./pic/"
    listfile = os.listdir(pic)
    for file in listfile:
        if threadid in file:
            #print("666")
            shutil.copy(pic+file,path)

    fp=open(path+"/基本信息.txt","w", encoding = "utf-8")

    fp.write("自我介绍：\r\n")

    fp.write("身高：")
    if "height" in dict1:
        if sex=="M":
            femaleHeight1.append(dict1["height"])
        else:
            maleHeight1.append(dict1["height"])
        fp.write(str(dict1["height"]))
    fp.write("\r\n")

    fp.write("体重：")
    if "weight" in dict1:
        if sex=="M":
            femaleWeight1.append(dict1["weight"])
        else:
            maleWeight1.append(dict1["weight"])
        fp.write(str(dict1["weight"]))
    fp.write("\r\n")

    fp.write("出生年份：")
    if "year" in dict1:
        if sex=="M":
            femaleYear.append(dict1["year"])
        else:
            maleYear.append(dict1["year"])
        fp.write(str(dict1["year"]))
    fp.write("\r\n")

    fp.write("学历：")
    if "education" in dict1:
        fp.write(dict1["education"])
    fp.write("\r\n")

    fp.write("邮箱：")
    if mail!=None :
        print(mail)
        fp.write(mail)
    fp.write("\r\n\r\n")

    fp.write("要求：\r\n")

    fp.write("身高：")
    if "height" in dict2:
        if sex=="M":
            femaleHeight2.append(dict2["height"])
        else:
            maleHeight2.append(dict2["height"])
        fp.write(str(dict2["height"]))
    fp.write("\r\n")

    fp.write("体重：")
    if "weight" in dict2:
        if sex=="M":
            femaleWeight2.append(dict2["weight"])
        else:
            maleWeight2.append(dict2["weight"])
        fp.write(str(dict2["weight"]))
    fp.write("\r\n")

    fp.write("出生年份：")
    if "year" in dict2:
        fp.write(str(dict2["year"]))
    fp.write("\r\n")

    fp.write("学历：")
    if "education" in dict2:
        fp.write(dict2["education"])
    fp.write("\r\n")

    fp.write("\r\n")

    fp.write("原标题 : ")
    fp.write(title + "\r\n")

    fp.write("原内容 : ")
    fp.write(content + "\r\n")

    fp.close()

def average(s):
    sum=0
    for t in s:
        sum=sum+t
    if len(s)==0:
        return "0"
    return str("%.1f"%(sum/len(s)))

def printTot():
    global male,female
    fp=open("./Information/总体情况.txt","w")

    fp.write("征友的的男生总数：")
    fp.write(str(male))
    fp.write("\r\n")

    fp.write("征友的的男生平均身高：")
    fp.write(average(maleHeight1))
    fp.write("\r\n")

    fp.write("征友的的男生平均体重：")
    fp.write(average(maleWeight1))
    fp.write("\r\n")

    fp.write("征友的的男生平均出生年份：")
    fp.write(average(maleYear))
    fp.write("\r\n")

    fp.write("征友的的男生对女生要求的平均身高：")
    fp.write(average(maleHeight2))
    fp.write("\r\n")

    fp.write("征友的的男生对女生要求的平均体重：")
    fp.write(average(maleWeight2))
    fp.write("\r\n")
    fp.write("\r\n")

    fp.write("征友的的女生总数：")
    fp.write(str(female))
    fp.write("\r\n")

    fp.write("征友的的女生平均身高：")
    fp.write(average(femaleHeight1))
    fp.write("\r\n")

    fp.write("征友的的女生平均体重：")
    fp.write(average(femaleWeight1))
    fp.write("\r\n")

    fp.write("征友的的女生平均出生年份：")
    fp.write(average(femaleYear))
    fp.write("\r\n")

    fp.write("征友的的女生对男生要求的平均身高：")
    fp.write(average(femaleHeight2))
    fp.write("\r\n")

    fp.write("征友的的女生对男生要求的平均体重：")
    fp.write(average(femaleWeight2))
    fp.write("\r\n")
    fp.write("\r\n")

f=open("content.txt","r",encoding="utf-8")
sys.stdin=f
for i in range(200):
    print(i+1)
    title=input()
    thread = input()
    threadid=thread[len(thread)-8:len(thread)-1]
    title = input()
    title = input()
    #print("***"+title)
    content=input()
    content = input()
    mail=findMail(content)
    #print("***"+content)
    s=input()
    s=list(jieba.cut(title))
    sex=findSex(s)
    if sex=="N":
        print("No sex")
        continue
    print(sex)
    s=list(jieba.cut(content))
    p=findTurning(s)
    if p==len(s):
        print("No turning")
        continue
    dict1=findInfo(s[0:p],-1)
    print(dict1)
    if "year" in dict1:
        dict2 = findInfo(s[p + 1:], dict1["year"])
    else:
        dict2 = findInfo(s[p + 1:], 0)
    print(dict2)
    printInfo(sex,mail,threadid,dict1,dict2,title,content)
    #os.system("pause")
printTot()
