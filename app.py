from flask import Flask, request, render_template

from generator.generator import generate
from generator.result import Result

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    query = request.values.get('input')
    result = generate(query)
    return render_template('generator.html', query=query, host=request.host, result=repr(result))


@app.route('/hello')
def hello_world() -> str:
    return "hello world"


if __name__ == '__main__':
    app.run()
