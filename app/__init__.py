'''Initialize APP'''
import os
from tornado import web
from tornado.options import define, options
from processor import process
from config import DEV_CONFIG, PROD_CONFIG
from .handlers import (PageNotFoundHandler,
                       IndexHandler,
                       PostHandler,
                       AchiveHandler,
                       ShareHandler,
                       ProductHandler,
                       LinkHandler,
                       AboutHandler)

def create_app():
    '''Create APP'''
    define(
        'config',
        default='dev',
        help='config',
        type=str)
    options.parse_command_line()
    if options.config == 'dev':
        DEV_CONFIG['POSTS'] = process()
        define(
            'CONFIG',
            default=DEV_CONFIG,
            help='config',
            type=dict)
    else:
        PROD_CONFIG['POSTS'] = process()
        define(
            'CONFIG',
            default=PROD_CONFIG,
            help='config',
            type=dict)
    define('port', default=options.CONFIG['PORT'], help='run on the given port', type=int)
    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
        debug=options.CONFIG['DEBUG'],
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
