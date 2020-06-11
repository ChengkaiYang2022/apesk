# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

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
        pass
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        cls.head_offset = HEADOFFSET
        cls.tail_offset = TAILOFFSET
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)
        return spider
