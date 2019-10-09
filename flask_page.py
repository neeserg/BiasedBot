from flask import Flask, request, jsonify, Response, render_template, redirect
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_restful import Resource, Api
from Forms import ExperimenterForm, TopicForm, AssessmentForm
from model.CRUD import update_conversation, create_conversation, get_response, is_before, is_after
import uuid
# from facebook_api import send_reply

app = Flask(__name__, static_folder="ReactApp/build/static", template_folder="ReactApp/build/")
api = Api(app)
VERIFY_TOKEN = 'qqwmHHGCKO1122P2PP3Q2Q2QQ11b5242225267ju2j2xkou'

app.config.from_object(__name__)
app.config['SECRET_KEY'] = '12djknk2jnkxlalqnlkn23kndla'

@app.route("/<testing>/<stuff>")
def test(testing, stuff):
    return testing+" "+stuff

@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ExperimenterForm()
    if form.validate_on_submit():
        converse = {}
        uid = str(uuid.uuid1())
        converse["userId"] = uid
        converse["bot_resp"] = []
        converse["user_resp"] = []
        _filter = {}
        if form.parameter.data and  form.parameter.data != "none":
            _filter["type"] = form.parameter.data
        if form.arguement_type.data and  form.arguement_type.data != "none":
            _filter["arguement_type"] = form.arguement_type.data
        converse["filter"] = _filter
        converse["strategy"] = form.strategy.data
        converse["assessment"] = form.assessment.data
        converse["active"] = True
        create_conversation(converse)
        return redirect("/topic/%s"%uid)

    return render_template("experimenter.html", form=form)

@app.route("/topic/<userId>", methods=['GET', 'POST'])
def topic(userId):
    form = TopicForm()
    if form.validate_on_submit():
        topic = form.topic.data
        topic_l = topic.split(',')
        print(topic)
        topic = {}
        topic["desposition"] = int(topic_l[0])
        topic["topic"] = topic_l[1]
        if not update_conversation(userId, topic):
            return redirect("/")
        before = is_before(userId)
        if before == "no doc":
            return redirect("/")
        elif before == "before":
            return redirect("/assessment/before/%s"%userId)
        else:
            return redirect("/chatbot/%s"%userId)
    return render_template("topic.html", form=form)

@app.route("/assessment/<before>/<userId>", methods=['GET', 'POST'])
def assessment(before,userId):
    form = AssessmentForm()
    if form.validate_on_submit():
        assessment = {}
        assessment[before] = {}
        assessment[before]["apathy"] = form.apathy.data
        assessment[before]["research"] = form.research.data
        assessment[before]["openness"] = form.openness.data
        assessment[before]["disscussion"] =form.disscussion.data
        assessment[before]["heard"] = form.heard.data
        if not update_conversation(userId, assessment):
            return redirect("/")
        if before == "before":
            return redirect("/chatbot/%s"%userId)
        else:
            return redirect("/end/userId")
    return render_template("assessment.html", form=form)

@app.route("/chatbot/<userId>", methods=['GET', 'POST'])
def chat(userId):
    if request.method == 'POST':
        user_message = request.get_json()
        print(user_message)
        print(userId)
        response = get_response(userId, user_message["message"])
        print(response)
        return jsonify(response)
    return render_template("index.html", userId = userId)

@app.route("/end/<userId>")
def end_of(userId):
    after = is_after(userId)
    if after == "after":
        return redirect("/assessment/after/%s"%userId)
    else:
        return "<h1 style='color:blue'>Thank You For The Conversation!!!</h1>"


# class WebHook(Resource):
#     def get(self):
#         mode  = request.args.get("hub.mode")
#         token = request.args.get("hub.verify_token")
#         print(token)
#         challenge = request.args.get("hub.challenge")
#         print(challenge)
#         if token == VERIFY_TOKEN and mode == 'subscribe':
#             return Response(challenge, 200)
#         else:
#             return "INVALID REQUEST", 403
#     def post(self):
#         res = request.get_json()
#         print(res)
#         if res["object"] != "page":
#             print("not Ok")
#             return "not Ok"
#         else:
#             for entry in res["entry"]:
#                 send_reply(entry["messaging"])
#         return "ok"
        

# api.add_resource(WebHook, '/webhook')
if __name__ == '__main__':
    app.debug=True
    app.run(port = 5000)
