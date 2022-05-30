from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/FundEvaluation')
def index():
    return render_template("FundEvaluation.html")


@app.route('/')
def mainPage():
    return render_template("MainPage.html")


if __name__ == '__main__':
    app.run()
