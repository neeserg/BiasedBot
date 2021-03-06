import json
from model.database.UserReplies import UserReplies
from model.database.Experiment import Experiment
from model.nlp.universal_classifier import classify
from datetime import datetime
file_stuff = {
    "empathy":{
        "climatechange": "conversations/old_stuff/empathy_climatechange.json"
    },
    "parallel": {
        "climatechange": "conversations/old_stuff/parallel_climatechange.json"
    },
    "logical":{
        "affirmative_action": "conversations/logical_affirmative_action.json",
        "free_speech": "conversations/logical_free_speech.json",
        "ml_affirmative_action": "conversations/old_stuff/ml_logical_affirmative_action.json",
        "ml_free_speech": "conversations/old_stuff/ml_logical_free_speech.json",
        "2_free_speech": "conversations/2_logical_free_speech.json",
        "2_affirmative_action":"conversations/2_logical_affirmative_action.json",
        "1_free_speech": "conversations/1_logical_free_speech.json",
        "1_affirmative_action":"conversations/1_logical_affirmative_action.json"
    },

    "character":{
        "affirmative_action": "conversations/character_affirmative_action.json",
        "free_speech": "conversations/character_free_speech.json",
        "ml_affirmative_action": "conversations/old_stuff/ml_character_affirmative_action.json",
        "ml_free_speech": "conversations/old_stuff/ml_character_free_speech.json",
        "2_free_speech": "conversations/2_character_free_speech.json",
        "2_affirmative_action":"conversations/2_character_affirmative_action.json",
        "1_free_speech": "conversations/1_character_free_speech.json",
        "1_affirmative_action":"conversations/1_character_affirmative_action.json"
    },

    "lara":{
        "affirmative_action": "conversations/lara_affirmative_action.json",
        "free_speech": "conversations/lara_free_speech.json",
        "ml_affirmative_action": "conversations/old_stuff/ml_lara_affirmative_action.json",
        "ml_free_speech": "conversations/old_stuff/ml_lara_free_speech.json",
        "2_free_speech": "conversations/2_lara_free_speech.json",
        "2_affirmative_action":"conversations/2_lara_affirmative_action.json",
        "1_free_speech": "conversations/1_lara_free_speech.json",
        "1_affirmative_action":"conversations/1_lara_affirmative_action.json"
    }
}

class EmpathyStrategy:

    def __init__(self, topic="free_speech", bot_type="lara", exper = "practice"):
        self.conversation = {}
        self.topic = topic
        self.bot_type = bot_type
        self.experiment = exper == "practice"
        if self.experiment:
            self.userReplies = UserReplies()
        else:
            self.userReplies = Experiment()
        with open(file_stuff[bot_type][topic]) as file:
            self.conversation = json.load(file)
    


    def _get_which(self, user_message, possible):
        user_message = user_message.lower().strip()
        for el in possible:
            if user_message in el["user_replies"]:
                if el["id"] not in self.conversation:
                    return "Not Found"
                return el["id"]
        return "Not Found"


    def get_prompt(self, prompt_id):
        if prompt_id in self.conversation:
            prompt = self.conversation[prompt_id]["prompt"]
            _type = self.conversation[prompt_id]["type"]
            if self.conversation[prompt_id]["type"] == "choice":
                choice = self.conversation[prompt_id]["choice"]
                return {"type": _type,"prompt_id":prompt_id, "prompt":prompt, "choice": choice}
            else:
                return {"prompt_id":prompt_id, "prompt":prompt, "type": _type}
        else:
            return {"prompt_id":prompt_id, "prompt":"%s not found"%prompt_id, "type": "error"}
    
    def insert(self, message, next_id):
        message["next_id"] = next_id
        usermessage = {"user_id": message["user_id"], "prompt": message["prompt_id"], "next": message["next_id"], "message": message["message"]}
        usermessage["topic"] = self.topic
        usermessage["type"] = self.bot_type
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        usermessage["timestamp"] = timestamp
        result = self.userReplies.insert(usermessage)
        return result

    def get_next(self, message):
        user_message = message["message"]
        current_id = message["prompt_id"]
        if (current_id not in self.conversation):
            reply = {"prompt_id": current_id, "prompt": "the conversation id does not exist", "type": self.conversation[current_id]["type"]}
            return reply
        curr_conv = self.conversation[current_id]
        next_id = "undefined"

        ##handle choice responses
        if(curr_conv["type"] == "choice"):
            ## if user replies a statement not in the choice return an error
            if(user_message.strip().lower() not in curr_conv["choice"]):
                reply = {"prompt_id": current_id, "prompt": "Not part of the available choices", "type": curr_conv["type"], 
                        "choice":curr_conv["choice"]}
                return reply
            ## handle response
            else:
                next_id = self._get_which(user_message, curr_conv["next"])
                # if the id does not exist then something wrong wioth tree
                if (next_id == "Not Found"):
                    reply = {"prompt_id": current_id, "prompt": "the conversation id does not exist", "type": curr_conv["type"], 
                        "choice":curr_conv["choice"]}
                    return reply              
                
                else:
                    #unsuccessful insertion of message
                    if(not self.insert(message, next_id)):
                        reply = {"prompt_id": current_id, "prompt": "Something went wrong with my brain, please try again", "type": curr_conv["type"], 
                        "choice":curr_conv["choice"]}
                        return reply
       
        ## handle non choice responses
        else:
            #can't handle multiple options in open setting right now, no parsing or machine learning yet
            if(len(curr_conv["next"]) > 1):
                next_id = classify(user_message, curr_conv["next"])
            else:
                next_id = curr_conv["next"][0]["id"]
                
            # if the id does not exist then something wrong wioth tree
            if (next_id not in self.conversation):
                reply = {"prompt_id": current_id, "prompt": "the conversation id does not exist", "type": curr_conv["type"]}
                return reply
            #update failed
            if (not self.insert(message, next_id)):
                reply = {"prompt_id": current_id, "prompt": "Something went wrong with my brain, please try again", "type": curr_conv["type"]}
                return reply

        #all checks should be successful by here
        next_conv = self.conversation[next_id]
        if(next_conv["type"] == "choice"):
            reply = {"prompt_id": next_id,"prompt": next_conv["prompt"], "choice": next_conv["choice"], 
                    "type": next_conv["type"]}
            return reply
        elif next_id == "form" and not self.experiment:
            #######################do some thinf skf
            url = self.userReplies.get_url(self.topic, self.bot_type, message["user_id"])
            if url:
                reply = {"prompt_id": next_id,"prompt": "Please fill out the following form:",\
                    "type": next_conv["type"], "url": url, "url_text": "Link to Form"}
            else:
                reply = {"prompt_id": next_id,"prompt": "Something went wrong!",\
                    "type": next_conv["type"]}
            return reply
        else:
            reply = {"prompt_id": next_id,"prompt": next_conv["prompt"], "type": next_conv["type"]}
            return reply