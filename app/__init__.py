'''Initialize APP'''
import os
import sys
import logging

from tornado import web
from tornado.options import define, options

from processor import process
from config import DEV_CONFIG, PROD_CONFIG
from .log_kit import LogFilter
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
    print(sys.getdefaultencoding())
    print(sys.stdout.encoding)
    root_logger = logging.getLogger()
    formatter = logging.Formatter('[%(asctime)s] $%(levelname)s (%(filename)s:%(lineno)d) %(message)s')
    stdout_hdlr = logging.StreamHandler(sys.stdout)
    stderr_hdlr = logging.StreamHandler(sys.stderr)
    log_filter = LogFilter(logging.WARNING)
    stdout_hdlr.addFilter(log_filter)
    stdout_hdlr.setLevel(logging.INFO)
    stderr_hdlr.setLevel(logging.WARNING)
    stdout_hdlr.setFormatter(formatter)
    stderr_hdlr.setFormatter(formatter)
    root_logger.addHandler(stdout_hdlr)
    root_logger.addHandler(stderr_hdlr)

    define('env',
           default='dev',
           help='[dev|prod](dev is default)',
           type=str)

    define('port',
           default=DEV_CONFIG['port'],
           help='run on the given port',
           type=int)

    options.parse_command_line()
    if options.env == 'dev':
        define('config', default=DEV_CONFIG, type=dict)
    else:
        define('config', default=PROD_CONFIG, type=dict)

    info_logger_path = os.path.join(options.config['root_path'], 'log/info.log')
    err_logger_path = os.path.join(options.config['root_path'], 'log/err.log')
    file_info_hdlr = logging.FileHandler(info_logger_path)
    file_err_hdlr = logging.FileHandler(err_logger_path)
    file_info_hdlr.addFilter(log_filter)
    file_info_hdlr.setLevel(logging.INFO)
    file_err_hdlr.setLevel(logging.WARNING)
    file_info_hdlr.setFormatter(formatter)
    file_err_hdlr.setFormatter(formatter)
    root_logger.addHandler(file_info_hdlr)
    root_logger.addHandler(file_err_hdlr)
    options.config['root_logger'] = root_logger

    options.config['posts'] = process()

    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
        debug=options.config['debug'],
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
        ('.*', PageNotFoundHandler)
    ], **settings)
    return app
