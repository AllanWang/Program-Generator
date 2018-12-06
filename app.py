from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('generator.html', host=request.host)


@socketio.on('code_input')
def code_input(message: str):
    # TODO add action here
    emit('code_output', f"todo {str}")


@app.route('/hello')
def hello_world() -> str:
    return "hello world"


if __name__ == '__main__':
    socketio.run(app)
