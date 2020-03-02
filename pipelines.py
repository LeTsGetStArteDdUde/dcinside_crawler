# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from __future__ import unicode_literals
import time
import logging
import sys
import mysql.connector
from mysql.connector import errorcode
#import MySQLdb
#import MySQLdb.cursors
#from sshtunnel import SSHTunnelForwarder
from scrapy.exceptions import DropItem

class CrawlerJijinPipeline(object):
    def __init__(self):
        try:
            #server = SSHTunnelForwarder(
            #    'ec2-52-78-171-7.ap-northeast-2.compute.amazonaws.com',
            #    ssh_username="root",
            #    ssh_password="root",
            #    remote_bind_address=('192.168.0.1', 22)
            #)
            #server.start()
            self.conn = mysql.connector.connect(user='root', password='root', database='crawling', host='192.168.0.1', port=3306)
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as e:
            print(e)
            sys.exit(1)

    def process_item(self, item, spider):
        self.cursor.execute("SELECT * FROM crawling.dcinsidejijin")
        now = time.localtime()
        d_crawl_date = "%04d-%02d-%02d %02d:%02d:%02d" % (
        now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        item_temp = []
        result = []
        result = self.cursor.fetchall()
        for x in range(0, 30):
            for i in range(0, len(result)):
                if result[i][0] == item['no'][x] and result[i][2] == item['writer'][x]:
                    try:
                        item_temp.append(x)
                        self.cursor.execute(
                            "UPDATE crawling.dcinsidejijin SET d_title = %s, d_date = %s, d_writer = %s, d_crawl_date = %s WHERE d_no = %s and d_writer = %s",
                            (item['title'][x].encode('utf-8'),
                             item['date'][x].encode('utf-8'),
                             item['writer'][x].encode('utf-8'),
                             d_crawl_date,
                             item['no'][x].encode('utf-8'),
                             item['writer'][x].encode('utf-8')))
                        self.conn.commit()
                        break
                    except mysql.connector.Error as e:
                        print(e)
        s1 = set(item_temp)
        s2 = set([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29])
        s3 = s2 - s1
        item_for_insert = list(s3)
        for i in range(0, len(item_for_insert)):
            try:
                self.cursor.execute(
                    "INSERT INTO crawling.dcinsidejijin (d_no, d_title, d_writer, d_date, d_link, d_crawl_date) VALUES (%s, %s, %s, %s, %s, %s)",
                    (item['no'][item_for_insert[i]].encode('utf-8'),
                    item['title'][item_for_insert[i]].encode('utf-8'),
                    item['writer'][item_for_insert[i]].encode('utf-8'),
                    item['date'][item_for_insert[i]].encode('utf-8'),
                    "http://gall.dcinside.com" + item['link'][item_for_insert[i]].encode('utf-8'),
                    d_crawl_date))
                self.conn.commit()
            except mysql.connector.Error as e:
                print(e)
                


