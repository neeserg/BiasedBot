import json
import spacy

nlp = spacy.load('en_vectors_web_lg')

class Option_strategy():
    def __init__(self, sender_id, response):
        self.sender_id = sender_id
        with open("json_templates/noButtonConversation.json") as file:
            self._templates = json.load(file)
        with open("strategies/state.json") as file:
            self._states = json.load(file)
            if sender_id in self._states:
                self._state = self._get_next(response, self._states[sender_id])
                self._states[sender_id] = self._state
            else:
                self._states[sender_id] = "0"
                self._state = "0"
        
# this gets the next prompt           
    def _get_next(self, response, state):
        current = self._get_prompt(state)
        next = current["next"]
        if type(next) is str:
            return next
        else:
            best = self.classify(response, next)
            return next[best]
        
    
    def _get_prompt(self, state):
        for el in self._templates:
            if el["_id"] == state:
                return el
    

    def get_message(self):
        return self._get_prompt(self._state)["message"]
    
    def update(self):
        with open("strategies/state.json", "w") as file:
            json.dump(self._states,file)
    
    def classify(self, response, options):
        best = ""
        max_score = 0.0
        resp_vector = nlp(response)
        for option in options:
            option_vector = nlp(option.lower())
            score = option_vector.similarity(resp_vector)
            if score > max_score:
                best = option
                max_score = score

        return best