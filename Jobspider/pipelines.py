# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import csv
class JobMysqlPipeline(object):
    def open_spider(self,object):
        self.connect=pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='s19930110l',
            port=3306,
            db='u148',
            charset='utf8',
        )
        self.cursor=self.connect.cursor()
    def process_item(self, item, spider):
        sql="insert into jobs values(0,'%s','%s','%s','%s','%s','%s')"%(item['job'],item['company'],item['money'],item['location'],item['ability'],item['fuli'])
        self.cursor.execute(sql)
        self.connect.commit()
        return item
    def close_spider(self,spider):
        self.cursor.close()
        self.connect.close()
class JobCsvPipeline(object):
    def open_spider(self,spider):
        self.fileobj=open('job.csv','w',encoding='utf-8')
        self.write=csv.writer(self.fileobj)
        self.write.writerow(['job','company','money','location','ability','fuli'])
        self.item_list=[]
    def process_item(self,item,spider):
        csvitem=[]
        csvitem.append(item['job'])
        csvitem.append(item['company'])
        csvitem.append(item['money'])
        csvitem.append(item['location'])
        csvitem.append(item['ability'])
        csvitem.append(item['fuli'])
        self.item_list.append(csvitem)
    def close_spider(self,spider):
        self.write.writerows(self.item_list)
        self.fileobj.close()


