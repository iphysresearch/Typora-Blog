'''Config'''
import os
import copy

ROOT_PATH = os.path.realpath(os.path.dirname(__file__))

COMMON_CONFIG = {
    'port': 8083,
    'debug': True,
    'root_path': ROOT_PATH}

DEV_CONFIG = copy.deepcopy(COMMON_CONFIG)

PROD_CONFIG = copy.deepcopy(COMMON_CONFIG)
PROD_CONFIG['debug'] = False
