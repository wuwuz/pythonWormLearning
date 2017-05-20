# -*- coding:utf-8 -*- 
import urllib.request
import http.cookiejar
import requests
import re
import sys
from collections import deque
from bs4 import BeautifulSoup

class MyThread : 
    def __init__(self, tid, title, time, repNum, url) : 
        print("added !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        self.tid = tid
        self.title = title
        self.time = time
        self.repNum = repNum
        self.url = url
    def __lt__(self, other) : 
        if (self.repNum != other.repNum) :  return self.repNum > other.repNum
        if (self.tid != other.tid) : return self.tid > other.tid
        

def getHotSpotInBoard(bid, outputFilePath, minReply = 50) : 
    head = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    cnt = 0
    que = deque()
    out = open(outputFilePath, 'w', encoding = "utf-8")
    url = "https://bdwm.net/v2/"
    pagenum = 1
    timeExceed = 0
    while (timeExceed == 0) and (pagenum <= 100) : 
        print("now pagenum = ", pagenum, "\n")
        par = {"bid" : str(bid), "mode" : "topic", "page" : str(pagenum)}

        try : 
            r = requests.get(url + "thread.php", params = par, headers = head, timeout = 15)
        except Exception as e: 
            print("fail to open page : ", r.url, '\n')
            continue
        r.encoding = "utf-8"
        soup = BeautifulSoup(r.text, "html.parser")
        for topic in soup.find_all(attrs = {"class" : "list-item-topic list-item"}) : 
            t = topic.find(attrs = {"class" : "title l limit"})
            title = t.string
            print(title)

            t = topic.find(attrs = {"class" : "reply-num l"});
            repNum = int(t.string)
            print(repNum)
            if (repNum < minReply) : 
                continue

            t = topic.find(attrs = {"class" : "link"})
            href = t.get("href")
            if (href == None) or (re.search(r"threadid=\w+$", href) == None) : 
                continue
            t = topic.find(attrs = {"class" : "time"})
            time = t.string

            tid = topic.get("data-itemid");
            
            print("add in que")
            cnt += 1
            que.append(MyThread(tid = tid, title = title, time = time, repNum = repNum, url = url + href))

        pagenum += 1

    print("cnt = ", cnt)
    sortedque = sorted(que)
    for trd in sortedque: 
        out.write("tid = ")
        out.write(trd.tid)
        out.write('\n')
        out.write("title = ")
        out.write(trd.title)
        out.write('\n')
        out.write("time = ")
        out.write(trd.time)
        out.write('\n')
        out.write("reply number = ")
        out.write(str(trd.repNum))
        out.write('\n')
        out.write("url = ")
        out.write(trd.url)
        out.write('\n\n')


print("")
print("查询板块热门帖子的python程序")
print("请输入板块id")
print("热门板块id如下")
print("三角地：22")
print("别问我是谁：414")
print("燕园食宿：1431")
bid = int(input())
print("请输入最小回复数（比如50）")
rep = int(input())
print("请输入文件名")
filename = input()
getHotSpotInBoard(bid = bid, minReply = rep, outputFilePath = "TriangleHotspot.txt", )
