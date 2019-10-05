from flask import Flask, request, jsonify, Response, render_template
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_restful import Resource, Api
from Forms import ExperimenterForm
# from facebook_api import send_reply
# from strategies.selection_strategy import SimpleFormSelection
app = Flask(__name__)
api = Api(app)
VERIFY_TOKEN = 'qqwmHHGCKO1122P2PP3Q2Q2QQ11b5242225267ju2j2xkou'

app.config.from_object(__name__)
app.config['SECRET_KEY'] = '12djknk2jnkxlalqnlkn23kndla'



@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ExperimenterForm()
    if form.validate_on_submit():
        print("%s, %s, %s"%(form.parameter.data, form.username.data, form.remember_me.data))
    return render_template("index.html", form=form)


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
