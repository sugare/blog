#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-3-2 下午8:17
# @Author  : Sugare
# @mail    : 30733705@qq.com
# @File    : app.py
# @Software: PyCharm


import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.escape import json_decode, json_encode
import os
from lib.orm import noblog,rightbarDate,rightbarHot,latest,dateData,PagerPerItem, PagerTotalItem, getData, tagData, indexTag
import json


from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/?', IndexHandler),
            (r'/page/(\d+)/?', PageHandler),
            (r'/tag/([a-z]+$)', TagHandler),
            (r'/date/(.*)/?', DateHandler),
            (r'/api/?', ApiHandler),
            (r'/.*', ErrorHandler),
        ]

        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            debug=True
        )

        super(Application,self).__init__(handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    pass


class IndexHandler(BaseHandler):
    def get(self):
        perPage = 8
        totalItem = PagerTotalItem()
        totalPage = totalItem // perPage if totalItem % perPage == 0 else totalItem // perPage + 1

        dataPool = PagerPerItem(1, perPage)
        self.render('index.html', dataPool=dataPool, indexTag=indexTag(), rightbarHot=rightbarHot(), rightbarDate=rightbarDate(),totalPage=totalPage)

    def post(self):
        perPage = 8
        totalItem = PagerTotalItem()
        totalPage = totalItem // perPage if totalItem % perPage == 0 else totalItem // perPage + 1
        page = self.get_argument('page')
        if int(page) > totalPage:
            self.write('1')
        else:
            dataPool = PagerPerItem(int(page), perPage)
            self.render('indexApi.html',dataPool=dataPool)

class ApiHandler(BaseHandler):
    def get(self, *args, **kwargs):
        a = {'i1': 1, 'i2': PagerPerItem(1,8)}
        self.write(json.dumps(a))

    def post(self):
        tag = self.get_argument('category')
        if tag == 'all':
            self.render('tagApi.html', tagDataPool=PagerPerItem(1, 8))
        else:
            self.render('tagApi.html',tagDataPool=tagData(tag))

class PageHandler(BaseHandler):
    def get(self, blog_id):
        try:
            dataPool = getData(blog_id)
        except:
            self.write_error(404)
        self.render('page.html',dataPool=dataPool, rightbarHot=rightbarHot(), rightbarDate=rightbarDate())

class TagHandler(BaseHandler):
    def get(self, tag):
        self.render('tag.html', tagDataPool=tagData(tag),rightbarHot=rightbarHot(), rightbarDate=rightbarDate())

    def post(self):
        tag = self.get_argument('category')
        self.render('tagApi.html',tagDataPool=tagData(tag))

class DateHandler(BaseHandler):
    def get(self, date):
        self.render('date.html', dateDataPool=dateData(date), rightbarHot=rightbarHot(), rightbarDate=rightbarDate())

class ErrorHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('404.html')

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()