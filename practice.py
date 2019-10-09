from model.ExperimentConversation import Conversation
import uuid

convo = Conversation("4f5e62f0-ea83-11e9-9a31-02425b01177c")

while True:
    message = input("user: ")
    resp = convo.get_next(message)
    print(resp)
    if resp == "End Of Conversation":
        break