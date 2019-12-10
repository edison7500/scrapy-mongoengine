import logging
from mongoengine import fields, DynamicDocument
from scrapy.exporters import BaseItemExporter


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
    def __init__(self, **kwargs):
        super(MongoEnginePipeline, self).__init__(**kwargs)
        self.logger = logging.getLogger("scrapy-mongoengine-pipeline")

    def process_item(self, item, spider):
        self.logger.info(item)
