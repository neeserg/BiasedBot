import requests
from model.FacebookConversation import FacebookConversation

URL = "https://graph.facebook.com/v2.6/me/messages"
PAGE_ACCESS_TOKEN = 'EAAHNiDyhU9QBAKWlBlelvxnFLXAfMcT8nR2S7ZBpVEq0HnGYHB2r2dfybmkhbEZAhiL0AmbeclhcZBny5D77ksOPI7mNgN0w64dt83WuVnxz9jBeWwlf0v9XYnWaUfHEjBUMLcSmelFTulEdPtmpC01aXsmC0px92m8NQ0TU8f8sdGFIAMIsm212hCysWUZD'

data = {
    "message":{
        "text": "Sorry try again"
  }
}

state = {
    "sender_action":"typing_on"
}
# resp = requests.post(URL+"?access_token="+PAGE_ACCESS_TOKEN, json=data)

# print(resp.content)

def send_reply(message):
    message = message[0]
    sender = message["sender"]["id"]
    state["recipient"] = {"id": sender}
    resp = requests.post(URL+"?access_token="+PAGE_ACCESS_TOKEN, json=state)
    if "postback" in message:
        text = message["postback"]["title"]
    elif "message" in message:
        text = message["message"]["text"]
    else:
        response =  data
        response["recipient"] = {"id": sender}
        return response
    strategy = Conversation(sender)
    response = {}
    response["message"] = {}
    response["message"]["text"] = strategy.get_next(text)
    response["recipient"] = {"id": sender}
    resp = requests.post(URL+"?access_token="+PAGE_ACCESS_TOKEN, json=response)
    print(resp.content)
    return response
    
