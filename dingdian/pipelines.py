# -*- coding: utf-8 -*-
import pymysql  # 用来链接mysql的第三方库

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DingdianPipeline(object):

    def process_item(self, item, spider):
        article_title = item['article_title']  # 定义文章名称的字段
        author = item['author']  # 定义作者的字段
        content = item['content']  # 定义内容的字段
        book = item['book']  # 定义书名的字段
        # 链接mysql
        conn = pymysql.connect(host='localhost',
                               user='root',
                               port=3307,
                               passwd='123456',
                               db='scrapy_pachong',
                               charset='utf8')
        # 获取游标
        cur = conn.cursor()
        # 插入你得到的数据
        cur.execute("INSERT INTO 顶点(`作者`,`章节名称`,`书名`,`内容`) VALUES('%s','%s','%s','%s')" % (author,article_title,book,content))
        conn.commit()
        conn.close()
        return item
