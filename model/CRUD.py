from pymongo import MongoClient
from model.ExperimentConversation import Conversation
import urllib.parse

IP_ADRESS = "115.146.92.158"
username = urllib.parse.quote_plus('admin')
password = urllib.parse.quote_plus('luhpi23h1brb23jr34hr324')


def create_conversation(form):
    client = MongoClient('mongodb://%s:%s@%s:27017/' % (username, password, IP_ADRESS))
    db = client.get_database("BiasedBot")
    col = db.get_collection("Conversation")
    doc = col.insert_one(form)
    client.close()
    if doc:
        return True
    return False

def update_conversation(uid, form):
    client = MongoClient('mongodb://%s:%s@%s:27017/' % (username, password, IP_ADRESS))
    db = client.get_database("BiasedBot")
    col = db.get_collection("Conversation")
    doc  = col.update({"userId": uid}, {"$set": form})
    client.close()
    if not doc:
        return False
    return True


def get_response(uid, message):
    conver = Conversation(uid)
    resp = {"recipient": uid, "message": conver.get_next(message) }
    return resp


def is_before(uid):
    client = MongoClient('mongodb://%s:%s@%s:27017/' % (username, password, IP_ADRESS))
    db = client.get_database("BiasedBot")
    col = db.get_collection("Conversation")
    doc = col.find_one({"userId": uid})
    client.close()
    if not doc:
        return "no doc"
    if "assessment" not in doc:
        return "no doc"
    if doc["assessment"] != "after":
        return "before"
    return "after"

def is_after(uid):
    client = MongoClient('mongodb://%s:%s@%s:27017/' % (username, password, IP_ADRESS))
    db = client.get_database("BiasedBot")
    col = db.get_collection("Conversation")
    doc = col.find_one({"userId": uid})
    client.close()
    if not doc:
        return "no doc"
    if "assessment" not in doc:
        return "no doc"
    if doc["assessment"] != "before":
        return "after"
    return "before"