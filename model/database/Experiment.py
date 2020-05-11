from pymongo import MongoClient
from hashlib import sha256
import json
import uuid



class Experiment:
    #must have authenticstion file with mongodb authentication already in it.
    def __init__(self):
        self.auth = {}
        with open("model/database/authentication.json") as file:
            self.auth = json.load(file)
    
    def _get_mongo_url(self):
        username = self.auth["username"]
        password = self.auth["password"]
        ip = self.auth["ip"]
        port = self.auth["port"]
        return 'mongodb://%s:%s@%s:%s/'%(username,password,ip,port)
    
    def create_experiment(self, experiment):
        client = MongoClient(self.get_mongo_url())
        db = client.get_database("BiasedBot")
        col = db.get_collection("Experiment")
        result = col.insert_one(experiment)
        if(result.acknowledged):
            client.close()
            return True
        client.close()
        return False

    def update_form(self, experiment):
        if "user_id" not in experiment:
            return False
        user_id = experiment["user_id"]
        client = MongoClient(self.get_mongo_url())
        db = client.get_database("BiasedBot")
        col = db.get_collection("Experiment")
        result = col.update_one({"user_id": user_id}, {'$push':{"forms": experiment}})
        if(result.acknowledged):
            client.close()
            return True     
        client.close()
        return False
    



    def insert(self, usermessage):
        if "user_id" not in usermessage:
            return False
        user_id = usermessage["user_id"]
        client = MongoClient(self.get_mongo_url())
        db = client.get_database("BiasedBot")
        col = db.get_collection("Experiment")
        result = col.update_one({"user_id": user_id},{"$push": {"chat": usermessage}})
        if(result.acknowledged):
            client.close()
            return True  
        client.close()
        return False

    def get_url(self, topic, bot_type, user_id):
        client = MongoClient(self.get_mongo_url())
        db = client.get_database("BiasedBot")
        col = db.get_collection("Experiment")

        result = col.find_one({"user_id": user_id})
        if(result):
            client.close()
            if not self._update_counter(user_id):
                return result[bot_type+topic]
            else:
                return False
        client.close()
        return False
    
    def _update_counter(self, user_id):
        client = MongoClient(self.get_mongo_url())
        db = client.get_database("BiasedBot")
        col = db.get_collection("Experiment")
        result = col.update_one({"user_id": user_id},{"$inc": {"conv_done": 1}})
        if(result.acknowledged):
            client.close()
            return True 
        client.close()
        return False


    def finished(self, user_id):
        client = MongoClient(self.get_mongo_url())
        db = client.get_database("BiasedBot")
        col = db.get_collection("Experiment")
        result = col.find_one({"user_id": user_id})
        if(result):
            client.close()
            if result["num_conv"] > result["conv_done"]:
                return "Error: Looks like you have not completed the experiment"
            else:
                password = "unimelb_biasedbot_314"
                uid = uuid.UUID(user_id).hex[:16]
                sha = sha256()
                sha.update(password)
                sha.update(uid)
                return uid+"-"+sha.hexdigest()[:16]
        else:
            client.close()
            return "Error: I am sorry the user ID does not exist"