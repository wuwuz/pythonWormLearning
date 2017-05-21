#encoding = utf-8
import jieba
import jieba.posseg as pseg
import sys
import os

word_lst = []
word_dict = {}


#filter_lst = ["c", "f", "m", "nr", "o", "p", "r", "u", "m", "x", "t", "q"]
filter_lst = ["a", "Aa", "ad", "an", "d", "ns", "nt", "nz", "vd", "vn", "z"]


with open("content.txt", "r", encoding = "utf-8", errors = "ignore") as f : 
    cnt = 0
    while True : 
        cnt += 1
        print(cnt)
        if (cnt > 10000) : break 
        line = f.readline()
        if (line == "") : break
        for j in range(2, 7) : line = f.readline()
        words = pseg.cut(line)
        for tag in words : 
            word = tag.word
            flag = tag.flag
            if (len(word) == 1) or (flag not in filter_lst) : continue
            if (word not in word_dict) : 
                word_dict[word] = 1
            else : 
                word_dict[word] += 1
    f.close()

#sort word_dict , ordered by its frequency
word_dict = sorted(word_dict.items(), key = lambda d:d[1], reverse = True)


with open("dict.txt", "w", encoding = "utf-8") as f : 
    for word in word_dict : 
        #print(word + ' ' +  str(word_dict[word]))
        f.write(word[0] + ' ' + str(word[1]) + '\n')
    f.close()

