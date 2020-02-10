import os

TITLE = 'AT Tracker'
DESC = 'Track Auckland Transport Vehicles'

VERSION = '1.0.0'

API_V1_STR = '/api/v1'

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
REDIS_PASS = os.environ.get('REDIS_PASS')
REDIS_DB_API = os.environ.get('REDIS_DB_API', 0)
REDIS_DB_TASKS = os.environ.get('REDIS_DB_TASKS', 1)

AT_API_URL = os.environ.get('AT_API_URL', 'https://api.at.govt.nz/v2')
AT_API_KEY = os.environ.get('AT_API_KEY', None)
