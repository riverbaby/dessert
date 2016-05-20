#!/usr/local/bin/python
# coding:utf-8

import os, sys, string
import MySQLdb
import re

reload(sys)
sys.setdefaultencoding('utf8')

class Operator:
    conn = ""
    def __init__(self):
        try:
            self.conn = MySQLdb.connect(host='localhost', user='root', passwd='passwd', db='resultdb', charset='utf8')
        except Exception, e:
            print e
            sys.exit()

    def get_report_number(self, *args):
        cursor = self.conn.cursor()
        if len(args) > 1:
            sql_report = "select count(*) from newsdb where tag= %s and date >= %s and date <= %s"
        else:
            sql_report = "select count(*) from newsdb where tag= %s"
        cursor.execute(sql_report, args)
        count = cursor.fetchone()
        cursor.close()
        return count[0]

    def get_comment_number(self, *args):
        cursor = self.conn.cursor()
        sql_report = "select body from newsdb where tag= %s"
        cursor.execute(sql_report, args)
        alldata = cursor.fetchall()
        comment = 0;
        if alldata:
            for rec in alldata:
                print rec[0]
        cursor.close()

    def get_table_info(self, table):
        cursor = self.conn.cursor()
        sql_report = "show create table %s" %table
        cursor.execute(sql_report)
        alldata = cursor.fetchone()
        cursor.close()
        return alldata

    def get_all_table(self):
        cursor = self.conn.cursor()
        sql_report = "show tables"
        cursor.execute(sql_report)
        tables= cursor.fetchall()
        cursor.close()
        return tables

    def get_all_data_by_filed(self, filed):
        cursor = self.conn.cursor()
        sql_query = "select %s from newsdb where date > '2016-05-11'" % filed
        cursor.execute(sql_query)
        data = cursor.fetchall()
        cursor.close()
        return data

if __name__ == '__main__':
    event = Operator()
    # print event.get_report_number('两会','2016-03-07 11:24:45', '2016-03-07 12:00:00')
    # print event.get_comment_number('明星吸毒')
    tables = event.get_all_table()
    content = ""
    p1 = re.compile("\(\d+\)([\w| |\']+)COMMENT")
    p2 = re.compile(r",\n  PRIMARY KEY([\s\S]+)COMMENT=" )
    for table in tables:
        data = event.get_table_info(table[0])[1]
        data = data.replace("TABLE", "TABLE IF NOT EXISTS")
        # data = data.replace("(\d+)[\s\S]+COMMENT", "")
        data = p1.sub(" COMMENT", data)
        data = p2.sub("\n) COMMENT ", data)
        data = data.replace("varchar", "string")
        content += data
        content +=';\n'
    f = file("rds1.sql","w")
    f.write(content)
    f.close()
