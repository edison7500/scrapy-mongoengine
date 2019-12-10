from scrapy import signals
from scrapy.exceptions import NotConfigured
from mongoengine import connection


class MongoEngineExtension(object):

    def __init__(self, crawler):
        if not crawler.settings.getbool("MONGOENGINE_ENABLED", False):
            raise NotConfigured

        self.mongodb = crawler.settings.get("MONGODB_DATABASES")
        if self.mongodb is None:
            raise NotConfigured

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler)
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        return ext

    def spider_opened(self, spider):
        for alias, conn_settings in self.mongodb.items():
            connection.register_connection(alias, **conn_settings)

    def spider_closed(self, spider):
        connection.disconnect()
