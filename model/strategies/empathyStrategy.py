import json
file_stuff = {
    "empathybot":{
        "climatechange": "empathy_climate.json"
    },
    "parallelbot": {
        "climatechange": "parallel_climate.json"
    }
}

class EmpathyStrategy:

    def __init__(self, topic="climatechange", bot_type="parallelbot"):
        self.conversation = {}
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
    
    def get_next(self, message):
        user_message = message["message"]
        current_id = message["prompt_id"]
        if (current_id not in self.conversation):
            reply = {"prompt_id": current_id, "prompt": "the conversation id does not exist", "type": self.conversation[current_id]["type"]}
            return reply
        curr_conv = self.conversation[current_id]
        
        if(curr_conv["type"] == "choice"):
            if(user_message.strip().lower() not in curr_conv["choice"]):
                reply = {"prompt_id": current_id, "prompt": "Not part of the available choices", "type": curr_conv["type"], 
                        "choice":curr_conv["choice"]}
                return reply
            else:
                next_id = self._get_which(user_message, curr_conv["next"])
                if (next_id == "Not Found"):
                    reply = {"prompt_id": current_id, "prompt": "the conversation id does not exist", "type": curr_conv["type"], 
                        "choice":curr_conv["choice"]}
                    return reply
                else:
                    next_conv = self.conversation[next_id]
                    
                    if(next_conv["type"] == "choice"):
                        reply = {"prompt_id": next_id,"prompt": next_conv["prompt"], "choice": next_conv["choice"], 
                                "type": next_conv["type"]}
                        return reply
                    else:
                        reply = {"prompt_id": next_id,"prompt": next_conv["prompt"], "type": next_conv["type"]}
                        return reply
        
        else:
            if(len(self.conversation[current_id]["next"]) > 1):
                ##do some machinelearning to decide what the next step is
                reply = {"prompt_id": current_id, "prompt": "currently there is no machine learning", "type": curr_conv["type"]}
                return reply
            else:
                next_id = curr_conv["next"][0]["id"]
                
                if (next_id not in self.conversation):
                    reply = {"prompt_id": current_id, "prompt": "the conversation id does not exist", "type": curr_conv["type"]}
                    return reply
                
                
                next_conv = self.conversation[next_id]
                if(next_conv["type"] == "choice"):
                    reply = {"prompt_id": next_id,"prompt": next_conv["prompt"], "choice": next_conv["choice"], 
                            "type": next_conv["type"]}
                    return reply
                else:
                    reply = {"prompt_id": next_id,"prompt": next_conv["prompt"], "type": next_conv["type"]}
                    return reply