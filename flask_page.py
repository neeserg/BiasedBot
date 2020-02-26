from flask import Flask,request, jsonify,render_template, redirect
from flask_restful import Resource, Api
from model.strategies.empathyStrategy import EmpathyStrategy
import uuid

app = Flask(__name__, static_folder="Frontend/static", template_folder="Frontend/templates/")
api = Api(app)

app.config.from_object(__name__)
app.config['SECRET_KEY'] = '12djknk2jnkxlalqnlkn23kndla'

class EmpathyBot(Resource):

    def get(self, prompt_id):
        bot = EmpathyStrategy()        
        print(bot.get_prompt(prompt_id))
        return jsonify(bot.get_prompt(prompt_id))

    def post(self,prompt_id):
        json_data = request.get_json(force=True)
        bot = EmpathyStrategy()        
        print(bot.get_next(json_data))
        return jsonify(bot.get_next(json_data))
        


@app.route("/empathybot", methods=['GET',"POST"])
def chat():
    if request.method == "POST":
        return redirect("/empathybot")
    userId = str(uuid.uuid1())
    return render_template("index.html", userId = userId)

@app.route("/")
def landing():
    return render_template("landing.html")


api.add_resource(EmpathyBot, '/empathybot/resources/<string:prompt_id>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000 ,debug=True)
