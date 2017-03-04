#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-3-4 下午5:32
# @Author  : Sugare
# @mail    : 30733705@qq.com
# @File    : test.py
# @Software: PyCharm

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-3-2 下午8:17
# @Author  : Sugare
# @mail    : 30733705@qq.com
# @File    : app.py
# @Software: PyCharm


import tornado.web
from tornado.web import UIModule
import tornado.ioloop
import tornado.httpserver
import tornado.options
import os
from lib.orm import rightbarDate, rightbarHot, indexTag, PagerPerItem, PagerTotalItem


from tornado.options import define, options
define("port", default=8899, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/?',TestHandler),
            (r'/.*', ErrorHandler),
        ]

        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            ui_modules = { 'Hello': HelloModle, 'tagCloud': tagCloudModule, 'newestPosts': newestPostsModule,
                           'hotestPosts': hotestPostsModule, 'tagIndex': tagIndexModule, 'allPosts':allPostsModule},
            debug=True,
        )

        super(Application,self).__init__(handlers, **settings)



class HelloModle(UIModule):
    def render(self):
        a = ['1','2','3']
        return a
class hotestPostsModule(UIModule):
    def render(self):
        return self.render_string('modules/hotest_posts.html', rightbarHot=rightbarHot())

class tagCloudModule(UIModule):
    def render(self):
        return self.render_string('modules/tag_cloud.html')

class newestPostsModule(UIModule):
    def render(self):
        return self.render_string('modules/newest_posts.html', rightbarDate=rightbarDate())

class tagIndexModule(UIModule):
    def render(self):
        return self.render_string('modules/tag_index.html', indexTag=indexTag())

class allPostsModule(UIModule):
    def render(self):
        perPage = 8
        totalItem = PagerTotalItem()
        totalPage = totalItem // perPage if totalItem % perPage == 0 else totalItem // perPage + 1
        dataPool = PagerPerItem(1, perPage)
        return self.render_string('modules/all_posts.html', dataPool=dataPool,totalPage=totalPage)


class BaseHandler(tornado.web.RequestHandler):
    pass

class TestHandler(BaseHandler):
    def get(self):
        self.render('test.html')

    def post(self, *args, **kwargs):
        pass

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