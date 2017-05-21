#coding:utf-8
from os import path
from scipy.misc import imread
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

freq = {}
with open("dict.txt", "r", encoding = "utf-8") as f : 
    for line in f : 
        [word, times] = line.split()
        freq[word] = int(times)
    f.close()
back_coloring = imread("center.jpg")
wc = WordCloud(
        font_path="msyh.ttc",
        background_color='white',
        mask=back_coloring,
        max_words=1000,
        max_font_size=50)
wc.generate_from_frequencies(freq)
image_colors = ImageColorGenerator(back_coloring)  

plt.figure()  
wc = wc.recolor(color_func=image_colors)
plt.imshow(wc)
plt.axis("off")  
plt.show()  
  
#wc.to_file(path.join(d, "pic_gen.png"))  
wc.to_file("pic_gen.png")

