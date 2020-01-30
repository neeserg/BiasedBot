from model.nlp.classifier import classify
from model.strategies.retrieval_strategy import Retrieval_strategy
from pymongo import MongoClient
from model.strategies.random_strategy import Random_strategy
import urllib.parse
import uuid

IP_ADRESS = "115.146.92.158"


class Conversation:
    def __init__(self, user_id):
        #initialise the the mongodb connection 
        self._username = urllib.parse.quote_plus('admin')
        self._password = urllib.parse.quote_plus('luhpi23h1brb23jr34hr324')
        client = MongoClient('mongodb://%s:%s@%s:27017/' % (self._username, self._password, IP_ADRESS))
        db = client.get_database("BiasedBot")


        # Retrieve conversation or create it
        col = db.get_collection("Conversation")
        self._current_conversation = col.find_one({"userId": user_id, "active":True})


        if not self._current_conversation:
            current_conversation = {}
            current_conversation["active"] = True
            current_conversation["userId"] = user_id
            current_conversation["bot_resp"] = []
            current_conversation["user_resp"] = []
            current_conversation["desposition"] = 1
            current_conversation["topic"] = "climate change"
            current_conversation["strategy"] = "retrieval"
            current_conversation["filter"] = {}
            col.insert_one(current_conversation)
            self._current_conversation = col.find_one({"userId": user_id, "active":True})
        
        current = self._current_conversation
        param_filter = current["filter"] if "filter" in current else {}
        
        # setup the required strategy
        if "strategy" in current and current["strategy"] == "random":
            self.strategy = Random_strategy(current["topic"],current["desposition"],_filter = param_filter)
        else:
            self.strategy = Retrieval_strategy(current["topic"],current["desposition"], _filter = param_filter)
        client.close()

    
    def get_next(self, message):       
        if message == "#reset":
            self.end(message)
            return "End Of Conversation"
        elif not self._current_conversation["bot_resp"]:
            resp = self.get_initial()
            if not resp:
                topic = self._current_conversation["topic"]
                return "Sorry %s not one of the options, something went wrong. Please restart" % topic
            self._update_conversation(message, resp["_id"])
            return resp['resp']
        else:
            current = self._current_conversation
            topic = current["topic"]
            mes = message
            if self.if_next():
                keys = list(current["next"].keys())
                _next = classify(message, keys)
                mes = self._current_conversation["next"][_next]
            resp, _id = self.strategy.get_resp(mes, set(current["bot_resp"]))
            if _id == -1:
                self.end(message)
                return "End Of Conversation"
            self._update_conversation(message, _id)
            return resp


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
    
    def get_initial(self):
        client = MongoClient('mongodb://%s:%s@%s:27017/' % (self._username, self._password, IP_ADRESS))
        db = client.get_database("BiasedBot")
        col = db.get_collection("Bot Responses")
        topic = self._current_conversation["topic"]
        resp = col.find_one({"topic": topic, "attacks": "initial"})
        client.close()
        return resp
    
    def if_next(self):
        client = MongoClient('mongodb://%s:%s@%s:27017/' % (self._username, self._password, IP_ADRESS))
        db = client.get_database("BiasedBot")
        col = db.get_collection("Bot Responses")
        bot_resp = self._current_conversation["bot_resp"]
        if not bot_resp:
            return False
        else:
            last_resp = bot_resp[-1]
            doc = col.find_one({"id": last_resp})
            if doc:
                if "next" in doc:
                    return True
            return False