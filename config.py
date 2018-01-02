'''Config'''
import os
import copy

ROOT_PATH = os.path.realpath(os.path.dirname(__file__))

COMMON_CONFIG = {
    'port': 8083,
    'debug': True,
    'root_path': ROOT_PATH,
    'paging': 5,
    'baidu_commit_url': 'http://data.zz.baidu.com/urls?site=https://www.jackeriss.com&token=ZwMI7Ew0rbHnz5ky'
}

DEV_CONFIG = copy.deepcopy(COMMON_CONFIG)

PROD_CONFIG = copy.deepcopy(COMMON_CONFIG)
PROD_CONFIG['debug'] = False
