# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class LagouPipeline(object):
    def process_item(self, item, spider):
        return item




class mysqltwistedpipeline(object):


    def __init__(self,dbpool):
        self.dbpool = dbpool



    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DB'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )



        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)

        return cls(dbpool)


    def process_item(self, item, spider):
        querry = self.dbpool.runInteraction(self.do_insert, item)
        querry.addErrback(self.handle_error, item, spider)


    def handle_error(self,failure, item, spider):
        print(failure, item, spider)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()

        cursor.execute(insert_sql, params)
