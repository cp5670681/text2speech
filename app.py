from flask import Flask, request
from wechatpy import parse_message
from wechatpy.replies import TextReply

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return request.args.get('echostr')
    xml = request.get_data().decode()
    print(xml)
    msg = parse_message(xml)
    if msg.type == 'text':
        reply = TextReply(content=msg.content, message=msg)
        return reply.render()
    return ''


if __name__ == '__main__':
    app.run()
