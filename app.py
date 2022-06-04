from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/FundEvaluation', methods=['GET', 'POST'])
def index():
    return render_template("FundEvaluation.html")


@app.route('/')
def mainPage():
    return render_template("MainPage.html")


@app.route('/testAjax', methods=['POST'])
def testAjax():
    value = request.form.get("value")
    data = request.args.get("data")
    endDate = request.args.get("endDate")
    return {'success': '1'}


if __name__ == '__main__':
    app.run()
