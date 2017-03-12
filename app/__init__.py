import os
from tornado import web
from tornado.options import define, options
from .handlers import *
from config import COMMON_CONFIG

def create_app():
    options.parse_command_line()
    define('port', default=COMMON_CONFIG.PORT, help='run on the given port', type=int)
    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
        debug=COMMON_CONFIG.DEBUG,
        gzip=True,
    )
    app = web.Application([
        (r'/', IndexHandler),
        (r'/p/(.*)', PostHandler),
        (r'/achive', AchiveHandler),
        (r'/share', ShareHandler),
        (r'/product', ProductHandler),
        (r'/link', LinkHandler),
        (r'/about', AboutHandler),
        (r'/(robots\.txt)', web.StaticFileHandler, dict(path=settings['static_path'])),
        ('.*', PageNotFoundHandler)
    ], **settings)
    return app
