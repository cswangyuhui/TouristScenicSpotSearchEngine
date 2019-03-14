# -*- coding:utf-8 -*-
import jieba
import sys
import MySQLdb
import re
import words
import numpy as np
#cursor = db.cursor()

class Site:
    def __init__(self, name, privince,city,grade,position,time,
                 price,type,info,href):
        self.name = name
        self.province = privince
        self.city = city
        self.grade = grade
        self.postion = position
        self.time = time
        self.price = price
        self.type = type
        self.info = info
        self.href = href

    def displaySite(self):
        print
        print "景点名称 : "+self.name.strip('\n')
        print "所在省市 : "+self.province+" "+self.city.strip('\n')
        if self.grade == 0:
            print "景点星级 : 暂无"
        else:
            print "景点星级 : "+str(self.grade).strip('\n')
        print "景点位置 : "+self.postion.strip('\n')
        print "开放时间 : "+self.time.strip('\n')
        print "门票价格 : "+self.price.strip('\n')
        print "景点类型 : "+self.type.strip('\n')
        print "景点简介 : "+self.info.strip('\n')
        print "景点详情地址 : "+self.href.strip('\n')

    def getTypeList(self):
        return list(set(self.type.strip('\n').split(" ")))


def searchDouments(msg,table,cursor):
    sql = ""
    temp_weight = 0
    if msg.find("免费") != -1:
        msg = re.sub(ur'免费', '', unicode(msg, 'utf-8'))
        if msg.find("5星级") != -1 or msg.find("五星级") != -1:
            sql = "select * from %s where FREE = 1 and GRADE = %d" % (table, 5)
            msg = re.sub(ur'5星级|五星级', '', unicode(msg, 'utf-8'))
        elif msg.find("4星级") != -1 or msg.find("四星级") != -1:
            sql = "select * from %s where FREE = 1 and GRADE = %d" % (table, 4)
            msg = re.sub(ur'4星级|四星级', '', unicode(msg, 'utf-8'))
        elif msg.find("3星级") != -1 or msg.find("三星级") != -1:
            sql = "select * from %s where FREE = 1 and GRADE = %d" % (table, 3)
            msg = re.sub(ur'3星级|三星级', '', unicode(msg, 'utf-8'))
        elif msg.find("2星级") != -1 or msg.find("二星级") != -1:
            sql = "select * from %s where FREE = 1 and GRADE = %d" % (table, 2)
            msg = re.sub(ur'2星级|二星级', '', unicode(msg, 'utf-8'))
        elif msg.find("1星级") != -1 or msg.find("一星级") != -1:
            sql = "select * from %s where FREE = 1 and GRADE = %d" % (table, 1)
            msg = re.sub(ur'1星级|一星级', '', unicode(msg, 'utf-8'))
        else:
            sql = "select * from %s where FREE = 1" % (table)
    else:
        if msg.find("5星级") != -1 or msg.find("五星级") != -1:
            sql = "select * from %s where GRADE = %d" % (table, 5)
            msg = re.sub(ur'5星级|五星级', '', msg)
        elif msg.find("4星级") != -1 or msg.find("四星级") != -1:
            sql = "select * from %s where GRADE = %d" % (table, 4)
            msg = re.sub(ur'4星级|四星级', '', unicode(msg, 'utf-8'))
        elif msg.find("3星级") != -1 or msg.find("三星级") != -1:
            sql = "select * from %s where GRADE = %d" % (table, 3)
            msg = re.sub(ur'3星级|三星级', '', unicode(msg, 'utf-8'))
        elif msg.find("2星级") != -1 or msg.find("二星级") != -1:
            sql = "select * from %s where GRADE = %d" % (table, 2)
            msg = re.sub(ur'2星级|二星级', '', unicode(msg, 'utf-8'))
        elif msg.find("1星级") != -1 or msg.find("一星级") != -1:
            sql = "select * from %s where GRADE = %d" % (table, 1)
            msg = re.sub(ur'1星级|一星级', '', unicode(msg, 'utf-8'))
        else:
            sql = "select * from %s" % (table)
    sql,temp_weight = getLocation(sql, table, msg,cursor)
    print "sql语句是:",sql
    return sql, msg,temp_weight

