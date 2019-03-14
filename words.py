# coding=utf-8

from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import jieba
import re
import os

def cosineSimilarity(x,y):
    x = np.array(x)
    y = np.array(y)
    num = float(np.sum(x*y))
    denom = np.linalg.norm(x) * np.linalg.norm(y)
    cos = num / denom
    return cos

def stopwordslist(filepath):
    f = open(filepath,'r')
    stopwords = [line.strip() for line in f.readlines()]
    f.close()
    return stopwords

# def get_Wordlist(path):
#     files = os.listdir(path.decode('utf-8'))
#     wordlist = []
#
#     for file in files:
#         # 准确获取一个txt的位置，利用字符串的拼接
#         txt_path = path + file
#
#         with open(txt_path, 'r') as fp:
#             wordlist.append(fp.read())
#
#     return wordlist


def get_Weight(wordlist,query):
    wordlist.append(query)
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(
        vectorizer.fit_transform(wordlist))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    words = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重

    return words, weight


def get_Words_Main(weight):
    resultWeights = []
    # for word in words:
    #     print word
    # print(len(words))
    for step, w in enumerate(weight):
        if step == len(weight)-1:
            break
        resultWeights.append(cosineSimilarity(w,weight[len(weight)-1]))
        # loc = np.argsort(-w)
        # # for i in range(num_top):
        # #     print u'-{}: {} {}'.format(str(i + 1), words[loc[i]], w[loc[i]])
        # # print '\n'
        # weight = 0
        # for i in range(num_top):
        #     if words[loc[i]] in query:
        #         weight += w[loc[i]]
        # resultWeights.append(weight)
    #print(resultWeights)
    return resultWeights

mystopwords = stopwordslist("/Users/wangyuhui/Desktop/IE_IR/stopwords.txt")

def fenci(msg,stopwords=mystopwords):
    seg_list = jieba.cut(msg, cut_all=True)
    result = []
    for seg in seg_list:
        seg = ''.join(seg.split())
        if (seg != '' and seg != "\n" and seg != "\r\n" and re.match(ur'\w+',seg) is None and seg not in stopwords):
            result.append(seg)
    return ' '.join(result)

# if __name__ == '__main__':
#     path = 'C:\\Users\\asuss\\Desktop\\detail\\'
#     num_top = 5
#     wordlist = get_Wordlist(path)
#     words, weight = get_Weight(wordlist)
#     get_Words_Main(words, weight, num_top)
