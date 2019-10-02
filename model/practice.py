from Conversation import Conversation

convo = Conversation("practice")

while True:
    message = input("user: ")
    resp = convo.get_next(message)
    print(resp)
    if resp == "End Of Conversation":
        break