# dessert
这个工程会用来存放一些常用的python脚本

## 生活服务类

##### 1. bridge/query_bus.py

   用来获取指定城市的所有公交站的信息，结果会保存在一个CSV文件中，依赖百度apistore中的api,需要用户提供apikey，免费。在使用时，用户需要指定城市名称和所有的公交线路。

## 实用工具类
##### 1. knife/DataBase.py

   用来连接mysql数据库，并执行sql语句，同时也提供了字符串匹配的方式修改mysql的建表语句为阿里云ODPS的建表语句


## 机器学习类
##### 1. machinelearning/NLP/WordFreq.py
	
   从数据库中读取信息之后使用jieba进行分词，然后统计词频的python脚本，dict.txt是自定义词典，stopword.txt是停词词典。
