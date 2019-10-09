import numpy as np
import spacy as sp

nlp = sp.load("en_core_web_lg")

def combo_classify(cat_l, token_l, union = True):
    cat = nlp(" ".join(cat_l))
    cat_s = set(cat_l)
    token_s = set(token_l)
    sentence = nlp(" ".join(token_l))
    sim1 = 0
    sim = 0
    if not cat_s or not token_s:
        sim1 = 0.1
    else:
        sim1 = sentence.similarity(cat)
    if union:
        u_size = len(cat_s.union(token_s))
        sim = len(cat_s.intersection(token_s))/(u_size+1)
    else:        
        sim = len(cat_s.intersection(token_s))/(len(token_s)+1)
    return (sim, sim1)

def tokenize(doc):
    sentence = nlp(doc)
    sent_l = [] 
    for token in sentence:
        if not (token.is_stop or token.is_punct):
            sent_l.append(token.text) 
    return sent_l


def classify(message, keys):
    _max = 0
    best = keys[0]
    mes_vec  = nlp(message)
    for key in keys:
        sim = nlp(key).similarity(mes_vec)
        if sim > _max:
            best = key
            _max = sim
    return best
