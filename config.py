

RUN_ON_HOST='192.168.1.202'
#RUN_ON_HOST='192.168.205.136'

REDIS_MQ_HOST = RUN_ON_HOST
REDIS_MQ_PORT = 6379
REDIS_MQ_DB = 0

DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_USER = 'gsgame'
DB_PASSWD = 'gsgame'
DB_NAME = 'test'

LOG_FILE = 'sdv.log'
LOG_LEVEL = 'DEBUG'

WSS_HOST = RUN_ON_HOST
WSS_URI = 'ws://'+RUN_ON_HOST
WSS_PORT = 8888
WSS_PREFIX_RGX = r'/rt/'