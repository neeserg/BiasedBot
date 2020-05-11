from flask import Flask,request, jsonify,render_template, redirect
from flask_restful import Resource, Api
from model.strategies.empathyStrategy import EmpathyStrategy
from model.database.Experiment import Experiment
from extra_functions import generate_experiments
import uuid
import random

app = Flask(__name__, static_folder="Frontend/static", template_folder="Frontend/templates/")
api = Api(app)

app.config.from_object(__name__)
app.config['SECRET_KEY'] = '12djknk2jnkxlalqnlkn23kndla'

class EmpathyBot(Resource):

    def get(self, experiment,bot_type, topic, prompt_id):
        if experiment =="experiment":
            bot = EmpathyStrategy(topic=topic, bot_type=bot_type, exper=experiment)
        else:
             bot = EmpathyStrategy(topic=topic, bot_type=bot_type) 
        response = bot.get_prompt(prompt_id)
        return jsonify(response)

    def post(self, experiment,bot_type,topic,prompt_id):
        json_data = request.get_json(force=True)
        if experiment =="experiment":
            bot = EmpathyStrategy(topic=topic, bot_type=bot_type, exper=experiment)
        else:
             bot = EmpathyStrategy(topic=topic, bot_type=bot_type) 
        response = bot.get_next(json_data)     
        return jsonify(response)
        
###################################################################################################################################################################################
@app.route("/<string:bot_type>", methods=['GET', 'POST'])
def land(bot_type):
    if request.method == "POST":
        topic = request.form["topic"]
        return redirect("/%s/%s"%(bot_type, topic))
    topics = [ ("affirmative_action","Affirmative Action"),("free_speech", "Free Speech")]
    return render_template("landing.html", bot_type = bot_type, topics = topics)

@app.route("/")
def landing():
    topics = [("affirmative_action", "Affirmative Action"),("free_speech", "Free Speech")]
    bot_type = random.choice(["character","lara", "logical"])
    return render_template("landing.html",  bot_type = bot_type, topics = topics)

@app.route("/<string:bot_type>/<string:topic>")
def chat(bot_type, topic):
    user_id ="hghjgjhg,k"
    return render_template("index.html", user_id = user_id, \
        experiment = "practice",bot_type = bot_type, topic= topic)


#########################EXPERIMENT API####################################################################################################################################################
''' creates a random experiment'''
@app.route("/form/generate/<string:name>")
def generateform(name):
    from_data = generate_experiments(name)
    experiment = Experiment()
    experiment.create_experiment(from_data)
    return redirect(from_data["before"])

@app.route("/finished/<string:user_id>")
def finish_experiment(user_id):
    experiment = Experiment()
    code = experiment.finished()
    return render_template("finished.html", user_id = user_id)

@app.route("/form/<string:bot_type1>/<string:bot_type2>/<string:topic1>/<string:topic2>")
def experiment(bot_type1, bot_type2, topic1,topic2):
    user_id = str( uuid.uuid1())
    domain = "https://neesergp.typeform.com/to"
    before = "RInkXP"
    after = "yLqwfQ"
    url = "%s/%s?user_id=%s&nexttopic=%s&nexttype=%s"%\
        (domain,before,user_id, topic1, bot_type1)
    url1 = "%s/%s?user_id=%s&nexttopic=%s&nexttype=%s&topic=%s&bot_type=%s"%\
        (domain, after,user_id, topic2, bot_type2, topic1, bot_type1)
    
    url2 = "%s/%s?user_id=%s&nexttopic=%s&nexttype=%s&topic=%s&bot_type=%s"%\
        (domain, after, user_id, "done", "done", topic2, bot_type2)

    from_data = {"user_id":user_id,
                  "chat":[],
                  "forms":[],
                  "before": url,
                  bot_type1+topic1: url1,
                  bot_type2+topic2: url2,}
    experiment = Experiment()
    experiment.create_experiment(from_data)
    return redirect(url)


@app.route("/experiment/<string:bot_type>/<string:topic>/<string:user_id>")
def chat_experiment(bot_type, topic, user_id,):
    return render_template("index.html", user_id = user_id, experiment = "experiment",\
        bot_type = bot_type, topic = topic)



@app.route("/webhook/form", methods=['GET', 'POST'])
def webhook_form():
    if request.method == "POST":
        experiment = Experiment()
        answer = request.get_json()
        form ={}
        user_id = answer["form_response"]["hidden"]["user_id"]
        form["user_id"] = user_id
        if "topic" in answer["form_response"]["hidden"]:
            topic = answer["form_response"]["hidden"]["topic"]
            bot_type = answer["form_response"]["hidden"]["bot_type"]
            form["bot_type"] = bot_type
            form["topic"] = topic
        form["experiment"] = answer
        worked = experiment.update_form(form)
        if worked:
            return "OK"
        else:
            return "NO Ok"

    return "Ok"

api.add_resource(EmpathyBot, '/resources/<string:experiment>/<string:bot_type>/<string:topic>/<string:prompt_id>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000 ,debug=True)
