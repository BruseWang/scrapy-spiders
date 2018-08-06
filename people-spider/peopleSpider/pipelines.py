# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import os
import time
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from openpyxl import Workbook
from scrapy.http import Request


class PeoplespiderPipeline(object):
    def process_item(self, item, spider):

        return item


# class JsonWithEncodingPipeline(object):
#     # 自定义json文件的导出
#     def __init__(self):
#         self.file = codecs.open('article.json', 'w', encoding="utf-8")
#
#     def process_item(self, item, spider):
#         lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
#         self.file.write(lines)
#         return item
#
#     def spider_closed(self, spider):
#         self.file.close()


class JsonExporterPipleline(object):
    # 调用scrapy提供的json export导出json文件
    def __init__(self):
        self.file = open('data.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class TuniuPipeline(object):  # 设置工序一,生成EXCEL表格
    wb = Workbook()
    ws = wb.active

    ws.append(['pageLink', 'city', 'title', 'titleImg', 'image_urls', 'star', 'avprice', 'address', 'phone', 'nearLocation', 'payType', 'workTime', 'playNotice', 'introduce', 'images'])

    def process_item(self, item, spider):

        def serialization_value(value):
            if not isinstance(value, str):
                # ensure_ascii 原样输出
                return json.dumps(value, ensure_ascii=False)
            else:
                return value

        keys = list(list(dict(item).keys()))
        print(keys)
        values = list(map(serialization_value, list(dict(item).values())))
        self.ws.append(values)

        file_name = item['city']+'01' + '.xlsx'
        self.wb.save(file_name)  # 保存xlsx文件

        return item


class TetePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if len(item['image_urls']) > 0:
            for index, image_url in enumerate(item['image_urls']):
                if os.path.exists(item['title'] + str(index) + image_url[-4:]):
                    print('yes,have this imag')
                else:
                    time.sleep(0.2)
                    yield Request(image_url, meta={'title': item['title'], 'index': index})

    def file_path(self, request, response=None, info=None):
        title = request.meta['title']
        index = request.meta['index']
        image_url = request.url
        image_name = title+str(index)+image_url[-4:]
        return image_name


