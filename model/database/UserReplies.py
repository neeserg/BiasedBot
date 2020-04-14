from pymongo import MongoClient
import json


class UserReplies:
    #must have authenticstion file with mongodb authentication already in it.
    def __init__(self):
        self.auth = {}
        with open("model/database/authentication.json") as file:
            self.auth = json.load(file)
    

    def insert(self,usermessage):
        username = self.auth["username"]
        password = self.auth["password"]
        ip = self.auth["ip"]
        port = self.auth["port"]

        client = MongoClient('mongodb://%s:%s@%s:%s/'%(username,password,ip,port))
        db = client.get_database("BiasedBot")
        col = db.get_collection("UserReplies")

        for i in range(10):
            result = col.insert_one(usermessage)
            if(result.acknowledged):
                client.close()
                return True
            
        return False


    def get_url(self, topic, type, user_id):
        return "Thank you very much"
