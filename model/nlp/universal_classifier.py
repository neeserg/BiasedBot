import tensorflow as tf
import tensorflow_hub as hub
import numpy as np


with open("model/nlp/model_file_url") as file:
    url = file.readline()
    url = url[:-1]
    print(url)



def get_score(user_resp, avail_list,embed):
    le = len(avail_list)
    user = embed([user_resp])
    print("here")
    score = 0
    for el in avail_list:
        t = embed([el])
        score += np.inner(t,user)[0]/le
    return score

def classify(user_resp, next_nodes):
    max_score = 0
    max_id = next_nodes[0]["id"]
    embed = hub.load(url)
    for node in next_nodes:
        curr_score = get_score(user_resp, node["user_replies"], embed)
        if curr_score>max_score:
            max_id = node["id"]
            max_score = curr_score
    return max_id
