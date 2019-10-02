import numpy as np
import spacy as sp

nlp = sp.load("en_core_web_lg")

def combo_classify(cat_l, token_l):
    cat = nlp(" ".join(cat_l))
    cat_s = set(cat_l)
    token_s = set(token_l)
    sentence = nlp(" ".join(token_l))
    sim1 = sentence.similarity(cat)
    sim = len(cat_s.intersection(token_s))
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
