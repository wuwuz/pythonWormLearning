# -*- coding : UTF-8 -*-
import urllib.request
import http.cookiejar
import requests
import re
import sys
from collections import deque
from bs4 import BeautifulSoup


head = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}

#filein = open('data.in', 'r')
fileout = open('href.txt', 'w', encoding = "utf-8")
#sys.stdin = filein
#sys.stdout = fileout

url = "https://bdwm.net/v2/"

dataout = open("content.txt", "a", encoding = "utf-8")

cnt = 0

for pagenum in range(1, 130 + 1) : 
    print("now pagenum = ", pagenum, "\n")
    que = deque()
    par = {"bid" : 167, "mode" : "topic", "page" : str(pagenum)}
    try : 
        r = requests.get(url + "thread.php", params = par, headers = head, timeout = 20)
    except Exception as e: 
        print("fail to open page : ", r.url, '\n')
        continue
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    for link in soup.find_all('a') : 
        t = link.get("href")
        if (t != None) and (re.search(r'threadid=\d+$', t) != None) : 
            que.append(t)
    
    for href in que : 
        print("now thread =" + href +  "\n");
        try : 
            sb = requests.get(url + href, headers = head, timeout = 20)
            sb.encoding = "utf-8"
            soup = BeautifulSoup(sb.text, "html.parser")
            cnt += 1
            dataout.write("num = ")
            dataout.write(str(cnt))
            dataout.write("\n")
            dataout.write("thread = ")
            dataout.write(sb.url)
            dataout.write("\n")
            dataout.write("title = \n")
            dataout.write(soup.title.string)
            dataout.write("\n")

            dataout.write("content = \n")
            for tex in soup.find_all(attrs = {"class" : "body file-read image-click-view"}) : 
                dataout.write(tex.text)
                break
            dataout.write("\n\n")
    
        except Exception as e : 
            print(e)
            print("fail to open thread : ", url + href, '\n')
    
#print(soup.prettify())

#tag = soup.find_all(a)
#print(type(tag))
#print(tag)
'''
for link in soup.find_all('a') :
    print(link)

with open("mytest.txt", "wb") as fd : 
    for chunk in r.iter_content() : 
        fd.write(chunk) 

#r = requests.get("https://baidu.com")

print(r.url)

print(r.cookies)
'''


