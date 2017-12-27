"""
Created on Nov 27 16:10 2016

@author: J. Chaudourne
"""

class Config(object):
    MONGO_HOST = 'iadvize-db-svc'
    MONGO_PORT = 27017
    MONGO_DBNAME = 'vdm'

class EnvDev(Config):
    DEBUG = True

class EnvProd(Config):
    DEBUG = False
