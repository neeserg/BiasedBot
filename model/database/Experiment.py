from pymongo import MongoClient
import json




class Experiment:
    #must have authenticstion file with mongodb authentication already in it.
    def __init__(self):
        self.auth = {}
        with open("model/database/authentication.json") as file:
            self.auth = json.load(file)
    
    def create_experiment(self, experiment):
        username = self.auth["username"]
        password = self.auth["password"]
        ip = self.auth["ip"]
        port = self.auth["port"]
        client = MongoClient('mongodb://%s:%s@%s:%s/'%(username,password,ip,port))
        db = client.get_database("BiasedBot")
        col = db.get_collection("Experiment")
        for i in range(10):
            result = col.insert_one(experiment)
            if(result.acknowledged):
                client.close()
                return True
            
        return False

    def update_form(self, experiment):
        if "user_id" not in experiment:
            return False
        user_id = experiment["user_id"]

        username = self.auth["username"]
        password = self.auth["password"]
        ip = self.auth["ip"]
        port = self.auth["port"]

        client = MongoClient('mongodb://%s:%s@%s:%s/'%(username,password,ip,port))
        db = client.get_database("BiasedBot")
        col = db.get_collection("Experiment")
        for i in range(10):
            result = col.update_one({"user_id": user_id}, {'$push':{"forms": experiment}})
            if(result.acknowledged):
                client.close()
                return True     
        return False
    



    def insert(self, usermessage):
        if "user_id" not in usermessage:
            return False
        user_id = usermessage["user_id"]

        username = self.auth["username"]
        password = self.auth["password"]
        ip = self.auth["ip"]
        port = self.auth["port"]

        client = MongoClient('mongodb://%s:%s@%s:%s/'%(username,password,ip,port))
        db = client.get_database("BiasedBot")
        col = db.get_collection("Experiment")

        for i in range(10):
            result = col.update_one({"user_id": user_id},{"$push": {"chat": usermessage}})
            if(result.acknowledged):
                client.close()
                return True     
        return False

    def get_url(self, topic, bot_type, user_id):
        username = self.auth["username"]
        password = self.auth["password"]
        ip = self.auth["ip"]
        port = self.auth["port"]
        client = MongoClient('mongodb://%s:%s@%s:%s/'%(username,password,ip,port))
        db = client.get_database("BiasedBot")
        col = db.get_collection("Experiment")

        for i in range(10):
            result = col.find_one({"user_id": user_id})
            if(result):
                client.close()
                return result[bot_type+topic]     
        return False