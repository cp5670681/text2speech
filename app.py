from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    print(request.get_data().decode())
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
