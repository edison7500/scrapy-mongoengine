import logging
from datetime import datetime
from mongoengine import fields, DynamicDocument, DoesNotExist
from scrapy.exporters import BaseItemExporter


def not_set(string):
    """Check if a string is None or ''.
    :returns: bool - True if the string is empty
    """
    if string is None:
        return True
    elif string == '':
        return True
    return False


class Article(DynamicDocument):
    title = fields.StringField(verbose_name="title")
    cover = fields.StringField(blank=True)
    content = fields.StringField()
    origin_link = fields.URLField(verbose_name="origin_link")
    published_at = fields.DateTimeField()
    tags = fields.ListField(blank=True)
    type = fields.StringField(verbose_name="type")
    scrapy_mongodb = fields.DictField(db_field="scrapy-mongodb")

    meta = {
        "collection": "bitcoin",
        "ordering": ["-published_at"],
        "indexes": ["$title", {"fields": ["published_at"]}],
        "index_background": True,
    }

    def __str__(self):
        return self.title


class MongoEnginePipeline(BaseItemExporter):
    config = {"unique_key": None, "append_timestamp": False}

    def __init__(self, **kwargs):
        super(MongoEnginePipeline, self).__init__(**kwargs)
        self.logger = logging.getLogger("scrapy-mongoengine-pipeline")

    def open_spider(self, spider):
        self.crawler = spider.crawler
        self.settings = spider.settings

        options = [
            ("unique_key", "MONGODB_UNIQUE_KEY"),
            ("buffer", "MONGODB_BUFFER_DATA"),
            ("append_timestamp", "MONGODB_ADD_TIMESTAMP"),
        ]

        for key, setting in options:
            if not not_set(self.settings[setting]):
                self.config[key] = self.settings[setting]

    def process_item(self, item, spider):
        item = dict(self._get_serialized_fields(item))
        if self.config['append_timestamp']:
            item['scrapy-mongodb'] = {'ts': datetime.utcnow()}
        return self.insert_item(item, spider)

    def insert_item(self, item, spider):
        if self.config["unique_key"] is not None:
            _key = self.config["unique_key"]
            try:
                a = Article.objects.get(**{_key: item[_key]})
                for k, v in item.items():
                    setattr(a, k, v)
            except DoesNotExist as e:
                a = Article(**item)
            a.save()
        return item
