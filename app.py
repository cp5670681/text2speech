from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return request.args.get('echostr')
    print(request.get_data().decode())
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
