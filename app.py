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
import os
from lib.orm import noblog,rightbarDate,rightbarHot,latest,dateData,PagerPerItem, PagerTotalItem, getData, tagData


from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/?', IndexHandler),
            (r'/page/(\d+)/?', PageHandler),
            (r'/tag/([a-z]+$)', TagHandler),
            (r'/date/(.*)/?', DateHandler),
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
        print(dataPool[1].get_tags())
        self.render('index.html', dataPool=dataPool, rightbarHot=rightbarHot(), rightbarDate=rightbarDate())

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

class DateHandler(BaseHandler):
    def get(self, date):
        self.render('date.html', dateDataPool=dateData(date), rightbarHot=rightbarHot(), rightbarDate=rightbarDate())

class ErrorHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write_error(404)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()