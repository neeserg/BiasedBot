from flask import Flask,request, jsonify


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def func():
    if request.method =="POST":
        print(request.get_json())
        return "done"
    return 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000 ,debug=True)
