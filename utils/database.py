from pymongo import MongoClient
from pymongo.server_api import ServerApi

from .env import Env

URI: str = f"mongodb+srv://{Env.MONGODB_USER}:{Env.MONGODB_PASS}@{Env.MONGODB_DB}.wldr2eq.mongodb.net/?retryWrites=true&w=majority&appName=laps"

COLLECTION: str = 'laps'


def get_client():
    return MongoClient(URI, server_api=ServerApi('1'))


def get_database():
    return get_client().get_database(name=Env.MONGODB_DB)


def get_result() -> list:
    # Get database
    database = get_database()
    # Get collection
    res_collection = database.get_collection(name=COLLECTION)
    # Get all results from collection
    return list(res_collection.find({}))


def insert_result(result: dict):
    # Get database
    database = get_database()
    # Get collection
    res_collection = database.get_collection(name=COLLECTION)
    # Insert one
    res_collection.insert_one(document=result)

def insert_results(data: list):
    # Get database
    database = get_database()
    # Get collection
    res_collection = database.get_collection(name=COLLECTION)
    # Insert one
    res_collection.insert_many(documents=data)