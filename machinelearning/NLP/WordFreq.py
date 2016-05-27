#!/usr/local/bin/python
# coding:utf-8

import jieba
import jieba.analyse
import DataBase

jieba.load_userdict("dict.txt")
class Tags:
    def __init__(self):
        self.cn_stopword =[]
        fd = file("stopwords.txt", "r")
        for line in fd.readlines():
            self.cn_stopword.append(line.replace("\n", ""))
        self.db = DataBase.Operator()

    def get_word_freq(self, filed):
        alldata = self.db.get_all_data_by_filed(filed);
        result ={}
        for data in alldata:
            seg_list = jieba.cut(data[0],cut_all=False)
            for word in seg_list:
                if word.encode("utf-8") in self.cn_stopword:
                    continue
                if word in result:
                    result[word] = result[word] + 1
                else:
                    result[word] = 1
        sort_result =  sorted(result.iteritems(), key=lambda d:d[1], reverse = True)
        return sort_result

    def get_keyword(self, filed):
        alldata = self.db.get_all_data_by_filed(filed);
        result ={}
        for data in alldata:
            seg_list = jieba.analyse.extract_tags(data[0],20)
            for word in seg_list:
                if word.encode("utf-8") in self.cn_stopword:
                    continue
                if word in result:
                    result[word] = result[word] + 1
                else:
                    result[word] = 1
        sort_result =  sorted(result.iteritems(), key=lambda d:d[1], reverse = True)
        return sort_result

    def get_comb_freq(self):
        alldata = self.db.get_all_data_by_filed("title");
        result ={}
        for data in alldata:
            seg_list = jieba.cut(data[0],cut_all=False)
            for word in seg_list:
                if word.encode("utf-8") in self.cn_stopword:
                    continue
                if word in result:
                    result[word] = result[word] + 1
                else:
                    result[word] = 1
        allbodydata = self.db.get_all_data_by_filed("body");
        for data in allbodydata:
            seg_list = jieba.analyse.extract_tags(data[0],20)
            for word in seg_list:
                if word.encode("utf-8") in self.cn_stopword:
                    continue
                if word in result:
                    result[word] = result[word] + 1
                else:
                    result[word] = 1
        sort_result =  sorted(result.iteritems(), key=lambda d:d[1], reverse = True)
        return sort_result

if __name__ == '__main__':
    cixi_tag = Tags()
    sort_title = cixi_tag.get_word_freq("title")
    f = file("freq1.txt", "w")
    for x in sort_title:
        f.write(x[0].encode("utf-8")+" "+str(x[1])+"\n")
    f.close()
    f = file("demo.txt", "w")
    for x in sort_title[:200]:
        f.write(str(x[1])+" "+x[0].encode("utf-8")+"\\n")
    f.close()
    sort_body = cixi_tag.get_keyword("body")
    f = file("freq2.txt", "w")
    for x in sort_body:
        f.write(x[0].encode("utf-8")+" "+str(x[1])+"\n")
    f.close()

    keyword_list = cixi_tag.get_comb_freq()
    f = file("freq3.txt", "w")
    for x in keyword_list:
        f.write(x[0].encode("utf-8")+" "+str(x[1])+"\n")
    f.close()
