# 北京邮电大学暑期课程信息检索与信息抽取课程设计
<br><br>
## 文件介绍
<br>

|文件名|作用|
|:---|:---|
| \_\_init\_\_.py|flask程序入口|
|algorithm.py|信息检索与抽取算法1|
|algorithm2.py|信息检索与抽取算法2|
|words.py|算法1用到的向量空间模型计算方法|
|name.py|命名实体识别|
|static文件夹|css,image,js文件|
|template文件夹|html文件|
|introduction/china.zip|网络爬虫得到的保存着中国所有景点信息的TXT文件|
|introduction/TRAVELDB.sql.zip|数据库建表sql文件|
|introduction/IR-IE.docx|实验报告|
|introduction/stopwords.txt|停用词表|

## 说明
<br>

默认使用的是算法2，要改为算法1，请将 *\_\_init\_\_.py* 文件中的 *import algorithm2 as ag* 改为
*import algorithm as ag*， <br>
并在words.py中设置 *mystopwords = stopwordslist(stopwords.txt文件路径)*。 <br>
introduction/china.zip解压缩后的 *景点名.txt* 文件是该景点的总介绍，*景点名_detail.txt* 文件是该景点详细文字介绍的 <br>
分词结果。 <br>
<div align=center><img width="480" height="360" src="https://github.com/cswangyuhui/TouristScenicSpotSearchEngine/blob/master/introduction/plot.png"/></div>
<br>
<div align=center><img width="480" height="360" src="https://github.com/cswangyuhui/TouristScenicSpotSearchEngine/blob/master/introduction/plot_detail.png"/></div>

## 程序运行截图
<br>

### 主界面
<br>
<div align=center><img width="580" height="360" src="https://github.com/cswangyuhui/TouristScenicSpotSearchEngine/blob/master/introduction/1.png"/></div>

### 搜索框输入历史悠久的红色旅游景点
<br>
<div align=center><img width="580" height="360" src="https://github.com/cswangyuhui/TouristScenicSpotSearchEngine/blob/master/introduction/2.png"/></div>
<div align=center><img width="580" height="360" src="https://github.com/cswangyuhui/TouristScenicSpotSearchEngine/blob/master/introduction/3.png"/></div>

### 搜索框输入令人心旷神怡的地方
<br>
<div align=center><img width="580" height="360" src="https://github.com/cswangyuhui/TouristScenicSpotSearchEngine/blob/master/introduction/4.png"/></div>
<div align=center><img width="580" height="360" src="https://github.com/cswangyuhui/TouristScenicSpotSearchEngine/blob/master/introduction/5.png"/></div>

### 搜索框输入江西革命圣地
<br>
<div align=center><img width="580" height="360" src="https://github.com/cswangyuhui/TouristScenicSpotSearchEngine/blob/master/introduction/6.png"/></div>
<div align=center><img width="580" height="360" src="https://github.com/cswangyuhui/TouristScenicSpotSearchEngine/blob/master/introduction/7.png"/></div>
