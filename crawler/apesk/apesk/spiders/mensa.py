# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import Request

from apesk.items import AdvantageScoreItem
from apesk.settings import TAILOFFSET, HEADOFFSET, SEARCH_URL_FORMAT, TASKID, SEARCH_HEADERS


class MensaSpider(scrapy.Spider):
    name = 'mensa'
    # allowed_domains = ['mensa.com']

    def start_requests(self):
        self.logger.debug('初始请求:'.format(self.head_offset))
        self.logger.debug('初始请求:'.format(self.tail_offset))
        for i in range(self.head_offset, self.tail_offset):

            yield Request(
                headers=SEARCH_HEADERS,
                cb_kwargs={
                    'task_id': TASKID,
                },
                dont_filter=True,
                callback=self.parse,
                url=SEARCH_URL_FORMAT.format(i),
            )

    def parse(self, response, **kwargs):
        # 获得id与姓名
        id = response.url.split("id=")[-1]
        name, submit_time = response.xpath("//div[@class='r'][1]//div").xpath('string(.)').extract()
        name, submit_time = name.split(":")[-1], re.search(':.*', submit_time).group(0)[1:]
        self.logger.info("id:{0},name:{1},submit_time:{2}".format(id, name, submit_time))
        # 解析原始得分表
        for line in response.xpath("//table[@style='border:1px solid #bbb'][1]//tr"):
            line_list = line.xpath("td").xpath("string(.)").extract()
            if len(line_list) == 6:
                if line_list[0] != '编号':
                    item1, item2 = AdvantageScoreItem(), AdvantageScoreItem()

                    item1['id'], item1['name'], item1['submit_time'], item1['advantage_id'], item1['advantage_name'], item1['score'] \
                        = [id, name, submit_time] + line_list[0:3]
                    # self.logger.debug(item1)
                    yield item1

                    item2['id'], item2['name'], item2['submit_time'], item2['advantage_id'], item2['advantage_name'], item2['score'] \
                        = [id, name, submit_time] + line_list[3:6]
                    # self.logger.debug(item2)
                    yield item2

                else:
                    self.logger.debug('原始得分表 行首')
            else:
                self.logger.error('原始得分表 表格列数不等于 6')
                raise Exception
            pass

        pass

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        cls.head_offset = HEADOFFSET
        cls.tail_offset = TAILOFFSET
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)
        return spider
