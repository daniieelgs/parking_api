import os
from dotenv import load_dotenv

from enum import Enum

DEFAULT_API_PREFIX = '/api/v1'
DEFAULT_API_TITLE = 'BOT API IA'
DEFAULT_API_VERSION = ''
DEFAULT_SWAGGER_URL = '/swagger-ui'
DEFAULT_OPENAPI_VERSION = '3.0.3'
DEFAULT_OPENAPI_URL_PREFIX = '/'
DEFAULT_OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
DEFAULT_DEBUG = False
DEFAULT_PORT = 5000
DEFAULT_HOST = "0.0.0.0"

#------------------------------

load_dotenv()

API_PREFIX=os.getenv('API_PREFIX', DEFAULT_API_PREFIX)
API_TITLE=os.getenv('API_TITLE', DEFAULT_API_TITLE)
API_VERSION=os.getenv('API_VERSION', DEFAULT_API_VERSION)
SWAGGER_URL=os.getenv('SWAGGER_URL', DEFAULT_SWAGGER_URL)
OPENAPI_VERSION=os.getenv('OPENAPI_VERSION', DEFAULT_OPENAPI_VERSION)
OPENAPI_URL_PREFIX=os.getenv('OPENAPI_URL_PREFIX', DEFAULT_OPENAPI_URL_PREFIX)
OPENAPI_SWAGGER_UI_URL=os.getenv('OPENAPI_SWAGGER_UI_URL', DEFAULT_OPENAPI_SWAGGER_UI_URL)
REDIS_URL=os.getenv('REDIS_URL', None)

DB_USER = os.getenv('DB_USER', None)
DB_PASSWORD = os.getenv('DB_PASSWORD', None)
DB_HOST = os.getenv('DB_HOST', None)
DB_PORT = os.getenv('DB_PORT', None)
DB_NAME = os.getenv('DB_NAME', None)

MYSQL_URI  = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', None)

DEBUG = os.getenv('FLASK_DEBUG', DEFAULT_DEBUG)
DEBUG = str(DEBUG).lower() in ['true', '1', 't', 'y', 'yes']
PORT = int(os.getenv('PORT', DEFAULT_PORT))
HOST = os.getenv('HOST', DEFAULT_HOST)

#------------------------------