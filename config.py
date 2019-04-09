import os
import json

root = os.path.dirname(os.path.realpath(__file__))
with open('./config.json') as fp:
    config = json.load(fp)

DB_URL = os.environ.get('DB_URL', None) or config['db']['url'].format(root=root)

REDIS_HOST = config['redis']['host']
REDIS_PORT = config['redis']['port']
# 'redis://localhost:6379'
REDIS_URL = os.environ.get('REDIS_URL', None) or 'redis://{}:{}'.format(REDIS_HOST, REDIS_PORT)
