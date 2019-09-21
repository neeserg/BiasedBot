from pymongo import MongoClient
import urlib.parse
from classifier import combo_classify, tokenize 

class Conversation:
    def __init__(self, topic, classifier, user_id):
        ####
        self._topic = topic
        self._user_id = user_id
        self._classifier = classifier
        self._username =  urllib.parse.quote_plus('admin')
        self._password = urllib.parse.quote_plus('luhpi23h1brb23jr34hr324')
        client = MongoClient('mongodb://%s:%s@0.0.0.0:27017/' % (self._username, self._password))
        db = client.get_database("BiasedBot")
        col = db.get_collection("Conversation")
        self._current_conversation = col.find_one({"userId": userId, "active":True})
        if (not self._current_conversation):
            current_conversation = {}
            current_conversation["active"] = True
            current_conversation["userId"] = userId
            current_conversation["bot_resp"] = []
            current_conversation["user_resp"] = []
            col.insert_one(current_conversation)
        self._current_conversation = col.find_one({"userId": userId, "active":True})
        client.close()


    def get_resp(self, message):
        token = tokenize(message)
        list_of_categories = self_categorize(token)

        for category in list_of_categories:
            cat1 = category[0]
            best = self._retrieved_best(cat1, token) 
            if best:
                best = best[0][0]
                self._update_conversation(message, best["_id"])
                return best["resp"]
        self.end(message)
        return "Thank You"


        ## categorize message into arguement
        ## get the best message for the arguement
        ## update the pair
   """List of best agetgories sorted by score"""
    def _categorize(self, token): 
        client = MongoClient('mongodb://%s:%s@0.0.0.0:27017/' % (self._username, self._password))
        db = client.get_database("BiasedBot")
        col = db.get_collection("Categories")
        c = {}
        for doc in col.find({"topic":self._topic}):
            c[doc["name"]] = doc["tokens"]
        client.close()
        scores = {}
        for key in c:
            scores[key] = combo_classify(c[key], token)
        return sorted(scores.items(), reverse = True, key = lambda item: item[1])
    
    """Retrieve the best documents according to cosine score"""
    def _retrieved_best(self, category, token): 
        client = MongoClient('mongodb://%s:%s@0.0.0.0:27017/' % (self._username, self._password))
        db = client.get_database("BiasedBot")
        col = db.get_collection("Bot Responses")
        scores = {}
        for doc in col.find({"topic": self._topic, "attacks":{"$regex": category}}):
            if doc["_id"] in self._current_conversation["bot_resp"]:
                continue
            else:
                bot_token = tokenize(doc["resp"])
                scores[doc] = combo_classify(bot_token, token)
        
        return sorted(scores.items(), reverse = True, key = lambda item: item[1])

                                                                

        return
    """Update the message and current message"""
    def _update_conversation(self, message, _id):
        self._current_conversation["bot_resp"].append(_id)
        self._current_conversation["user_resp"].append(message)
        convo_id = self._current_conversation["_id"]
        client = MongoClient('mongodb://%s:%s@0.0.0.0:27017/' % (self._username, self._password))
        db = client.get_database("BiasedBot")
        col = db.get_collection("Conversation")
        col.update_one({"_id": convo_id}, {"$set": self._current_conversation})

        return
    
    """Update and set the the conversation status to inactive"""
    def end(self, message):
        self._current_conversation["user_resp"].append(message)
        self._current_conversation["active"] = False
        convo_id = self._current_conversation["_id"]
        client = MongoClient('mongodb://%s:%s@0.0.0.0:27017/' % (self._username, self._password))
        db = client.get_database("BiasedBot")
        col = db.get_collection("Conversation")
        col.update_one({"_id": convo_id}, {"$set": self._current_conversation})
        return

    
    def get_initial(self, ):

