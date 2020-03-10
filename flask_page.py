from flask import Flask,request, jsonify,render_template, redirect
from flask_restful import Resource, Api
from model.strategies.empathyStrategy import EmpathyStrategy
import uuid

app = Flask(__name__, static_folder="Frontend/static", template_folder="Frontend/templates/")
api = Api(app)

app.config.from_object(__name__)
app.config['SECRET_KEY'] = '12djknk2jnkxlalqnlkn23kndla'

class EmpathyBot(Resource):

    def get(self, bot_type, topic, prompt_id):
        bot = EmpathyStrategy(topic=topic, bot_type=bot_type)        
        print(bot.get_prompt(prompt_id))
        return jsonify(bot.get_prompt(prompt_id))

    def post(self,bot_type,topic,prompt_id):
        json_data = request.get_json(force=True)
        bot = EmpathyStrategy(topic=topic, bot_type=bot_type)       
        print(bot.get_next(json_data))
        return jsonify(bot.get_next(json_data))
        


@app.route("/<string:bot_type>", methods=['GET', 'POST'])
def land(bot_type):
    if request.method == "POST":
        topic = request.form["topic"]
        return redirect("/%s/%s"%(bot_type, topic))
    topics = [("climatechange", "Climate Change")]
    return render_template("landing.html", bot_type = bot_type, topics = topics)

@app.route("/")
def landing():
    topics = [("climatechange", "Climate Change")]
    return render_template("landing.html",  bot_type = "empathybot", topics = topics)

@app.route("/<string:bot_type>/<string:topic>")
def chat(bot_type, topic):
    return render_template("index.html", user_id = str( uuid.uuid1() ))

api.add_resource(EmpathyBot, '/<string:bot_type>/<string:topic>/resources/<string:prompt_id>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000 ,debug=True)
