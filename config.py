'''Config'''
import copy

COMMON_CONFIG = {
    'PORT': 8084,
    'DEBUG': True}

DEV_CONFIG = copy.deepcopy(COMMON_CONFIG)

PROD_CONFIG = copy.deepcopy(COMMON_CONFIG)
PROD_CONFIG['DEBUG'] = False
