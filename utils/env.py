import os

from dotenv import load_dotenv

from .paths import ROOT_PATH

load_dotenv(ROOT_PATH.joinpath('.env'))


class Env:
    INFLUXDB_TOKEN = os.getenv('INFLUXDB_TOKEN', '')
    INFLUXDB_ORG = os.getenv('INFLUXDB_ORG', '')
    INFLUXDB_HOST = os.getenv('INFLUXDB_HOST', '')
    INFLUXDB_BUCKET = os.getenv('INFLUXDB_BUCKET', '')
    MONGODB_PASS = os.getenv('MONGODB_PASS', '')
    MONGODB_USER = os.getenv('MONGODB_USER', '')
    MONGODB_DB = os.getenv('MONGODB_DB', '')
