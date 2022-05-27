from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route('/ajax', methods=["get", "post"])
def hello_world():
    name = request.values.get("name")
    score = request.values.get("score")
    print(f"收到名字是：{name},成绩是：{score}")
    return 'hello_world'


@app.route('/')
def index():
    return render_template("FundEvaluation.html")


if __name__ == '__main__':
    app.run()
