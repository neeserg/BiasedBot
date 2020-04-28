import random
import uuid

def make_url(conv):
    user_id = str( uuid.uuid1())
    conv = conv + [("done", "done")]
    domain = "https://neesergp.typeform.com/to"
    before = "RInkXP"
    after = "yLqwfQ"
    form_data = {"user_id":user_id,
                  "chat":[],
                  "forms":[]}
    form_data["before"] = "%s/%s?user_id=%s&nexttopic=%s&nexttype=%s"%\
        (domain,before,user_id, conv[0][0], conv[0][1])
    for i in range(len(conv)-1):
        topic, bot, next_topic, next_bot = (conv[i][1], conv[i][0], conv[i+1][1],conv[i+1][0])
        form_data[bot+topic] = "%s/%s?user_id=%s&nexttopic=%s&nexttype=%s&topic=%s&bot_type=%s"%\
            (domain, after,user_id, next_topic, next_bot, topic, bot)
    
    return form_data

    

def generate_experiments():
    bot_types = ["character", "lara", "logical"]
    topic = ["affirmative_speech", "free_speech"]
    conv_order = []
    for bt in bot_types:
        for tp in topic:
            conv_order.append((bt, tp))
    random.shuffle(conv_order)
    new_conv = [(conv_order[0][0], conv_order[0][1])]
    s = set([conv_order[0][1]])
    for bt, tp in conv_order[1:]:
        if tp in s:
            new_conv.append((bt, '2_'+ tp))
        else:
            s.add(tp)
            new_conv.append((bt, '1_'+tp))
    
    return make_url(new_conv)