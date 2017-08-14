from tornado import web, gen
from tornado.options import options


class PageNotFoundHandler(web.RequestHandler):
    @gen.coroutine
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
        self.render('index.html', posts=options.config['posts'])

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('error.html', code='404')
        else:
            self.render('error.html', code='500')


class PostHandler(web.RequestHandler):
    @gen.coroutine
    def get(self, url):
        found_post = False
        for post in options.config['posts']:
            if url == post['id']:
                found_post = True
                break
        if found_post:
            self.render('post/' + post['title'] +
                        '.html', timestamp=post['timestamp'])
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
        self.render('achive.html', posts=options.config['posts'])

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
