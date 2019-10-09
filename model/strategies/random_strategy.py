from pymongo import MongoClient
import urllib.parse
import random

IP_ADRESS = "115.146.92.158"

class Random_strategy:
    def __init__(self, topic, despsition=1,_filter = {}):
        ####
        self._topic = topic
        self._filter = _filter
        self._desposition = despsition
        self._username = urllib.parse.quote_plus('admin')
        self._password = urllib.parse.quote_plus('luhpi23h1brb23jr34hr324')
    
    def get_resp(self, message, done_set):
        best = self._get_random(done_set) 
        if best:
            best = random.choice(best)
            return (best["resp"], best["_id"])
        return ("End Of Conversation", -1)

    def _get_random(self, done_set): 
        client = MongoClient('mongodb://%s:%s@%s:27017/' % (self._username, self._password, IP_ADRESS))
        db = client.get_database("BiasedBot")
        col = db.get_collection("Bot Responses")
        scores = []
        _filter = {"topic": self._topic, "desposition": self._desposition}
        _filter.update(self._filter)
        for doc in col.find(_filter):
            if doc["_id"] in done_set:
                continue
            else:
                scores.append(doc)
        return scores