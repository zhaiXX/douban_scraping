from urllib import request
from bs4 import BeautifulSoup as bs
import re
import jieba
import pandas as pd
import numpy
import matplotlib.pyplot as plt
import matplotlib
from wordcloud import WordCloud
import pylab


resp = request.urlopen('https://movie.douban.com/nowplaying/beijing/')
html_data = resp.read().decode('utf-8')
soup = bs(html_data,"html.parser")

soup = bs(html_data, 'html.parser')
nowplaying_movie = soup.find_all('div', id='nowplaying')
nowplaying_movie_list = nowplaying_movie[0].find_all('li', class_='list-item')

nowplaying_list = []
for item in nowplaying_movie_list:
    nowplaying_dict = {}
    nowplaying_dict['id'] = item['data-subject']
    for tag_img_item in item.find_all('img'):
        nowplaying_dict['name'] = tag_img_item['alt']
        nowplaying_list.append(nowplaying_dict)


requrl = 'https://movie.douban.com/subject/' + nowplaying_list[0]['id'] + '/comments' +'?' +'start=20&limit=20&sort=new_score&status=P'
resp = request.urlopen(requrl)
html_data = resp.read().decode('utf-8')
soup = bs(html_data, 'html.parser')
comment_div_lits = soup.find_all('div', class_='comment')

eachCommentList = []
for item in comment_div_lits:
    if item.find_all('p')[0].string is not None:
        eachCommentList.append(item.find_all('p')[0].string)

comments = ''
for k in range(len(eachCommentList)):
    comments = comments + (str(eachCommentList[k])).strip()


pattern = re.compile(r'[\u4e00-\u9fa5]+')
filterdata = re.findall(pattern, comments)
cleaned_comments = ''.join(filterdata)

segment = jieba.lcut(cleaned_comments)
words_df=pd.DataFrame({'segment':segment})

stopwords=pd.read_csv("/home/zhai/github/python3_project/douban_scraping/stopwords.txt",index_col=False,quoting=3,sep="\t",names=['stopword'], encoding='utf-8')#quoting=3全不引用
words_df=words_df[~words_df.segment.isin(stopwords.stopword)]

words_stat=words_df.groupby(by=['segment'])['segment'].agg({"计数":numpy.size})
words_stat=words_stat.reset_index().sort_values(by=["计数"],ascending=False)

print(words_stat.head())



matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)

wordcloud = WordCloud(font_path="simhei.ttf", background_color="white", max_font_size=80)  # 指定字体类型、字体大小和字体颜色
word_frequence = {x[0]: x[1] for x in words_stat.head(1000).values}
word_frequence_list = []
for key in word_frequence:
    temp = (key, word_frequence[key])
    word_frequence_list.append(temp)




wordcloud = wordcloud.fit_words(word_frequence)
wordcloud.fit_words(word_frequence)

plt.imshow(wordcloud)
pylab.show()
