from pymongo import MongoClient
import urllib.parse
from model.nlp.classifier import combo_classify, tokenize

IP_ADRESS = "115.146.92.158"


class Retrieval_strategy:
    def __init__(self, topic, despsition=1,_filter={}):
        ####
        self._topic = topic
        self._desposition = despsition
        self._filter = _filter
        self._username = urllib.parse.quote_plus('admin')
        self._password = urllib.parse.quote_plus('luhpi23h1brb23jr34hr324')

    def get_resp(self, message, done_set):
        token = tokenize(message)
        list_of_categories = self._categorize(token)
        for category in list_of_categories:
            cat1 = category[0]
            best = self._retrieved_best(cat1, token, done_set) 
            if best:
                best = best[0][0]
                return (best["resp"], best["_id"])
        return ("End Of Conversation", -1)


        ## categorize message into arguement
        ## get the best message for the arguement
        ## update the pair
    """List of best agetgories sorted by score"""
    def _categorize(self, token): 
        client = MongoClient('mongodb://%s:%s@%s:27017/' % (self._username, self._password, IP_ADRESS))
        db = client.get_database("BiasedBot")
        col = db.get_collection("Categories")
        c = {}
        for doc in col.find({"topic": self._topic, "desposition": self._desposition}):
            c[doc["name"]] = doc["tokens"]
        client.close()
        scores = {}
        for key in c:
            scores[key] = combo_classify(c[key], token)
        return sorted(scores.items(), reverse = True, key = lambda item: item[1])
    
    """Retrieve the best documents according to cosine score"""
    def _retrieved_best(self, category, token, done_set): 
        client = MongoClient('mongodb://%s:%s@%s:27017/' % (self._username, self._password, IP_ADRESS))
        db = client.get_database("BiasedBot")
        col = db.get_collection("Bot Responses")
        scores = []
        _filter = {"topic": self._topic, "desposition": self._desposition, "attacks":{"$regex": category}}
        _filter.update(self._filter)
        for doc in col.find(_filter):
            if doc["_id"] in done_set:
                continue
            else:
                bot_token = tokenize(doc["resp"])
                scores.append( (doc, combo_classify(bot_token, token) ) )
        
        return sorted(scores, reverse = True, key = lambda item: item[1])

                                                            
    