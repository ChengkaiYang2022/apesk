# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

from apesk.exceptions import SQLMapperException
from apesk.items import AdvantageScoreItem, AdvantageItem


class ApeskPipeline:
    def process_item(self, item, spider):
        return item


class MysqlPipeline:

    collection_name = 'scrapy_items'

    def __init__(self, mysql_uri, mysql_db, mysql_username, mysql_password):
        self.mysql_uri = mysql_uri
        self.mysql_db = mysql_db
        self.mysql_username = mysql_username
        self.mysql_password = mysql_password
        # TODO 使用orm
        self.sql_mapper = {
            AdvantageItem.__name__: "replace into advantage_item (advantage_name, advantage_desc, "
                                     "advantage_desc_more_info) value({advantage_name},{advantage_desc},"
                                     "{advantage_desc_more_info});",
            AdvantageScoreItem.__name__: "replace into advantage_score_item(id, name, submit_time, advantage_id,"
                                " advantage_name, score) value "
                                "({id},'{name}','{submit_time}',{advantage_id},'{advantage_name}',{score});",
        }

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_uri=crawler.settings.get('MYSQL_URI'),
            mysql_db=crawler.settings.get('MYSQL_DB'),
            mysql_username=crawler.settings.get('MYSQL_USERNAME'),
            mysql_password=crawler.settings.get('MYSQL_PASSWORD'),
        )

    def open_spider(self, spider):

        self.db = pymysql.connect(self.mysql_uri, self.mysql_username, self.mysql_password, self.mysql_db, charset='utf8')
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()

    def process_item(self, item, spider):
        sql = self.sql_mapper.get(item.__class__.__name__)
        if not sql:
            raise SQLMapperException
        sql = sql.format(**dict(item))
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Commit your changes in the database
            self.db.commit()
        except Exception as e:
            # Rollback in case there is any error
            self.db.rollback()

        return item