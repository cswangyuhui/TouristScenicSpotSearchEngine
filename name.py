# coding=utf-8
import requests
import os
import re
import time as tm
from bs4 import BeautifulSoup as bs
import pynlpir
import urllib

apiUrl = "http://dynamic.goubanjia.com/dynamic/get/23f2fc16fe6d6d8b88182a336d4a0e1f.html?sep=3&random=true"
def getHtml(url):
    if url is None:
        return None
    response = urllib.request.urlopen(url)
    if response.getcode() != 200:
        return None
    return response.read()

# def getHtml(url):
#     session = requests.session()
#     page = ''
#     res = urllib.urlopen(apiUrl).read().strip("\n")
#     ips = res.split("\n")
#     proxyip = 'http://' + ips[0]
#     myproxies = {}
#     myproxies['http'] = proxyip
#     t = 0
#     while page == '' and t < 15:
#         try:
#             page = session.get(url, proxies=myproxies, timeout=2).text
#         except:
#             print("extract information时读取网页出错")
#             res = urllib.urlopen(apiUrl).read().strip("\n")
#             ips = res.split("\n")
#             proxyip = 'http://' + ips[0]
#             myproxies['http'] = proxyip
#             print("the global proxyip is " + proxyip)
#             t += 1
#     return page

def getDetail(url):
    detail_html = getHtml(url)
    try:
        soup = bs(detail_html,"lxml")
        detail = re.findall(ur"简介.(.*)", re.sub(ur'\r|\n', ur'', soup.find("div", {"class": "type"}).get_text()))[
            0].encode('utf-8')
    except:
        #print("not take the detail")
        detail = ""
    print(detail)
    return detail


def getName(url):
    name = {}
    name['ns'] = []  # 地点
    name['t'] = []  # 时间
    name['nr'] = []  # 人名
    name['nt'] = []  # 机构名
    pynlpir.open(encoding='utf-8')
    #print 'pynlpir model loaded succesed'
    detail = getDetail(url)
    print(detail)
    if detail == "":
        print "can't get detail"
        return "error"
    word_pos = pynlpir.segment(detail, pos_names=None)
    for i in range(0, len(word_pos)):
        if word_pos[i][1] in name:
            name[word_pos[i][1]].append(word_pos[i][0])
    name['ns'] = list(set(name['ns']))  # 地点
    name['t'] = list(set(name['t']))  # 时间
    name['nr'] = list(set(name['nr']))  # 人名
    name['nt'] = list(set(name['nt']))  # 机构名
    place = ''
    time = ''
    human = ''
    ins = ''
    for i in range(len(name['ns'])):
        place = place + name['ns'][i] + '|'
    for i in range(len(name['t'])):
        time = time + name['t'][i] + '|'
    for i in range(len(name['nr'])):
        human = human + name['nr'][i] + '|'
    for i in range(len(name['nt'])):
        ins = ins + name['nt'][i] + '|'
    return "地名:"+place+"\n"+"时间:"+time+"\n"+"人名:"+human+"\n"+"机构名:"+ins;
    # print "place:" + place
    # print "time:" + time
    # print "human:" + human
    # print "ins:" + ins

