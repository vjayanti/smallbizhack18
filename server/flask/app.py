from flask import Flask, request

from tsheets import get_users

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/swap_shifts', methods=['POST', 'GET'])
def swap_shifts():
    if request.method == 'POST':
        return 'post swap'
    if request.method == "GET":
        return 'get swap'


@app.route('/cover_shifts')
def cover_shift():
    return 'cover'


@app.route('/users', methods=['GET'])
def users():
    return get_users()


if __name__ == '__main__':
    app.run()