def getLocation(sql,table,msg,cursor):
    cursor.execute("select CITY from province")
    results = cursor.fetchall()
    weight = 0
    for result in results:
        if msg.find(result[0]) != -1:
            weight = 2
            if sql.find("where") != -1:
                sql = sql + " and CITY like '%"+result[0]+"%'"
            else:
                sql = sql + " where CITY like '%"+result[0]+"%'"
    return sql,weight

def getRetrievalResults(msg):
        db = MySQLdb.connect("localhost", "root", "201071", "TRAVELDB", charset='utf8')
        cursor = db.cursor()
        tables = {'北京': 'beijing', '天津': 'tianjing', '河北': 'hebei', '内蒙古': 'neimenggu', '山西': 'shanxi',
                  '香港': 'xianggang', '陕西': 'shanxi2', '黑龙江':'heilongjiang','海南':'hainan','福建':'fujian', \
                  '河南':'henan','江西':'jiangxi','山东':'shandong','宁夏':'ningxia','甘肃':'gansu','云南':'yunnan', \
                  '辽宁':'liaoning','浙江':'zhejiang','新疆':'xinjiang','四川':'sichuan', '安徽':'anhui','广东':'guangdong', \
                  '贵州':'guizhou','广西':'guangxi','湖北':'hubei','江苏':'jiangsu','吉林':'jiling','湖南':'hunan', \
                  '澳门': 'aomen', '台湾': 'taiwan', '重庆': 'chongqing', '上海': 'shanghai','西藏':'xizang','青海':'qinghai'}
        flag = False
        findLoc = False
        returnList = []
        for table in tables:
            temp_msg = msg
            print(table)
            if msg.find(table) != -1:
                solDetails = []
                solSites = []
                solWeights = []
                #try:
                sql,msg,temp_weight = searchDouments(msg, tables[table], cursor)
                cursor.execute(sql)
                # 获取所有记录列表
                results = cursor.fetchall()
                print '数据库检索记录数是:', len(results)
                databaseFetchCount = 0
                if sql.find("where") != -1:
                    databaseFetchCount = len(results)
                print '数据库检索记录数是:', len(results)
                resultCount = 0
                print("change_"+msg)
                msg = re.sub(re.compile(ur'%s' % table), "", msg)
                print("change_" + msg)
                for result in results:
                    site = Site(result[1], result[2], result[3], result[4], result[5],
                                result[6], result[7], result[8], result[9], result[10])
                    solSites.append(site)
                    typeLists = site.getTypeList()
                    baseWeight = temp_weight
                    for typeList in typeLists:
                        if msg.find(typeList) != -1:
                            baseWeight += 1
                    solWeights.append(baseWeight)
                    # site.displaySite()
                    if len(msg) > 0:
                        cursor.execute("select DETAIL from %s where ID = %d" % (tables[table] + "_detail", result[0]))
                        solDetails.append(cursor.fetchone()[0])
                    else:
                        tempDict = {}
                        tempDict['name'] = site.name.strip('\n')
                        tempDict['loc'] = site.province.strip('\n') + " " + site.city.strip('\n')
                        if site.grade == 0:
                            tempDict['grade'] = '暂无'
                        else:
                            tempDict['grade'] = str(site.grade).strip('\n')
                        tempDict['position'] = site.postion.strip('\n')
                        tempDict['time'] = site.time.strip('\n')
                        tempDict['price'] = site.price.strip('\n')
                        tempDict['type'] = site.type.strip('\n')
                        tempDict['info'] = site.info.strip('\n')
                        tempDict['href'] = site.href.strip('\n')
                        tempDict['weight'] = baseWeight
                        returnList.append(tempDict)
                        resultCount += 1
                if len(msg) > 0:
                    myWords, myWeighs = words.get_Weight(solDetails, words.fenci(msg))
                    queryWeights = words.get_Words_Main(myWeighs)
                    # print("***queryWeight***:", len(queryWeights), "***solWeights***:", len(solWeights))
                    for i, queryWeight in enumerate(queryWeights):
                        solWeights[i] += queryWeight
                    for i in range(len(solWeights)):
                        if solWeights[i] <= 0.11 and databaseFetchCount == 0:
                            continue
                        if np.isnan(solWeights[i]):
                            continue
                        solSites[i].displaySite()

                        tempDict = {}
                        tempDict['name'] = solSites[i].name.strip('\n')
                        tempDict['loc'] = solSites[i].province.strip('\n') + " " + solSites[i].city.strip('\n')
                        if solSites[i].grade == 0:
                            tempDict['grade'] = '暂无'
                        else:
                            tempDict['grade'] = str(solSites[i].grade).strip('\n')
                        tempDict['position'] = solSites[i].postion.strip('\n')
                        tempDict['time'] = solSites[i].time.strip('\n')
                        tempDict['price'] = solSites[i].price.strip('\n')
                        tempDict['type'] = solSites[i].type.strip('\n')
                        tempDict['info'] = solSites[i].info.strip('\n')
                        tempDict['href'] = solSites[i].href.strip('\n')
                        tempDict['weight'] = solWeights[i]
                        returnList.append(tempDict)
                        resultCount += 1
                if resultCount > 0:
                    print('-' * 5)
                    print table, "搜索得到的结果数:", resultCount
                    print('-' * 5)
                # except:
                #     print("错误发生，请重试")
                #     flag = False
                flag = True
                findLoc = True
                del solDetails
                del solSites
                del solWeights
            msg = temp_msg
        if flag == False:
            for table in tables:
                temp = msg
                if msg.find("直辖市") != -1 and table != '北京' and table != '天津' and table != '重庆' and table != '上海':
                    continue
                if msg.find("港澳台") != -1 and table != '香港' and table != '澳门' and table != '台湾':
                    continue
                solDetails = []
                solSites = []
                solWeights = []
                #try:
                sql, msg, temp_weight = searchDouments(msg, tables[table], cursor)
                cursor.execute(sql)
                # 获取所有记录列表
                results = cursor.fetchall()
                print '数据库检索记录数是:', len(results)
                databaseFetchCount = 0
                if sql.find("where") != -1:
                    databaseFetchCount = len(results)
                print '数据库检索记录数是:', len(results)
                for result in results:
                    site = Site(result[1], result[2], result[3], result[4], result[5],
                                result[6], result[7], result[8], result[9], result[10])
                    solSites.append(site)
                    typeLists = site.getTypeList()
                    baseWeight = temp_weight
                    for typeList in typeLists:
                        if msg.find(typeList) != -1:
                            baseWeight += 1
                    solWeights.append(baseWeight)
                    # site.displaySite()
                    cursor.execute("select DETAIL from %s where ID = %d" % (tables[table] + "_detail", result[0]))
                    solDetails.append(cursor.fetchone()[0])

                myWords, myWeighs = words.get_Weight(solDetails, words.fenci(msg))
                queryWeights = words.get_Words_Main(myWeighs)
                # print("***queryWeight***:", len(queryWeights), "***solWeights***:", len(solWeights))
                for i, queryWeight in enumerate(queryWeights):
                    solWeights[i] += queryWeight
                resultCount = 0
                for i in range(len(solWeights)):
                    if solWeights[i] <= 0.11 or databaseFetchCount == 0:
                        continue
                    if np.isnan(solWeights[i]):
                        continue
                    else:
                        solSites[i].displaySite()

                        tempDict = {}
                        tempDict['name'] = solSites[i].name.strip('\n')
                        tempDict['loc'] = solSites[i].province.strip('\n') + " " + solSites[i].city.strip('\n')
                        if solSites[i].grade == 0:
                            tempDict['grade'] = '暂无'
                        else:
                            tempDict['grade'] = str(solSites[i].grade).strip('\n')
                        tempDict['position'] = solSites[i].postion.strip('\n')
                        tempDict['time'] = solSites[i].time.strip('\n')
                        tempDict['price'] = solSites[i].price.strip('\n')
                        tempDict['type'] = solSites[i].type.strip('\n')
                        tempDict['info'] = solSites[i].info.strip('\n')
                        tempDict['href'] = solSites[i].href.strip('\n')
                        tempDict['weight'] = solWeights[i]
                        returnList.append(tempDict)

                        resultCount += 1
                if resultCount > 0:
                    print('-' * 5)
                    print table, "搜索得到的结果数:", resultCount
                    print('-' * 5)
                # except:
                #     print("错误发生，请重试")
                #     flag = False
                #     break
                del solDetails
                del solSites
                del solWeights
                msg = temp
        cursor.close()
        db.close()
        returnList.sort(key=lambda obj: obj.get('weight'), reverse=True)
        if findLoc == True:
            return returnList
        elif len(returnList) <= 200:
            return  returnList
        else:
            return returnList[0:200]
    #keywords = jieba.analyse.extract_tags(msg, allowPOS=('ns', 'n', 'vn', 'v', 'nr', 'i', 'j', 'l', 'nt'))