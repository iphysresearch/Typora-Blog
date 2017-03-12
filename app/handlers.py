from tornado import web, httpclient, gen
from config import COMMON_CONFIG


class PageNotFoundHandler(web.RequestHandler):
    def get(self):
        self.render('error.html', code='404')

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('error.html', code='404')
        else:
            self.render('error.html', code='500')


class IndexHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.render('index.html', posts=COMMON_CONFIG.POSTS)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('error.html', code='404')
        else:
            self.render('error.html', code='500')


class PostHandler(web.RequestHandler):
    @gen.coroutine
    def get(self, url):
        foundPost = False
        for post in COMMON_CONFIG.POSTS:
            if url == post['title']:
                foundPost = True
                break
        if foundPost:
            self.render('posts/' + post['title'] + '.html', timestamp = post['timestamp'])
        else:
            self.render('error.html', code='404')

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('error.html', code='404')
        else:
            self.render('error.html', code='500')


class AchiveHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.render('achive.html', posts=COMMON_CONFIG.POSTS)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('error.html', code='404')
        else:
            self.render('error.html', code='500')


class ShareHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.render('share.html')

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('error.html', code='404')
        else:
            self.render('error.html', code='500')


class ProductHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.render('product.html')

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('error.html', code='404')
        else:
            self.render('error.html', code='500')


class LinkHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.render('link.html')

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('error.html', code='404')
        else:
            self.render('error.html', code='500')


class AboutHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.render('about.html')

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('error.html', code='404')
        else:
            self.render('error.html', code='500')
