from model.nlp.classifier import classify
from model.strategies.retrieval_strategy import Retrieval_strategy
from pymongo import MongoClient
import urllib.parse

IP_ADRESS = "115.146.92.158"


class FacebookConversation:
    def __init__(self, user_id):
        self._username = urllib.parse.quote_plus('admin')
        self._password = urllib.parse.quote_plus('luhpi23h1brb23jr34hr324')
        client = MongoClient('mongodb://%s:%s@%s:27017/' % (self._username, self._password, IP_ADRESS))
        db = client.get_database("BiasedBot")
        col = db.get_collection("Conversation")
        self._current_conversation = col.find_one({"userId": user_id, "active":True})
        if (not self._current_conversation):
            current_conversation = {}
            current_conversation["active"] = True
            current_conversation["userId"] = user_id
            current_conversation["bot_resp"] = []
            current_conversation["user_resp"] = []
            current_conversation["desposition"] = 1
            current_conversation["topic"] = "none"
            col.insert_one(current_conversation)
            self._current_conversation = col.find_one({"userId": user_id, "active":True})
        client.close()
   
    def get_current(self):
        if not self._current_conversation["bot_resp"]:
            return False
        else:
            current = self._current_conversation["bot_resp"][-1]
            client = MongoClient('mongodb://%s:%s@%s:27017/' % (self._username, self._password, IP_ADRESS))
            db = client.get_database("BiasedBot")
            col = db.get_collection("Bot Responses")
            current = col.find_one({"_id": current})
            return current

    def get_next(self, message):       
        if message == "#reset":
            self.end(message)
            return "End Of Conversation"
        current = self.get_current()
        if not current:
            current = self.get_initial()
            resp = current["resp"]
            _id = current["_id"]
        elif self._current_conversation["topic"] == "none":
            keys = self.get_keys(current) 
            topic = classify(message, keys)
            self._current_conversation["topic"] = topic
            client = MongoClient('mongodb://%s:%s@%s:27017/' % (self._username, self._password, IP_ADRESS))
            db = client.get_database("BiasedBot")
            col = db.get_collection("Bot Responses")
            resp = col.find_one({"topic": topic, "attacks": "initial"})
            client.close()
            _id = resp["_id"]
            resp = resp["resp"]               
        else:
            topic = self._current_conversation["topic"]
            strategy = Retrieval_strategy(topic)
            mes = message
            if "next" in current:
                keys = list(current["next"].keys())
                _next = classify(message, keys)
                mes = current["next"][_next]
            resp, _id = strategy.get_resp(mes, set(self._current_conversation["bot_resp"]))
            if _id == -1:
                self.end(message)
                return "End Of Conversation"

        self._update_conversation(message, _id)
        return resp


    """Update the message and current message"""
    def _update_conversation(self, message, _id):
        self._current_conversation["bot_resp"].append(_id)
        self._current_conversation["user_resp"].append(message)
        convo_id = self._current_conversation["_id"]
        client = MongoClient('mongodb://%s:%s@%s:27017/' % (self._username, self._password, IP_ADRESS))
        db = client.get_database("BiasedBot")
        col = db.get_collection("Conversation")
        col.update_one({"_id": convo_id}, {"$set": self._current_conversation})
        client.close()
        return

    """Update and set the the conversation status to inactive"""
    def end(self, message):
        self._current_conversation["user_resp"].append(message)
        self._current_conversation["active"] = False
        convo_id = self._current_conversation["_id"]
        client = MongoClient('mongodb://%s:%s@%s:27017/' % (self._username, self._password, IP_ADRESS))
        db = client.get_database("BiasedBot")
        col = db.get_collection("Conversation")
        col.update_one({"_id": convo_id}, {"$set": self._current_conversation})
        client.close()
        return

    def get_initial(self):
        client = MongoClient('mongodb://%s:%s@%s:27017/' % (self._username, self._password, IP_ADRESS))
        db = client.get_database("BiasedBot")
        col = db.get_collection("Bot Responses")
        resp = col.find_one({"topic": "initial"})
        client.close()
        return resp

    def get_keys(self, current):
        if "next" in current:
            return list(current["next"].keys())
        return []
